import sqlite3
import pandas as pd
import uuid
import hashlib
from tqdm import tqdm

def import_history(tsv_file, sqlite_file):
    """
    Import browser history from a TSV file into a Firefox places.sqlite database.
    Args:
        tsv_file (str): Path to the TSV file.
        sqlite_file (str): Path to the Firefox places.sqlite file.
    """
    # Read the .tsv file into a pandas DataFrame
    df = pd.read_csv(tsv_file, sep='\t', header=None, names=['url', 'timestamp', 'single_number', 'title'])

    # Connect to the SQLite database
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()

    # Get existing URLs and their ids
    c.execute("SELECT id, url FROM moz_places")
    existing_urls = {row[1]: row[0] for row in c.fetchall()}

    # Iterate over the rows of the DataFrame    
    for index, row in tqdm(df.iterrows(), total=df.shape[0]):
        url = row['url']
        title = str(row['title']).replace("'", "''")  # Escape single quotes
        rev_host = url.split('//')[-1].split('/')[0][::-1]
        guid = str(uuid.uuid4())
        url_hash = hashlib.sha1(url.encode()).hexdigest()
        #timestamp = int(float(row['timestamp'][1:]) * 1e6)  # Remove the 'U' prefix, convert to float, then to int, and multiply by 1e6
        timestamp = int(float(row['timestamp'][1:])) * 1e3 #same without milleseconds

        if url not in existing_urls:
            # URL does not exist in the table, so insert it
            c.execute("""
                INSERT INTO moz_places (url, title, rev_host, last_visit_date, guid, url_hash) 
                VALUES (?, ?, ?, ?, ?, ?)
            """, (url, title, rev_host, timestamp, guid, url_hash))

            # Get the id of the inserted row
            c.execute("SELECT last_insert_rowid()")
            place_id = c.fetchone()[0]

            # Add the new URL to the set of existing URLs
            existing_urls[url] = place_id
        else:
            # URL already exists in the table, so get its id
            place_id = existing_urls[url]

        # Insert into moz_historyvisits
        c.execute("""
            INSERT INTO moz_historyvisits (place_id, visit_date, visit_type, session) 
            VALUES (?, ?, 1, 0)
        """, (place_id, timestamp))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    # Example usage
    tsv_file = r"tests/assets/htu_backup_20250615_112854.tsv"
    sqlite_file = r"tests/assets/places.sqlite"
    import_history(tsv_file, sqlite_file)
    print("Import complete.")

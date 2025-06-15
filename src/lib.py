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
    df = pd.read_csv(tsv_file, sep='\t', header=None, names=['url', 'timestamp', 'single_number', 'title'])
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    c.execute("SELECT id, url FROM moz_places")
    existing_urls = {row[1]: row[0] for row in c.fetchall()}
    for index, row in tqdm(df.iterrows(), total=df.shape[0]):
        url = row['url']
        title = str(row['title']).replace("'", "''")
        rev_host = url.split('//')[-1].split('/')[0][::-1]
        guid = str(uuid.uuid4())
        url_hash = hashlib.sha1(url.encode()).hexdigest()
        timestamp = int(float(row['timestamp'][1:])) * 1e3
        if url not in existing_urls:
            c.execute("""
                INSERT INTO moz_places (url, title, rev_host, last_visit_date, guid, url_hash) 
                VALUES (?, ?, ?, ?, ?, ?)
            """, (url, title, rev_host, timestamp, guid, url_hash))
            c.execute("SELECT last_insert_rowid()")
            place_id = c.fetchone()[0]
            existing_urls[url] = place_id
        else:
            place_id = existing_urls[url]
        c.execute("""
            INSERT INTO moz_historyvisits (place_id, visit_date, visit_type, session) 
            VALUES (?, ?, 1, 0)
        """, (place_id, timestamp))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    # Example usage
    tsv_file = r"tests/assets/htu_backup_20250615_112854.tsv"
    sqlite_file = r"tests/assets/places.sqlite"
    import_history(tsv_file, sqlite_file)
    print("Import complete.")

#%%
import sqlite3
import pandas as pd
import uuid
import hashlib

def import_history(tsv_file, sqlite_file):
    # Read the .tsv file into a pandas DataFrame
    df = pd.read_csv(tsv_file, sep='\t', header=None, names=['url', 'timestamp', 'unknown_number', 'title'])

    # Connect to the SQLite database
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()

    # Iterate over the rows of the DataFrame
    for index, row in df.iterrows():
        url = row['url']
        title = str(row['title']).replace("'", "''")  # Escape single quotes
        rev_host = url.split('//')[-1].split('/')[0][::-1]
        guid = str(uuid.uuid4())
        url_hash = hashlib.sha1(url.encode()).hexdigest()
        #timestamp = int(float(row['timestamp'][1:]) * 1e6)  # Remove the 'U' prefix, convert to float, then to int, and multiply by 1e6
        timestamp = int(float(row['timestamp'][1:])) * 1e3 #same without milleseconds

        # Insert into moz_places
        c.execute("""
            INSERT INTO moz_places (url, title, rev_host, last_visit_date, guid, url_hash) 
            VALUES (?, ?, ?, ?, ?, ?)
        """, (url, title, rev_host, timestamp, guid, url_hash))

        # Get the id of the inserted row
        c.execute("SELECT last_insert_rowid()")
        place_id = c.fetchone()[0]

        # Insert into moz_historyvisits
        c.execute("""
            INSERT INTO moz_historyvisits (place_id, visit_date, visit_type, session) 
            VALUES (?, ?, 1, 0)
        """, (place_id, timestamp))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

tsv_file = r"C:\Users\user\Downloads\htu_backup_202....tsv"
sqlite_file = r"C:\Users\user\AppData\Roaming\Mozilla\Firefox\Profiles\profileblub\places.sqlite"
import_history(tsv_file, sqlite_file)
# %%

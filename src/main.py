#%%
import os
import shutil
from datetime import datetime
import argparse
from lib import import_history

def backup_files(file_paths):
    # Backup the input files into a timestamped subdirectory in bak
    bak_dir = os.path.join(os.path.dirname(__file__), '..', 'bak')
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    bak_subdir = os.path.join(bak_dir, timestamp)
    os.makedirs(bak_subdir, exist_ok=True)
    for file_path in file_paths:
        if os.path.exists(file_path):
            base_file = os.path.basename(file_path)
            bak_file_path = os.path.join(bak_subdir, base_file)
            shutil.copy2(file_path, bak_file_path)

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Import browser history from TSV to Firefox places.sqlite.")
    parser.add_argument("tsv_file", help="Path to the TSV file")
    parser.add_argument("sqlite_file", help="Path to the Firefox places.sqlite file")
    args = parser.parse_args()
    backup_files([args.tsv_file, args.sqlite_file])
    
    import_history(args.tsv_file, args.sqlite_file)

    print("Import complete.")
# %%

#%%
from lib import import_history
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Import browser history from TSV to Firefox places.sqlite.")
    parser.add_argument("tsv_file", help="Path to the TSV file")
    parser.add_argument("sqlite_file", help="Path to the Firefox places.sqlite file")
    args = parser.parse_args()
    import_history(args.tsv_file, args.sqlite_file)
    print("Import complete.")
# %%

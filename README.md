# Chrome History Trends Unlimited import to Mozilla Firefox

This repository contains a Python script for importing the data of Chrome's extension "History Trends Unlimited" to Mozilla Firefox.

## Description

The `import_history` function in `src/lib.py` takes a `.tsv` file and a `places.sqlite` file as input. The `.tsv` file should contain the browsing history data to be imported, and the `places.sqlite` file is the SQLite database used by Firefox to store browsing history.

The tsv file contains a column with numbers, which is not used.

The function reads the `.tsv` file into a pandas DataFrame, connects to the SQLite database, and iterates over the rows of the DataFrame. For each row, it checks if the URL already exists in the `moz_places` table of the database. If the URL does not exist, it inserts a new row into the `moz_places` table. Then, it inserts a new row into the `moz_historyvisits` table.

The function uses the `uuid` module to generate a random GUID for each new place, and the `hashlib` module to generate a hash of the URL. The timestamp from the DataFrame is used for the `last_visit_date` and `visit_date`.


## Usage

The tsv file is created by exporting in History Trends Unlimited.

### With [uv](https://github.com/astral-sh/uv) (recommended)

Run the import script with arguments:

```bash
uv run python src/main.py path/to/your.tsv path/to/places.sqlite
```

Replace `path/to/your.tsv` and `path/to/places.sqlite` with your actual file paths.

### Arguments
- The first argument is the path to your exported `.tsv` file.
- The second argument is the path to your Firefox `places.sqlite` file (usually found in your Firefox profile directory).

### Automatic Backup
Before any import, the script automatically creates a backup of the parent folder of each input file. The backup is stored in the `bak` directory in the project root, with a timestamp appended to the folder name. This ensures you can always restore your original data if needed.

### Example
```bash
uv run python src/main.py tests/assets/htu_backup_20250615_112854.tsv tests/assets/places.sqlite
```

### Warning
This script directly manipulates the places.sqlite database used by Firefox. Always make a backup of your places.sqlite file before running this script. Ensure that Firefox is not running when you execute this script to prevent any potential conflicts. Use this script at your own risk. The author is not responsible for any potential data loss or corruption.



# Chrome History Trends Unlimited import to Mozilla Firefox

This repository contains a Python script for importing the data of chromes extension "History Trends Unlimited" to Mozilla Firefox.

## Description

The `import_history` function in `import_history.py` takes a `.tsv` file and a `places.sqlite` file as input. The `.tsv` file should contain the browsing history data to be imported, and the `places.sqlite` file is the SQLite database used by Firefox to store browsing history.

The tsv file contains a column with numbers, which I don't know what it is used for, so it is not used.

The function reads the `.tsv` file into a pandas DataFrame, connects to the SQLite database, and iterates over the rows of the DataFrame. For each row, it checks if the URL already exists in the `moz_places` table of the database. If the URL does not exist, it inserts a new row into the `moz_places` table. Then, it inserts a new row into the `moz_historyvisits` table.

The function uses the `uuid` module to generate a random GUID for each new place, and the `hashlib` module to generate a hash of the URL. The timestamp from the DataFrame is used for the `last_visit_date` and `visit_date`.



## Usage

The tsv file is created, by doing an export in History Trends Unlimited.

To use the `import_history` function, call it with the paths to your `.tsv` file and `places.sqlite` file, found in AppData\Roaming\Mozilla\Firefox\Profiles\your_profile :

```python
import_history('path_to_your_tsv_file.tsv', 'path_to_your_places.sqlite')
```

Please replace 'path_to_your_tsv_file.tsv' and 'path_to_your_places.sqlite' with the actual paths to your .tsv file and places.sqlite file respectively.

Please adjust the content as necessary to fit your needs. If you have any other questions or need further assistance, feel free to ask.  😊

### Warning
This script directly manipulates the places.sqlite database used by Firefox. Always make a backup of your places.sqlite file before running this script. Ensure that Firefox is not running when you execute this script to prevent any potential conflicts. Use this script at your own risk. The author is not responsible for any potential data loss or corruption.



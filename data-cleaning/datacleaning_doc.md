Python script that cleans *Global_Mobile_Prices_2025_Extended_dirty.csv* dataset through the following operations:
- checks duplicates and removes them if found,
- sets data types,
- normalizes data,
- detects and removes outliers,
- handles NaN values.

Input: *Global_Mobile_Prices_2025_Extended_dirty.csv*  
Output: *Global_Mobile_Prices_2025_Extended_clean.csv*

Important:
- place input file in the same directory as the script,
- pandas library need to be installed,
- during script execution, choose whether to delete or keep records with NaN.
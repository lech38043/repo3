Python script that import dataset from *Global_Mobile_Prices_2025_Extended_clean.csv* to Microsoft SQL Server. The result is a cleaned source table that is ready for further operations in database.

Input: *Global_Mobile_Prices_2025_Extended_clean.csv*  
Output: 
*'src' table in MS SQL Server database*

IMPORTANT! Before run the script:
1) On your local machine install:
    - Microsoft SQL Server - [MS SQL Server 2022 Express](https://www.microsoft.com/en-us/download/details.aspx?id=104781&lc=1033&msockid=3f317202607163c33ed9646061d0621c),
    - SQL Server Management Studio SSMS - [SSMS 22](https://learn.microsoft.com/en-us/ssms/install/install?view=sql-server-ver16.),
    - python libraries: pandas, sqlalchemy and pyodbc.

2) Open SSMS and connect to your local server:
    - use 'Windows Authentication',
    - check "Trust Server Certificate".

3) In SSMS create a database named 'smartphone_market'.

4) In the script, enter the name of your local server (like 'DESKTOP-XXXXXXX\SQLEXPRESS').
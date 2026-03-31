import pandas as pd
from sqlalchemy import create_engine, types, text
import os
import sys


csv_file_path=os.path.join(os.path.dirname(os.path.abspath(__file__)),'Global_Mobile_Prices_2025_Extended_clean.csv') #Place source file in the same directory as the script, otherwise put full path
server=r'DESKTOP-XXXXXXX\SQLEXPRESS' #Enter the name of your local server
database='smartphone_market' #Before run the script, create 'smartphone_market' database in your local server
table='src' #Table name that are created in the database
dtypes_schema={
        'brand': types.VARCHAR(10),
        'model': types.VARCHAR(30),
        'model_var': types.VARCHAR(30),
        'price_usd': types.SMALLINT,
        'ram_gb': types.SMALLINT,
        'storage_gb': types.SMALLINT,
        'camera_mp': types.SMALLINT,
        'battery_mah': types.SMALLINT,
        'display_size_inch': types.DECIMAL(2,1),
        'charging_watt': types.SMALLINT,
        '5g_support': types.Boolean,
        'os': types.VARCHAR(10),
        'processor': types.VARCHAR(30),
        'rating': types.DECIMAL(2,1),
        'release_month': types.SMALLINT,
        'year': types.SMALLINT}

run=input(f'IMPORTANT - read the "csv_to_mssql_doc.md" before run the script! (Press Enter to continue...)\n')

def csv_to_mssql():
    # Loading csv and creating data frame
    try:
        print('Loading CSV file...')
        df=pd.read_csv(csv_file_path)
        print(f'  |_ lodaded {len(df)} records\n')
    except Exception as e:
        print(f'ERROR OCCURED: "{repr(e)}"')
        input('Press Enter to close...')
        sys.exit()

    #Exporting to mssql
    try:
        print('Exporting to MS SQL database...')
        engine=create_engine(f'mssql+pyodbc://{server}/{database}?''driver=ODBC+Driver+17+for+SQL+Server''&trusted_connection=yes') #Works only with Windows authenticated coonnection to server
        df.to_sql(table, con=engine, if_exists='replace', index=False, dtype=dtypes_schema) #Creating table in db
        conn=engine.connect()
        print(f'  |_ imported {conn.execute(text(f'SELECT COUNT(*) FROM {table}')).scalar()} records') #Checking number of imported records in db
        engine.dispose() #Closing connections to database
    except Exception as e:
        print(f'ERROR OCCURED: "{repr(e)}"')
        input('Press Enter to close...')
        sys.exit()


if __name__ == "__main__":
    csv_to_mssql()
    input('\nPress Enter to close...') #Prevents console window from closing
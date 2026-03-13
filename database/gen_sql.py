
#%%
import pandas as pd
import datetime

# dirty_file_path="../data-cleaning/Global_Mobile_Prices_2025_Extended_dirty.csv" #Place source file in the same directory as the script, otherwise put full path
clean_file_path="../data-cleaning/Global_Mobile_Prices_2025_Extended_clean.csv" #Place source file in the same directory as the script, otherwise put full path

# coded by Marcin
dtypes_schema={
    'brand':'string',
    'model':'string', 
    'price_usd':'Int64',
    'ram_gb':'Int64',
    'storage_gb':'Int64',
    'camera_mp':'Int64',
    'battery_mah':'Int64',
    'display_size_inch':'float64',
    'charging_watt':'Int64',
    '5g_support':'boolean',
    'os':'string',
    'processor':'string',
    'rating':'float64',
    'release_month':'category',
    'year':'Int64'}

# coded by Marcin
def set_dtypes(df,dtypes_schema): #Setting data types according to the defined schema
    try:
        print('  |_ setting data types:')
        for col, dtype in dtypes_schema.items():
            if dtype=='Int64':
                df[col]=df[col].astype('Float32') #Prevents error
                df[col]=df[col].astype(dtype)
            elif dtype=='boolean':
                df[col]=df[col].map({'Yes':1,'No':0}) #Replacing to bool-like values
                df[col]=df[col].astype(dtype)
            else:
                df[col]=df[col].astype(dtype)
            print(f'     |_ {col}: {df[col].dtype}')
    except Exception as e:
        print(f'ERROR OCCURED: "{repr(e)}"')

    return df

# loading files to dataframes and setting dtypes
df_clean=pd.read_csv(clean_file_path)
df_clean=set_dtypes(df_clean,dtypes_schema)
# df_dirty=pd.read_csv(dirty_file_path)
# df_dirty=set_dtypes(df_dirty,dtypes_schema)

#%% defining functions 
def pandas_to_mssql(dtype):
    if "Int" in str(dtype):
        return "BIGINT NULL"
    elif "float" in str(dtype):
        return "FLOAT"
    elif "datetime" in str(dtype):
        return "DATETIME2"
    elif "bool" in str(dtype):
        return "BIT"
    else:
        return "NVARCHAR(50)"
    
def generate_create_table(df, table_name):
    cols = []
    for col, dtype in df.dtypes.items():
        sql_type = pandas_to_mssql(dtype)
        cols.append(f"\"{col}\" {sql_type}")
    columns_sql = ",\n    ".join(cols)
    create_sql = f"CREATE TABLE {table_name}(\n    {columns_sql})"
    return create_sql

def generate_insert_sql(df, table_name):
    insert_statements = []
    for i, row in df.iterrows():
        values = []
        for val in row:
            if pd.isna(val):
                values.append("NULL")
            elif isinstance(val, str):
                values.append(f"'{val.replace('\'','\'\'')}'")  # escape '
            elif isinstance(val, (pd.Timestamp, datetime.datetime)):
                values.append(f"'{val}'")
            else:
                values.append(str(val))
        insert_statements.append(f"INSERT INTO {table_name} VALUES ({', '.join(values)});")
    return "\n".join(insert_statements)

def generate_batch_insert_sql(df, table_name, batch_size=2000):
    all_inserts = []
    num_rows = len(df)
    for start in range(0, num_rows, batch_size):
        batch = df.iloc[start:start + batch_size]
        values_list = []
        for _, row in batch.iterrows():
            values = []
            for val in row:
                if pd.isna(val):
                    values.append("NULL")
                elif isinstance(val, bool):
                    values.append(str(int(bool(val))))
                elif isinstance(val, str):
                    #values.append(f"'{val.replace(\"'\", \"''\")}'")
                    values.append("'" + val.replace("'", "''") + "'")
                elif isinstance(val, (pd.Timestamp, datetime.datetime)):
                    values.append(f"'{val.isoformat(sep=' ')}'")
                else:
                    values.append(str(val))
            values_list.append(f"({', '.join(values)})")
        batch_insert = f"INSERT INTO {table_name} VALUES\n" + ",\n".join(values_list) + ";"
        all_inserts.append(batch_insert)
    return "\n\n".join(all_inserts)

#%% generating sql files

clean_table_sql = generate_create_table(df_clean, "t_raw1")
with open("create_table.sql", "w", encoding="utf-8") as f:
    f.write(clean_table_sql)

clean_data_sql = generate_batch_insert_sql(df_clean, "clean_data")
with open("insert_data.sql", "w", encoding="utf-8") as f:
    f.write(clean_data_sql)

# dirty_table_sql = generate_create_table(df_dirty, "t_raw1")
# with open("dirty_table.sql", "w", encoding="utf-8") as f:
#     f.write(dirty_table_sql)

# dirty_data_sql = generate_batch_insert_sql(df_dirty, "dirty_data")
# with open("insert_data.sql", "w", encoding="utf-8") as f:
#     f.write(dirty_table_sql)

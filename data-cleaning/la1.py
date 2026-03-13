#%%
import pandas as pd
import datetime

csv_file_path="Global_Mobile_Prices_2025_Extended_dirty.csv" #Place source file in the same directory as the script, otherwise put full path

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

def duplicates(df): #Checking for duplicates and removing them if found
    try:
        print('  |_ checking for duplicates:')
        duplicates=df[df.duplicated(keep='first')]
        if duplicates.empty:
            print('     |_ no duplicates found.')
        else:
            df=df.drop_duplicates(keep='first')
            print(f'     |_ {len(duplicates)} duplicate record/-s removed.')
    except Exception as e:
        print(f'ERROR OCCURED: "{repr(e)}"')

    return df

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
    
def normalization(df,dtypes_schema): #Data normalization
    try:
        print('  |_ normalization:')
        print(f'     |_ replacing "ERR" values with NaN')
        df=df.replace('ERR',float('nan')) #Replacing "ERR" values with NaN
        print(f'     |_ removing leading/trailing whitespace from strings')
        print(f'     |_ converting strings to lowercase')
        print(f'     |_ rounding float values') 
        for col, dtype in dtypes_schema.items():
            if dtype=='string':
                df[col]=df[col].str.strip() #Removing leading/trailing whitespace
                df[col]=df[col].str.lower() #Converting to lowercase
            elif dtype=='float64':
                df[col]=df[col].round(1) #Rounding float values
    except Exception as e:
        print(f'ERROR OCCURED: "{repr(e)}"')

    return df

def outliers(df): #Detecting outliers and replacing them with NaN values
    try:
        print('  |_ identifying and replacing outliers with NaN')
        outl_col=['price_usd','ram_gb','storage_gb','camera_mp','battery_mah','display_size_inch','charging_watt','rating','year']
        for col in outl_col:
            if col=='price_usd': 
                df[col]=df[col].where((df[col]>=100)&(df[col]<=1500),float('nan')) #Price taken into account: 100-1500 USD
            else:
                df[col]=df[col].where(df[col].map(df[col].value_counts())>=5,float('nan')) #Values ​​that appear less than 5 times are replaced with NaN values
    except Exception as e:
        print(f'ERROR OCCURED: "{repr(e)}"')

    return df

def handling_nan(df): #Handling NaN values
    try:
        print('  |_ handling NaN values:')
        print('     |_ filling NaN if possible')

        #Filling NaN in "brand" col according to first 4 letters of model
        def get_brand(model):
            for brand, models in brand_model_dict.items():
                if model in models:
                    return brand
        df_sub_dict=df[['brand','model']].copy()
        df_sub_dict['model']=df_sub_dict['model'].str[:4]
        brand_model_dict=df_sub_dict.groupby('brand')['model'].apply(set).to_dict()
        df['brand']=df['brand'].fillna(df['model'].str[:4].apply(get_brand))

        #Filling NaN in "os" col according to brand (apple -> iOS, others -> android)
        df.loc[df['brand']=='apple','os']='ios'
        df.loc[df['brand']!='apple','os']='android'

        #Filling NaN in "year" col with 2025 value
        df['year']=df['year'].fillna(2025)

        #Removing remaining NaN values (optional)
        rows_with_nan=df.isna().any(axis=1).sum()
        removing_nan_rows=input(f'     |_ {rows_with_nan} records with NaN left. Remove them? (Y/N) ').lower()
        if removing_nan_rows == "y":
            df.dropna(how='any',inplace=True)
            print('     |_ records with NaN have been removed')
        else:
            print('     |_ records with NaN have been kept')
    except Exception as e:
        print(f'ERROR OCCURED: "{repr(e)}"')

    return df

#%%
df=pd.read_csv(csv_file_path)
# %%
df=set_dtypes(df,dtypes_schema)
#%%
df.info()
#%%
df.duplicated(subset=["model"]).sum()

# %%
df['model_dupl']=df.duplicated(subset='model')

# %%
df.sample(5)

#%%
df_cleared=pd.read_csv("Global_Mobile_Prices_2025_Extended_clean.csv")
#%%
df_cleared.duplicated(subset="model").sum()
#%%
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
        return "NVARCHAR(MAX)"
    
def generate_create_table(df, table_name):
    cols = []
    for col, dtype in df.dtypes.items():
        sql_type = pandas_to_mssql(dtype)
        if col[0].isdigit(): 
            cols.append(f"_{col} {sql_type}")
        else:
            cols.append(f"{col} {sql_type}")
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

def generate_batch_insert_sql(df, table_name, batch_size=1000):
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
#%%
create_table_sql = generate_create_table(df, "t_raw1")
with open("create_table.sql", "w", encoding="utf-8") as f:
    f.write(create_table_sql)
#%%
insert_sql = generate_batch_insert_sql(df, "t_raw1")
with open("insert_data.sql", "w", encoding="utf-8") as f:
    f.write(insert_sql)
#################################################################################
#%%
df1=df
df1.drop_duplicates(subset="model", keep="first")
# %%
df_cleared.isna().sum()
# %%
rows_with_nan=df.isna().any(axis=1).sum()
# %% Q1
kolumny = ['brand'
            ,'model'
            ,'price_usd'
            ,'ram_gb'
            ,'storage_gb'
            ,'camera_mp'
            ,'battery_mah'
            ,'display_size_inch'
            ,'charging_watt'
            ,'5g_support'
            #,'os'
            ,'processor'
            #,'rating'
            #,'release_month'
            #,'year'
            ]
# %% Q2
kolumny = ['brand'
            ,'model'
            ,'price_usd'
            ,'ram_gb'
            ,'storage_gb'
            #,'camera_mp'
            ,'battery_mah'
            ,'display_size_inch'
            #,'charging_watt'
            #,'5g_support'
            ,'os'
            #,'processor'
            ,'rating'
            #,'release_month'
            #,'year'
            ]
# %% Q3
kolumny = [#'brand'
            #,'model'
            'price_usd'
            ,'ram_gb'
            ,'storage_gb'
            ,'camera_mp'
            ,'battery_mah'
            ,'display_size_inch'
            ,'charging_watt'
            ,'5g_support'
            #,'os'
            ,'processor'
            ,'rating'
            #,'release_month'
            #,'year'
            ]
#%%
print(df_cleared[kolumny].isna().any(axis=1).sum())
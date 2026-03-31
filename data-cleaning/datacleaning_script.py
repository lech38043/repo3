import pandas as pd
import os
import sys


csv_file_path_in=os.path.join(os.path.dirname(os.path.abspath(__file__)),'Global_Mobile_Prices_2025_Extended_dirty.csv') #Place source file in the same directory as the script
csv_file_path_out=os.path.join(os.path.dirname(os.path.abspath(__file__)),'Global_Mobile_Prices_2025_Extended_clean.csv') # Output file is placed in the same directory as the script
dtypes_schema={
    'brand':'string',
    'model':'string',
    'model_var':'string', 
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
    'release_month':'Int64',
    'year':'Int64'}
month_map={'January':1,'February':2,'March':3,'April':4,'May':5,'June':6,'July':7,'August':8,'September':9,'October':10,'November':11,'December':12}


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

def init_transform(df):
    try:
        print('  |_ initial transformation:')
        print('     |_ add column with cleaned model names,')
        df=df.rename(columns={'model':'model_var'}) #Renaming "model" column to "model_var" that keeps original model names with unique variant number
        df.insert(1, 'model', df['model_var'].str.rpartition(' ')[0].str.rstrip()) #Adding new "model" column with cleaned model names
        print('     |_ mapping month names to numbers.')
        df['release_month']=df['release_month'].map(month_map) #Mapping month names to numbers 1-12
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


if __name__ == "__main__":
    #Importing "dirty" source file
    try:
        print('Loading "dirty" csv file')
        df=pd.read_csv(csv_file_path_in)
        print(f'  |_ lodaded {len(df)} records\n')
    except Exception as e:
        print(f'ERROR OCCURED: "{repr(e)}"')
        input('Press Enter to close...')
        sys.exit()

    #Data cleaning
    print('Data cleaning process:')
    df=duplicates(df)
    df=init_transform(df)
    df=set_dtypes(df,dtypes_schema)
    df=normalization(df,dtypes_schema)
    df=outliers(df)
    df=handling_nan(df)

    #Exporting "cleaned" file
    try:
        print('\nExporting "cleaned" csv file')
        df.to_csv(csv_file_path_out,index=False)
        print(f'  |_ exported {len(df)} records\n')
    except Exception as e:
        print(f'ERROR OCCURED: "{repr(e)}"')
        input('Press Enter to close...')
        sys.exit()

    #Prevents console window from closing
    input('Press Enter to close...')
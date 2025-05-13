## Sales Data Transformation Project


### Tasks:
Python (Data Cleaning & Transformation)
1. Read the multi-sheet Excel file using pandas.
2. Clean, standardize column names across sheets (e.g., lowercases, underscores).
3. Remove unwanted characters like dollar signs in prices, and convert types (str → float, int).
4. Handle inconsistent values, nulls, and duplicates.
5. Validate schema readiness before data loading to PostgreSQL.

PostgreSQL (Data Storage & Preparation)
1. Create a new schema "sales_combined_data" in a database.
2. Load cleaned tables from Python to PostgreSQL.
3. Performed SQL joins across tables to create an integrated sales_report.

Power BI (Visualization & Insights)
1. Connect Power BI to PostgreSQL to fetch the sales_combined_data.
2. Perform the final data transformations (data types, relationships, renaming columns).
3. Built dashboards using various charts to translate the data into digestible visual insights.


import pandas as pd
from sqlalchemy import create_engine, text

data = pd.read_excel(r"c:\DOWNLOADS\sales_combined_data.xlsx", sheet_name=None)

#Clean and transform Columns and sheets
def clean_columns(df):
    df.columns = [str(col).lower().replace(' ', '_').strip() for col in df.columns]
    return df
for name in data:
    df = data[name]  # Get the DataFrame for the current sheet
    df = clean_columns(df)  # Clean the column names
    
    #Remove dollar signs and convert to float for relevant columns
if 'unit_cost' in df.columns:
        df['unit_cost'] = df['unit_cost'].replace('[\$,]', '', regex=True).astype(float)
if 'unit_price' in df.columns:
        df['unit_price'] = df['unit_price'].replace('[\$,]', '', regex=True).astype(float)
    
    #Convert quantity to integer in the orders table
if name.lower() == 'orders' and 'quantity' in df.columns:
        df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce').fillna(0).astype(int)
         
         #Remove duplicates in products and customers
if name.lower() in ['product', 'customers']:
        df = df.drop_duplicates().reset_index(drop=True)

#Handle missing/inconsistent values
df = df.fillna(value=pd.NA)

#Save cleaned DataFrame back into dictionary
data[name] = df

#Connect to PostgreSQL
engine = create_engine("postgresql+psycopg2://postgres:Legend@localhost:5432/Project 1")

#Create a new schema
with engine.begin() as conn:
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS sales_combined_data;"))
    print("Schema 'sales_combined_data' created or already exists.")

#Load each DataFrame into the schema
for name, df in data.items():
    table_name = name.lower().replace(" ", "_")  # Clean table name
    df.to_sql(
        name=table_name,
        con=engine,
        schema='sales_combined_data',
        if_exists='replace',
        index=False
    )
    print(f"✅ Table '{table_name}' loaded into schema 'sales_combined_data'")
import pandas as pd
import numpy as np
from datetime import datetime
import os

def extract(file_path):
    print(f"Extracting data from {file_path}...")
    try:
        df = pd.read_csv(file_path)
        print(f"Data extracted successfully. Shape: {df.shape}")
        return df
    except Exception as e:
        print(f"Error extracting data: {e}")
        return None

def transform(df):
    print("Transforming data...")
    # Make a copy to avoid SettingWithCopyWarning
    df_transformed = df.copy()

    # 1. Handle missing values
    print("Handling missing values...")
    # Fill numerical missing values with the median
    num_cols = df_transformed.select_dtypes(include=[np.number]).columns
    for col in num_cols:
        if df_transformed[col].isnull().sum() > 0:
            df_transformed[col] = df_transformed[col].fillna(df_transformed[col].median())
            
    # Fill categorical missing values with the mode
    cat_cols = df_transformed.select_dtypes(include=['object']).columns
    for col in cat_cols:
        if df_transformed[col].isnull().sum() > 0:
            df_transformed[col] = df_transformed[col].fillna(df_transformed[col].mode()[0])

    # 2. Date conversion
    print("Converting dates...")
    if 'Dt_Customer' in df_transformed.columns:
        df_transformed['Dt_Customer'] = pd.to_datetime(df_transformed['Dt_Customer'], format='%d-%m-%Y', errors='coerce')

    # 3. Feature Engineering
    print("Engineering new features...")
    # Calculate Age (assuming current year is 2026 based on the context)
    if 'Year_Birth' in df_transformed.columns:
        df_transformed['Age'] = 2026 - df_transformed['Year_Birth']
        # Optionally, filter out unrealistic ages (e.g., > 120)
        df_transformed = df_transformed[df_transformed['Age'] <= 120]

    # Calculate Total Children
    if 'Kidhome' in df_transformed.columns and 'Teenhome' in df_transformed.columns:
        df_transformed['Total_Children'] = df_transformed['Kidhome'] + df_transformed['Teenhome']

    # Calculate Total Amount Spent
    mnt_cols = ['MntWines', 'MntFruits', 'MntMeatProducts', 'MntFishProducts', 'MntSweetProducts', 'MntGoldProds']
    available_mnt_cols = [col for col in mnt_cols if col in df_transformed.columns]
    if available_mnt_cols:
        df_transformed['Total_Amount_Spent'] = df_transformed[available_mnt_cols].sum(axis=1)

    # Calculate Total Purchases
    purchases_cols = ['NumDealsPurchases', 'NumWebPurchases', 'NumCatalogPurchases', 'NumStorePurchases']
    available_purchases_cols = [col for col in purchases_cols if col in df_transformed.columns]
    if available_purchases_cols:
        df_transformed['Total_Purchases'] = df_transformed[available_purchases_cols].sum(axis=1)
        
    # 4. Clean up unnecessary or constant columns
    if 'Z_CostContact' in df_transformed.columns and 'Z_Revenue' in df_transformed.columns:
        df_transformed = df_transformed.drop(columns=['Z_CostContact', 'Z_Revenue'], errors='ignore')

    print(f"Data transformed successfully. New shape: {df_transformed.shape}")
    return df_transformed

def load(df, output_path):
    print(f"Loading data to {output_path}...")
    try:
        df.to_csv(output_path, index=False)
        print("Data loaded successfully.")
    except Exception as e:
        print(f"Error loading data: {e}")

def run_etl():
    # Define paths
    base_dir = r"c:\Users\PC\OneDrive\Escritorio\CCiencia datos"
    input_file = os.path.join(base_dir, "customer_behavior_dataset.csv")
    output_file = os.path.join(base_dir, "customer_behavior_cleaned.csv")

    # Execute ETL pipeline
    print("--- Starting ETL Pipeline ---")
    data = extract(input_file)
    
    if data is not None:
        transformed_data = transform(data)
        load(transformed_data, output_file)
    print("--- ETL Pipeline Finished ---")

if __name__ == "__main__":
    run_etl()

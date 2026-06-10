import pandas as pd
import numpy as np

def clean_data():
    input_file = "customer_behavior_dataset.csv"
    output_file = "customer_behaviour_dataset_finalmax.csv"
    
    print(f"Reading {input_file}...")
    df = pd.read_csv(input_file)
    original_shape = df.shape
    print(f"Original shape: {original_shape}")
    
    # 1. Filter out invalid rows:
    # - Year_Birth >= 1930 (exclude invalid birth years like 1893, 1899, 1900)
    # We must handle NaN in Year_Birth if any, but Year_Birth has no nulls in original.
    df = df[df['Year_Birth'] >= 1930]
    
    # - Income >= 0 (exclude negative income)
    # Since Income has nulls, we keep nulls for now (so they can be imputed) and only drop rows where Income is negative.
    df = df[(df['Income'].isna()) | (df['Income'] >= 0)]
    
    # - Expenses >= 0 (exclude negative expenses in any of the expense columns)
    gastos_cols = ["MntWines", "MntFruits", "MntMeatProducts", "MntFishProducts", "MntSweetProducts", "MntGoldProds"]
    for col in gastos_cols:
        df = df[(df[col].isna()) | (df[col] >= 0)]
        
    # - Purchases >= 0 (exclude negative purchases)
    compras_cols = ["NumDealsPurchases", "NumWebPurchases", "NumCatalogPurchases", "NumStorePurchases"]
    for col in compras_cols:
        df = df[(df[col].isna()) | (df[col] >= 0)]
        
    print(f"Shape after filtering invalid rows: {df.shape}")
    
    # 2. Impute missing values (nulls) as recommended in the ETL guide:
    # - Fill numerical columns with their median
    num_cols = df.select_dtypes(include=[np.number]).columns
    for col in num_cols:
        if df[col].isnull().sum() > 0:
            median_val = df[col].median()
            df[col] = df[col].fillna(median_val)
            print(f"Imputed missing values in numerical column '{col}' with median: {median_val}")
            
    # - Fill categorical columns with their mode
    cat_cols = df.select_dtypes(include=['object']).columns
    for col in cat_cols:
        if df[col].isnull().sum() > 0:
            mode_val = df[col].mode()[0]
            df[col] = df[col].fillna(mode_val)
            print(f"Imputed missing values in categorical column '{col}' with mode: {mode_val}")
            
    # 3. Rename columns as done in massi.py:
    nombres_columnas = {
        'AcceptedCmp1': 'Campaña 1',
        'AcceptedCmp2': 'Campaña 2',
        'AcceptedCmp3': 'Campaña 3',
        'AcceptedCmp4': 'Campaña 4',
        'AcceptedCmp5': 'Campaña 5'
    }
    df.rename(columns=nombres_columnas, inplace=True)
    print("Renamed campaign columns.")
    
    # 4. Drop unnecessary/constant columns:
    # Z_CostContact and Z_Revenue are constant (always 3 and 11) and contain no useful information
    df.drop(columns=['Z_CostContact', 'Z_Revenue'], errors='ignore', inplace=True)
    print("Dropped constant columns Z_CostContact and Z_Revenue.")
    
    # 5. Check and remove duplicates:
    duplicados = df.duplicated().sum()
    if duplicados > 0:
        df.drop_duplicates(inplace=True)
        print(f"Removed {duplicados} duplicate rows.")
    
    # Save the cleaned dataset
    df.to_csv(output_file, index=False)
    print(f"Cleaned dataset saved successfully to {output_file}. Shape: {df.shape}")

if __name__ == "__main__":
    clean_data()

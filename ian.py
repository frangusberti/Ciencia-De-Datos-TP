import pandas as pd
import numpy as np
from datetime import datetime

# Cargar el dataset original
df = pd.read_csv("customer_behavior_dataset.csv")

# CREAMOS LA COPIA PARA NO ALTERAR EL ORIGINAL
df_copia = df.copy()

print("--- Análisis Inicial ---")
print(f"Dimensiones originales: {df_copia.shape}")

# 1. FORMA DISTINTA DE VER VALORES ÚNICOS Y NULOS
# En lugar de varios prints, creamos un DataFrame resumen que junta todo:
resumen = pd.DataFrame({
    'Tipo de Dato': df_copia.dtypes,
    'Valores Únicos': df_copia.nunique(),
    'Nulos Totales': df_copia.isnull().sum(),
    '% de Nulos': (df_copia.isnull().sum() / len(df_copia)) * 100
})
print("\n--- Resumen de Columnas ---")
print(resumen) 

# 2. FORMA AUTOMATIZADA DE ELIMINAR COLUMNAS CON 1 SOLO VALOR
# En lugar de poner los nombres a mano, busca y elimina columnas que no aportan info.
cols_un_valor = [col for col in df_copia.columns if df_copia[col].nunique() == 1]
print(f"\nEliminando columnas con un solo valor único: {cols_un_valor}")
df_copia = df_copia.drop(columns=cols_un_valor)

# 3. RELLENAR NULOS CON 0 PARA CIERTAS COLUMNAS
columnas_a_cero = [
    'Kidhome', 'MntMeatProducts', 'MntFishProducts', 
    'MntSweetProducts', 'NumDealsPurchases', 
    'AcceptedCmp3', 'AcceptedCmp2', 'Complain', 'Response'
]
columnas_a_cero_existentes = [col for col in columnas_a_cero if col in df_copia.columns]
df_copia[columnas_a_cero_existentes] = df_copia[columnas_a_cero_existentes].fillna(0)

# 4. ALGO ORIGINAL: IMPUTACIÓN INTELIGENTE Y CREACIÓN DE VARIABLES (Feature Engineering)
print("\n--- Aplicando transformaciones originales ---")

# a) Rellenar ingresos con la mediana
if 'Income' in df_copia.columns and df_copia['Income'].isnull().sum() > 0:
    mediana_ingreso = df_copia['Income'].median()
    df_copia['Income'] = df_copia['Income'].fillna(mediana_ingreso)
    print(f"-> Nulos en 'Income' rellenados con la mediana: {mediana_ingreso}")

# b) Crear columna Edad
if 'Year_Birth' in df_copia.columns:
    anio_actual = datetime.now().year
    df_copia['Edad'] = anio_actual - df_copia['Year_Birth']
    print("-> Nueva columna 'Edad' creada a partir de 'Year_Birth'.")

print(f"\nDimensiones finales de la copia: {df_copia.shape}")

# Guardamos la copia en un nuevo archivo CSV para mantener el original intacto
nombre_nuevo_archivo = "customer_behavior_dataset_copia.csv"
df_copia.to_csv(nombre_nuevo_archivo, index=False)
print(f"\n-> ¡Dataset modificado guardado exitosamente como '{nombre_nuevo_archivo}'!")

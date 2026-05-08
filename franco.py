import pandas as pd
import numpy as np
from datetime import datetime

# 1. EXTRACCIÓN (EXTRACT)
# Carga del dataset original
df_original = pd.read_csv(r"c:\Users\PC\OneDrive\Escritorio\CCiencia datos\customer_behavior_dataset.csv")

# Creación de una copia de trabajo para proteger los datos crudos
df = df_original.copy()

# 2. EXPLORACIÓN INICIAL
print("--- EXPLORACIÓN INICIAL ---")
print(f"Dimensiones iniciales: {df.shape}")

# Conteo de valores únicos por columna para identificar variables constantes
print("\nIdentificando variables sin variabilidad:")
for col in df.columns:
    nunique = df[col].nunique()
    if nunique <= 1:
        print(f"- {col}: {nunique} valores únicos (Constante)")

# 3. TRANSFORMACIONES (TRANSFORM)
# 3.1 Eliminación de columnas constantes que no aportan información al modelo
df = df.drop(columns=["Z_CostContact", "Z_Revenue"]) 

# 3.2 Tratamiento de valores faltantes (Nulos)
nulos_iniciales = df.isnull().sum()
print("\nValores nulos iniciales por columna:\n", nulos_iniciales[nulos_iniciales > 0])

# En las siguientes variables, los nulos representan lógicamente una cantidad de cero
columnas_a_cero = [
    'Kidhome', 'MntMeatProducts', 'MntFishProducts', 
    'MntSweetProducts', 'NumDealsPurchases', 
    'AcceptedCmp3', 'AcceptedCmp2', 'Complain', 'Response'
]
df[columnas_a_cero] = df[columnas_a_cero].fillna(0)

# Para 'Income' (Ingreso), se opta por imputar con la mediana para evitar el sesgo por ingresos atípicos muy altos
mediana_ingreso = df['Income'].median()
df['Income'] = df['Income'].fillna(mediana_ingreso)

# 3.3 Tratamiento de valores atípicos (Outliers) y Errores
# A) Eliminación de filas duplicadas
duplicados = df.duplicated().sum()
if duplicados > 0:
    df = df.drop_duplicates()
    print(f"\nSe eliminaron {duplicados} filas duplicadas.")

# B) Fechas de nacimiento irreales (ej. 1893)
# Se establece como límite el año 1930
df = df[df['Year_Birth'] >= 1930]

# C) Ingresos negativos (Error de carga)
df = df[df['Income'] >= 0]

# D) Corrección de gastos negativos (Error de carga)
columnas_gasto = ['MntWines', 'MntFruits', 'MntMeatProducts', 
                  'MntFishProducts', 'MntSweetProducts', 'MntGoldProds']
for col in columnas_gasto:
    # Se eliminan los registros con gastos menores a 0 al no tener sentido lógico
    df = df[df[col] >= 0]

# E) Valores con decimales en variables que representan números enteros
columnas_discretas = ['Recency', 'NumWebPurchases', 'NumCatalogPurchases', 'NumStorePurchases']
for col in columnas_discretas:
    # Redondeo y conversión a formato entero
    df[col] = df[col].round(0).astype(int)

# 3.4 Transformación de tipos de datos (Fechas)
# Conversión de la columna fecha de formato string a datetime para su correcta manipulación
df['Dt_Customer'] = pd.to_datetime(df['Dt_Customer'], format='%d-%m-%Y', errors='coerce')

# 3.5 Ingeniería de características (Feature Engineering)
# Creación de nuevas variables para mejorar la capacidad analítica del dataset

# A) Edad del cliente proyectada al año 2026
df['Edad'] = 2026 - df['Year_Birth']

# B) Cantidad total de hijos en el hogar
df['Total_Hijos'] = df['Kidhome'] + df['Teenhome']

# C) Gasto total acumulado por cliente
df['Gasto_Total'] = df[columnas_gasto].sum(axis=1)

# D) Cantidad total de compras
columnas_compras = ['NumDealsPurchases', 'NumWebPurchases', 
                    'NumCatalogPurchases', 'NumStorePurchases']
df['Total_Compras'] = df[columnas_compras].sum(axis=1)

# 3.6 Renombramiento de columnas para mayor claridad
df = df.rename(columns={
    'Dt_Customer': 'Fecha_Cliente',
    'Year_Birth': 'Anio_Nacimiento',
    'Kidhome': 'Ninos_Hogar',
    'Teenhome': 'Adolescentes_Hogar',
    'Recency': 'Dias_Ultima_Compra',
    'Income': 'Ingreso_Anual'
})

print(f"\nDimensiones post-limpieza: {df.shape}")

# 4. CARGA (LOAD)
# Exportación del DataFrame ya procesado
ruta_salida = r"c:\Users\PC\OneDrive\Escritorio\CCiencia datos\customer_behavior_LIMPIO.csv"
df.to_csv(ruta_salida, index=False)
print(f"\n¡Proceso ETL finalizado! Archivo guardado correctamente en:\n{ruta_salida}")
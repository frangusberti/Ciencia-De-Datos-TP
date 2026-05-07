import pandas as pd
import numpy as np
from datetime import datetime

# Cargo el original usando la ruta completa
df_original = pd.read_csv(r"c:\Users\PC\OneDrive\Escritorio\CCiencia datos\customer_behavior_dataset.csv")

# Creo una copia para trabajar así no rompo el original
df = df_original.copy()

# chusmeo cuantos valores unicos tiene cada columna
for col in df.columns:
    print(f"{col}: {df[col].nunique()} valores únicos")

# veo q las colunmas z_costcontact y z_revenue no aportan informacion ya q tienen un solo valor único
# asi q las vuelo nomas
df = df.drop(["Z_CostContact", "Z_Revenue"], axis=1) 

# Contar nulos y porcentaje
nulos = df.isnull().sum()
print("\nNulos encontrados inicialmente:\n", nulos[nulos > 0])

# veo q hay muchos valores nulos en varios datos, como kidhome, complain, acceptedcmp. 
# Llegue a la conclusion de que no son errores sino que o no tienen hijos, o no hay quejas, o aceptó 0 campañas.
# por lo tanto en lugar de eliminar, simplemente relleno los huecos con 0.
columnas_a_cero = [
    'Kidhome', 'MntMeatProducts', 'MntFishProducts', 
    'MntSweetProducts', 'NumDealsPurchases', 
    'AcceptedCmp3', 'AcceptedCmp2', 'Complain', 'Response'
]

# Rellenar todas juntas
df[columnas_a_cero] = df[columnas_a_cero].fillna(0)

# me quedaron 24 nulos colgados en Income. 
# como los sueldos pueden tener picos raros (outliers), le mando la mediana para que sea mas representativo
df['Income'] = df['Income'].fillna(df['Income'].median())

# Verificar que ya no queden nulos en el dataset
print("\nNulos despues de la limpieza:\n", df.isnull().sum()[df.isnull().sum() > 0])

# --- TRATAMIENTO DE OUTLIERS ---
# vi algunos años de nacimiento re bizarros tipo 1893 (gente de 130 años? rari). 
# vuelo a los que nacieron antes de 1930 para limpiar la mugre
df = df[df['Year_Birth'] >= 1930]

# y por las dudas me aseguro de que nadie tenga sueldo negativo porque no tiene sentido
df = df[df['Income'] >= 0]

# --- ARREGLO DE FECHAS ---
# la fecha en la que se hicieron clientes está como texto, la paso a formato datetime posta
df['Dt_Customer'] = pd.to_datetime(df['Dt_Customer'], format='%d-%m-%Y', errors='coerce')

# --- CREACION DE COLUMNAS NUEVAS (FEATURE ENGINEERING) ---
# me armo un par de columnas extra que nos van a servir para analizar mejor despues

# 1. Edad al año del tp (2026)
df['Edad'] = 2026 - df['Year_Birth']

# 2. Total de pibes en la casa (sumo los nenes y los adolescentes)
df['Total_Hijos'] = df['Kidhome'] + df['Teenhome']

# 3. Cuanta plata gastaron en total (sumo todos los Mnt)
columnas_gasto = ['MntWines', 'MntFruits', 'MntMeatProducts', 
                  'MntFishProducts', 'MntSweetProducts', 'MntGoldProds']
df['Gasto_Total'] = df[columnas_gasto].sum(axis=1)

# --- EXPORTAR ---
# ahora sí, con todo pipí cucú, lo guardo en un archivo nuevo limpio
df.to_csv(r"c:\Users\PC\OneDrive\Escritorio\CCiencia datos\customer_behavior_LIMPIO.csv", index=False)
print("\n¡Listo! Archivo limpio guardado en customer_behavior_LIMPIO.csv")
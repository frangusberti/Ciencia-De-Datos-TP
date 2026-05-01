import pandas as pd
import numpy as np
from datetime import datetime
df = pd.read_csv(r"c:\Users\PC\OneDrive\Escritorio\CCiencia datos\customer_behavior_dataset.csv")
# Cargo el original
df_original = pd.read_csv("customer_behavior_dataset.csv")
# Creo una copia para trabajar
df = df_original.copy()
#  Guardar en un archivo nuevo
df.to_csv("customer_behavior_LIMPIO.csv", index=False)
# df.to_csv("customer_behavior_dataset.csv", index=False)
# busco cuantos valores unicos tiene cada columna
for col in df.columns:
    print(f"{col}: {df[col].nunique()} valores únicos")
# veo q las colunmas z_costcontact y z_revenue no aportan informacion ya q tienen un solo valorЕ único
# asi q lo tanto los elimino
df = df.drop(["Z_CostContact", "Z_Revenue"], axis=1) 
# Contar nulos y porcentaje
nulos = df.isnull().sum()
porcentaje = (nulos / len(df)) * 100
print(nulos[nulos > 0])
# veo q hay muchos valores nulos en varios datos, como kidhome, complain, acceptedcmp, por lo tanto no significan errores sino que o no tienen hijos, o no hay quejas, o acepto 0 camapañas. por lo tanto en lugar de eliminar, simplemente relleno con 0.
# Lista de columnas q vamos a rellenar con 0
columnas_a_cero = [
    'Kidhome', 'MntMeatProducts', 'MntFishProducts', 
    'MntSweetProducts', 'NumDealsPurchases', 
    'AcceptedCmp3', 'AcceptedCmp2', 'Complain', 'Response'
]
# Rellenar todas juntas
df[columnas_a_cero] = df[columnas_a_cero].fillna(0)
# Verificar que ya no queden nulos en esas
print(df[columnas_a_cero].isnull().sum())
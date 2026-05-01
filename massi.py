import pandas as pd
import numpy as np
from datetime import datetime
df = pd.read_csv("/Users/maximarissop/Desktop/Ciencia de Datos/Ciencia-De-Datos-TP/customer_behavior_dataset.csv")
nulos = df.isnull().sum()
print(nulos[nulos > 0])
#hasta ahora programe para que cuente valores que faltan en por columna, podria ver el porcentaje de valores nulos si quiero pero me parece medio innecesario
#veo que hago con esos valores nulos pq hay algunas categorias que tienen muchos valores nulos y otras no tantos
#me trato de sacar de encima valores extraños (ejs: años y sueldos negativos)
print(df.describe())
#se detectan esos valores atipicos observando el minimo y el maxixmo valor de las columnas
#Pueden emplearse conceptos de Probabilidad y Estadistica (Teorema Central del Limite) para ver si los valores de las columnas pertenecen o no al rango especificado
#pruebo detectar valores atipicos para la columna de year_birth, tengo que definir que son los outliers

# Detección automática de outliers usando el método estadístico de Rango Intercuartílico (IQR)
# Esto sirve para TODAS las columnas numéricas sin tener que hacer una por una.

print("\n--- DETECCIÓN AUTOMÁTICA DE OUTLIERS (MÉTODO IQR) ---")

# Seleccionamos solo las columnas numéricas para poder calcular cuartiles
columnas_numericas = df.select_dtypes(include=[np.number]).columns

for columna in columnas_numericas:
    # Si la columna es el ID u otra categórica codificada, la saltamos porque no tiene sentido buscar outliers ahí
    if columna in ['ID', 'Z_CostContact', 'Z_Revenue', 'Response', 'AcceptedCmp1', 'AcceptedCmp2', 'AcceptedCmp3', 'AcceptedCmp4', 'AcceptedCmp5', 'Complain']:
        continue
        
    Q1 = df[columna].quantile(0.25)
    Q3 = df[columna].quantile(0.75)
    IQR = Q3 - Q1
    
    limite_inferior = Q1 - 1.5 * IQR
    limite_superior = Q3 + 1.5 * IQR
    
    # Filtramos los valores que se salen de los límites
    outliers = df[(df[columna] < limite_inferior) | (df[columna] > limite_superior)]
    
    # Solo imprimimos si encontró algún valor atípico
    if len(outliers) > 0:
        print(f"\nColumna: {columna}")
        print(f"Límites normales: [{limite_inferior:.2f}, {limite_superior:.2f}]")
        print(f"Cantidad de outliers encontrados: {len(outliers)}")

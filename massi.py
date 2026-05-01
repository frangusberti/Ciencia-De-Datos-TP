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

#pruebo detectar valores atipicos para la columna de year_birth, tengo que definir que son los outliers en cada caso
#mas facil puede ser sin usar conceptos de PyE, lo hago directamente con definiciones y (longitud de cadena?) pero ahi tendria que hacer uno por uno creo asi que mejor usar PyE



import pandas as pd
import numpy as np
from datetime import datetime
df = pd.read_csv(r"c:\Users\PC\OneDrive\Escritorio\CCiencia datos\customer_behavior_dataset.csv")
nulos = df.isnull().sum()
print(nulos[nulos > 0]) 
porcentaje_nulos = (df.isnull().sum() / len(df)) * 100
print(porcentaje_nulos[porcentaje_nulos > 0].round(2))  
import pandas as pd
import numpy as np
from datetime import datetime
df = pd.read_csv("/Users/maximarissop/Desktop/Ciencia de Datos/Ciencia-De-Datos-TP/customer_behavior_dataset.csv")
nulos = df.isnull().sum()
print(nulos[nulos > 0])
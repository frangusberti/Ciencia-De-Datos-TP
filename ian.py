import pandas as pd
import numpy as np
from datetime import datetime

df=pd.read_csv("customer_behavior_dataset.csv")
print(df.head())
print(f"Dimensiones: {df.shape}")

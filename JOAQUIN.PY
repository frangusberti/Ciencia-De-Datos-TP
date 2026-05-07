import pandas as pd
import numpy as np
from datetime import datetime
import os
base_dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(base_dir, "customer_behavior_dataset.csv"))
print(df.head())

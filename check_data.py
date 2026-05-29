# check_data.py
import pandas as pd

df = pd.read_csv("vsl_data.csv", header=None)
print(df[0].value_counts())
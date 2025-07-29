import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

df=pd.read_csv('FinalTable.csv')

# print(df.info())
# print(df.columns)
# print(df.describe)

df["statusTimestamp"] = df["statusTimestamp"].astype(str)
df["statusTimestamp"] = pd.to_datetime(df["statusTimestamp"], format="%Y%m%d%H%M%S.%f", errors="coerce")

df["pollerFetchTime"] = pd.to_datetime(df["pollerFetchTime"], unit="ms", errors="coerce")
# print(df.head())

# print(df.duplicated().sum())
# print(df.duplicated(subset=["VIN", "statusTimestamp"]).sum())

df2=df.sort_values(by='statusTimestamp')

df2["odometer_diff"] = df2["odometer"].diff()
df2["time_diff"] = df2["statusTimestamp"].diff()

# for col in ["odometer", "speed", "gasLevel"]:
#     sns.histplot(df[col], kde=True)
#     plt.title(f"Distribution of {col}")
#     plt.show()

sns.heatmap(df[["odometer", "speed", "gasLevel"]].corr(), annot=True, cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.show()

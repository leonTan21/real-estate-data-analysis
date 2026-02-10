import pandas as pd

data = pd.read_csv("data/realtor.csv")
print(data.info())
print(data.describe())
print(data.head())

print(data.drop_duplicates())
print(data.isna())
expensive_houses = data[~(data['price'] <= 50000)]
print(expensive_houses.info())
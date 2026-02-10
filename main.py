import pandas as pd
from io import StringIO
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv("data/realtor.csv")

file_path = "output.txt"
content = ""

data.info()
data.describe(include="all")
data.head()
data.drop_duplicates()
data.isna().sum()
expensive_houses = data[data['price'] > 50000]

Q1 = data['price'].quantile(0.25)
Q3 = data['price'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

data_no_outliers = data[(data['price'] >= lower_bound) & (data['price'] <= upper_bound)]
print("Original data shape:", data.shape)
print("Data shape after removing outliers:", data_no_outliers.shape)
print(data_no_outliers['price'].describe())

missing_percentage = data_no_outliers['price'].isna().mean() * 100
print(f"Percentage of missing values in price: {missing_percentage:.2f}%")

data_no_outliers = data_no_outliers.dropna(subset=['price'])

#Histogram
plt.figure(figsize=(10,5))
sns.histplot(data_no_outliers['price'], bins=50, kde=True)
plt.title("Histogram of House Prices")
plt.xlabel("Price")
plt.ylabel("Frequency")
plt.savefig("histogram_price.png")  # saves plot as image

# Boxplot
plt.figure(figsize=(10,3))
sns.boxplot(x=data_no_outliers['price'])
plt.title("Boxplot of House Prices")
plt.xlabel("Price")
plt.savefig("boxplot_price.png")  # saves plot as image

# Convert to datetime
data_no_outliers['sold_date'] = pd.to_datetime(data_no_outliers['sold_date'], errors='coerce')

# Check for any parsing errors
print(data_no_outliers['sold_date'].isna().sum(), "missing after conversion")

data_no_outliers['sold_year'] = data_no_outliers['sold_date'].dt.year
data_no_outliers['sold_month'] = data_no_outliers['sold_date'].dt.month
print(data_no_outliers[['sold_date', 'sold_year', 'sold_month']].head())

state_counts = data_no_outliers['state'].value_counts()
print("Observations per state:\n", state_counts)
# Keep only states with more than 1 observation
states_to_keep = state_counts[state_counts > 1].index
data_filtered = data_no_outliers[data_no_outliers['state'].isin(states_to_keep)]
# Check counts again
new_state_counts = data_filtered['state'].value_counts()
print("Observations per state after removing singletons:\n", new_state_counts)

with open("output.txt", "a") as file:
    # Capture info
    buffer = StringIO()
    data_no_outliers.info(buf=buffer)
    file.write("Data Info:\n" + buffer.getvalue() + "\n\n")

    # Describe
    file.write("Summary Statistics:\n" + str(data_no_outliers.describe()) + "\n\n")

    # Head
    file.write("First 5 Rows:\n" + str(data_no_outliers.head()) + "\n\n")

    # Missing price %
    missing_percentage = data_no_outliers['price'].isna().mean() * 100
    file.write(f"Percentage of missing values in price: {missing_percentage:.2f}%\n\n")

    # Sold year/month preview
    file.write("Sold date info:\n" + str(data_no_outliers[['sold_date', 'sold_year', 'sold_month']].head()) + "\n\n")
    file.write("Visualizations saved as:\n")
    file.write("1. histogram_price.png\n")
    file.write("2. boxplot_price.png\n")
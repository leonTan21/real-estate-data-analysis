import pandas as pd
from io import StringIO
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv("data/realtor.csv")
file_path = "output.txt"
content = ""

def view_data():
    data.info()
    data.describe(include="all")
    data.head()

def del_duplicates():
    data.drop_duplicates()
    data.info()

def na_count():
    print(data.isna().sum())

def price_gauge(data):
    return data[data['price'] > 50000]

def del_outliers(data):
    q = data['price'].quantile([0.25, 0.5, 0.75])
    iqr = q.loc[0.75] - q.loc[0.25]
    left = q.loc[0.25] - 1.5 * iqr
    right = q.loc[0.75] + 1.5 * iqr
    return (data['price'] < left) | (data['price'] > right)

def na_percentage():
    missing_percentage = data['price'].isna().mean() * 100
    print(f"Percentage of missing values in price: {missing_percentage:.2f}%")
    data.dropna(subset=['price'])

# Convert to datetime
def convert_datetime():
    data['sold_date'] = pd.to_datetime(data['sold_date'], errors='coerce')
    # Check for any parsing errors
    print(data['sold_date'].isna().sum(), "missing after conversion")
    data['sold_year'] = data['sold_date'].dt.year
    data['sold_month'] = data['sold_date'].dt.month
    print(data[['sold_date', 'sold_year', 'sold_month']].head())

def state_count():
    state_counts = data['state'].value_counts()
    print("Observations per state:\n", state_counts)
    states_to_keep = state_counts[state_counts > 1].index
    data_filtered = data[data['state'].isin(states_to_keep)]
    new_state_counts = data_filtered['state'].value_counts()
    print("Observations per state after removing singletons:\n", new_state_counts)

def save_output():
    with open("output.txt", "a") as file:
        # Capture info
        buffer = StringIO()
        data.info(buf=buffer)
        file.write("Data Info:\n" + buffer.getvalue() + "\n\n")

        # Describe
        file.write("Summary Statistics:\n" + str(data.describe()) + "\n\n")

        # Head
        file.write("First 5 Rows:\n" + str(data.head()) + "\n\n")

        # Missing price %
        missing_percentage = data['price'].isna().mean() * 100
        file.write(f"Percentage of missing values in price: {missing_percentage:.2f}%\n\n")

        # Sold year/month preview
        file.write("Sold date info:\n" + str(data[['sold_date', 'sold_year', 'sold_month']].head()) + "\n\n")
        file.write("Visualizations saved as:\n")
        file.write("1. histogram_price.png\n")
        file.write("2. boxplot_price.png\n")

view_data()
del_duplicates()
na_count()
data = price_gauge(data)
data = data[~del_outliers(data)]
na_percentage()
convert_datetime()
state_count()

#Histogram
plt.figure(figsize=(10,5))
sns.histplot(data['price'], bins=50, kde=True)
plt.title("Histogram of House Prices")
plt.xlabel("Price")
plt.ylabel("Frequency")
plt.savefig("histogram_price.png")

# Boxplot
plt.figure(figsize=(10,3))
sns.boxplot(x=data['price'])
plt.title("Boxplot of House Prices")
plt.xlabel("Price")
plt.savefig("boxplot_price.png")

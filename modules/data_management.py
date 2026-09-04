import pandas as pd

# Step 1: Load the dataset
df = pd.read_csv("data/covid_data.csv")

# Step 2: Check dataset shape
print("Dataset Shape:")
print(df.shape)

# Step 3: Check column names
print("\nColumn Names:")
print(df.columns)

# Step 4: Check data types
print("\nData Types:")
print(df.dtypes)

# Step 5: Convert Date column to datetime
df["Date"] = pd.to_datetime(df["Date"])

# Step 6: Check missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Step 7: Handle missing Province/State values
df["Province/State"] = df["Province/State"].fillna("Unknown")

# Step 8: Investigate missing Recovered values
print("\nCountries with Missing Recovered Values:")
print(df[df["Recovered"].isnull()]["Country/Region"].unique())

# Step 9: Handle missing Recovered values
df["Recovered"] = df["Recovered"].fillna(0)

# Step 10: Check duplicate rows
print("\nDuplicate Rows:")
print(df.duplicated().sum())

# Step 11: Check for negative values
print("\nNegative Confirmed Values:")
print((df["Confirmed"] < 0).sum())

print("Negative Recovered Values:")
print((df["Recovered"] < 0).sum())

print("Negative Death Values:")
print((df["Deaths"] < 0).sum())

# Step 12: Check date range
print("\nDate Range:")
print("Earliest Date:", df["Date"].min())
print("Latest Date:", df["Date"].max())

# Step 13: Check number of unique countries
print("\nNumber of Unique Countries/Regions:")
print(df["Country/Region"].nunique())

# Step 14: Display first five rows
print("\nFirst Five Rows:")
print(df.head())

# Step 15: Verify final data types
print("\nFinal Data Types:")
print(df.dtypes)

# Step 16: Statistical summary
print("\nStatistical Summary:")
print(df.describe())

# Step 17: Save cleaned dataset
df.to_csv("data/cleaned_covid_data.csv", index=False)

print("\nCleaned dataset saved successfully!")
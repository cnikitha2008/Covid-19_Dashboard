import pandas as pd


# Load the raw COVID-19 dataset
df = pd.read_csv("data/covid_data.csv")

print("COVID-19 DATA MANAGEMENT MODULE")

print("\n1. DATA LOADING")
print("Dataset loaded successfully.")

# Display the shape of the dataset
print("\n2. DATA INSPECTION")

print("\nDataset Shape:")
print(df.shape)

# Display the column names
print("\nColumn Names:")
print(df.columns)

# Display the data types of all columns
print("\nData Types Before Cleaning:")
print(df.dtypes)

# Convert Date column from string to datetime
df["Date"] = pd.to_datetime(df["Date"])

print("\nDate column converted from string to datetime.")

print("\nData Types After Date Conversion:")
print(df.dtypes)

# Find missing values in each column
print("\n3. MISSING VALUE ANALYSIS")

print("\nMissing Values Before Cleaning:")
print(df.isnull().sum())

# Display the first five records where Province/State is missing
print("\nFirst Five Records with Missing Province/State:")
print(df[df["Province/State"].isnull()].head())

# Replace missing Province/State values with Unknown
df["Province/State"] = df["Province/State"].fillna("Unknown")

print("\nMissing Province/State values handled.")

print("\nMissing Values After Province/State Cleaning:")
print(df.isnull().sum())

# Find the number of countries having missing Recovered values
missing_recovered_countries = df[
    df["Recovered"].isnull()
]["Country/Region"].unique()

print("\nNumber of Countries with Missing Recovered Values:")
print(len(missing_recovered_countries))

print("\nCountries with Missing Recovered Values:")
print(missing_recovered_countries)

# Display the first five records where Recovered is missing
print("\nFirst Five Records with Missing Recovered Values:")
print(df[df["Recovered"].isnull()].head())

# Replace missing Recovered values with zero
df["Recovered"] = df["Recovered"].fillna(0)

print("\nMissing Recovered values handled.")

print("\nMissing Values After Cleaning:")
print(df.isnull().sum())

# Check duplicate records
print("\n4. DATA VALIDATION")

print("\nDuplicate Rows:")
print(df.duplicated().sum())

# Check negative Confirmed values
print("\nNegative Confirmed Values:")
print((df["Confirmed"] < 0).sum())

# Check negative Recovered values
print("\nNegative Recovered Values:")
print((df["Recovered"] < 0).sum())

# Check negative Death values
print("\nNegative Death Values:")
print((df["Deaths"] < 0).sum())

# Display the earliest date
print("\nEarliest Date:")
print(df["Date"].min())

# Display the latest date
print("\nLatest Date:")
print(df["Date"].max())

# Display all unique countries
print("\nUnique Countries/Regions:")
print(df["Country/Region"].unique())

# Display the number of unique countries
print("\nNumber of Unique Countries/Regions:")
print(df["Country/Region"].nunique())

# Display the first five records after cleaning
print("\n5. FINAL DATA INSPECTION")

print("\nFirst Five Rows of Cleaned Data:")
print(df.head())

# Display statistical summary
print("\nStatistical Summary:")
print(df.describe())

# Save the cleaned dataset
df.to_csv("data/cleaned_covid_data.csv", index=False)

print("\n6. CLEANED DATASET")

print("Cleaned dataset saved successfully.")
print("File: data/cleaned_covid_data.csv")

print("\nModule 1 Data Management Completed Successfully.")
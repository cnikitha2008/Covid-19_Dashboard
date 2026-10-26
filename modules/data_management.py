import numpy as np
import pandas as pd


# ==============================================================================
# REUSABLE FUNCTIONS FOR DATA MANAGEMENT (MODULE 1)
# ==============================================================================

def load_raw_data(filepath="data/covid_data.csv"):
    """Load the raw COVID-19 dataset from CSV."""
    return pd.read_csv(filepath)


def clean_covid_data(df, assumption_rate=0.80):
    """
    Clean and preprocess the COVID-19 dataset:
    - Converts Date column to datetime
    - Fills missing Province/State values with 'Unknown'
    - Fills missing Recovered values or estimates them using assumption rate
    - Computes Active cases (Confirmed - Recovered - Deaths)
    - Sorts records chronologically by Date and Country/Region
    """
    df = df.copy()

    # Convert Date column from string to datetime
    df["Date"] = pd.to_datetime(df["Date"])

    # Handle missing Province/State values
    if "Province/State" not in df.columns:
        df["Province/State"] = "Unknown"
    df["Province/State"] = df["Province/State"].fillna("Unknown")

    # Handle missing Recovered values
    if "Recovered" not in df.columns:
        df["Recovered"] = np.nan
    df["Recovered"] = df["Recovered"].fillna(0)

    # Apply recovery assumption where recovery is 0 or missing
    missing_recovery = df["Recovered"] == 0
    df.loc[missing_recovery, "Recovered"] = df.loc[missing_recovery, "Confirmed"] * assumption_rate

    # Ensure Recovered never exceeds Confirmed and is never negative
    df["Recovered"] = np.where(df["Recovered"] > df["Confirmed"], df["Confirmed"], df["Recovered"])
    df["Recovered"] = np.where(df["Recovered"] < 0, 0, df["Recovered"])

    # Calculate Active cases
    df["Active"] = df["Confirmed"] - df["Recovered"] - df["Deaths"]

    # Sort values chronologically and by Country
    df = df.sort_values(by=["Date", "Country/Region"])

    return df


def load_and_clean_data(cleaned_path="data/cleaned_covid_data.csv", raw_path="data/covid_data.csv"):
    """
    Load data from cleaned CSV if available, otherwise fallback to raw CSV,
    clean the data, and return the cleaned DataFrame.
    """
    try:
        df = pd.read_csv(cleaned_path)
    except Exception:
        df = pd.read_csv(raw_path)

    return clean_covid_data(df)


# ==============================================================================
# STANDALONE CLI DEMONSTRATION
# ==============================================================================

def run_standalone_demo():
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


if __name__ == "__main__":
    run_standalone_demo()
import pandas as pd
import matplotlib.pyplot as plt


# Load the cleaned COVID-19 dataset
df = pd.read_csv("data/cleaned_covid_data.csv")

# Convert Date column to datetime
df["Date"] = pd.to_datetime(df["Date"])

print("WORLDWIDE COVID-19 ANALYSIS MODULE")

print("\n1. DATA LOADING")
print("Cleaned dataset loaded successfully.")

# Find the latest available date
latest_date = df["Date"].max()

print("\n2. LATEST DATE")
print("Latest available date:")
print(latest_date)

# Select records from the latest date
latest_data = df[df["Date"] == latest_date]

print("\nNumber of records on latest date:")
print(len(latest_data))

# Calculate worldwide totals
worldwide_confirmed = latest_data["Confirmed"].sum()
worldwide_recovered = latest_data["Recovered"].sum()
worldwide_deaths = latest_data["Deaths"].sum()

# Check whether recovered cases are available
recovered_available = latest_data["Recovered"].sum() > 0

# Calculate active cases only when recovered data is available
if recovered_available:
    worldwide_active = (
        worldwide_confirmed
        - worldwide_recovered
        - worldwide_deaths
    )
else:
    worldwide_active = None

print("\n3. WORLDWIDE COVID-19 STATISTICS")

print("\nTotal Confirmed Cases:")
print(worldwide_confirmed)

print("\nTotal Recovered Cases:")

if recovered_available:
    print(worldwide_recovered)
else:
    print("Not available for latest date")

print("\nTotal Deaths:")
print(worldwide_deaths)

print("\nTotal Active Cases:")

if worldwide_active is not None:
    print(worldwide_active)
else:
    print("Not available because recovered cases are unavailable")

# Group latest data by country
country_data = latest_data.groupby("Country/Region")[
    ["Confirmed", "Recovered", "Deaths"]
].sum()

# Calculate active cases for each country only when recovered data is available
if recovered_available:
    country_data["Active"] = (
        country_data["Confirmed"]
        - country_data["Recovered"]
        - country_data["Deaths"]
    )

print("\n4. TOP COUNTRIES BY CONFIRMED CASES")

top_confirmed = country_data.sort_values(
    "Confirmed",
    ascending=False
).head(10)

print(top_confirmed[["Confirmed"]])

print("\n5. TOP COUNTRIES BY DEATHS")

top_deaths = country_data.sort_values(
    "Deaths",
    ascending=False
).head(10)

print(top_deaths[["Deaths"]])

# Prepare worldwide daily totals
daily_data = df.groupby("Date")[
    ["Confirmed", "Recovered", "Deaths"]
].sum()

# Calculate worldwide daily active cases only where recovered data is available
daily_data["Active"] = (
    daily_data["Confirmed"]
    - daily_data["Recovered"]
    - daily_data["Deaths"]
)

print("\n6. WORLDWIDE TREND DATA")

print("\nFirst five records:")
print(daily_data.head())

print("\nLast five records:")
print(daily_data.tail())

# Worldwide confirmed cases trend
plt.figure(figsize=(10, 5))

plt.plot(
    daily_data.index,
    daily_data["Confirmed"]
)

plt.title("Worldwide Confirmed COVID-19 Cases")
plt.xlabel("Date")
plt.ylabel("Confirmed Cases")

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Worldwide deaths trend
plt.figure(figsize=(10, 5))

plt.plot(
    daily_data.index,
    daily_data["Deaths"]
)

plt.title("Worldwide COVID-19 Deaths")
plt.xlabel("Date")
plt.ylabel("Deaths")

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Top 10 countries by confirmed cases
plt.figure(figsize=(10, 5))

plt.bar(
    top_confirmed.index,
    top_confirmed["Confirmed"]
)

plt.title("Top 10 Countries by Confirmed COVID-19 Cases")
plt.xlabel("Country/Region")
plt.ylabel("Confirmed Cases")

plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()

print("\n7. WORLDWIDE ANALYSIS COMPLETED")
print("Worldwide analysis generated successfully.")
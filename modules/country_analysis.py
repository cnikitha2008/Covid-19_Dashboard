import pandas as pd
import matplotlib.pyplot as plt


# Load the cleaned COVID-19 dataset
df = pd.read_csv("data/cleaned_covid_data.csv")

# Convert Date column to datetime
df["Date"] = pd.to_datetime(df["Date"])

print("COUNTRY COVID-19 ANALYSIS MODULE")

print("\n1. DATA LOADING")
print("Cleaned dataset loaded successfully.")

countries = sorted(df["Country/Region"].unique())

print("\n2. AVAILABLE COUNTRIES")
print("Total number of countries:")
print(len(countries))

print("\nCountry List:")
print(countries)

country = input("\nEnter country name: ").strip()

if country not in countries:
    print("\nInvalid country name.")
else:
    country_data = df[df["Country/Region"] == country].copy()

    print("\n3. SELECTED COUNTRY")
    print("Country:")
    print(country)

    latest_date = country_data["Date"].max()

    print("\n4. LATEST DATE")
    print("Latest available date:")
    print(latest_date)

    latest_data = country_data[
        country_data["Date"] == latest_date
    ]

    confirmed = latest_data["Confirmed"].sum()
    recovered = latest_data["Recovered"].sum()
    deaths = latest_data["Deaths"].sum()

    recovered_available = latest_data["Recovered"].sum() > 0

    if recovered_available:
        active = confirmed - recovered - deaths
    else:
        active = None

    print("\n5. COUNTRY COVID-19 STATISTICS")

    print("\nTotal Confirmed Cases:")
    print(confirmed)

    print("\nTotal Recovered Cases:")

    if recovered_available:
        print(recovered)
    else:
        print("Not available for latest date")

    print("\nTotal Deaths:")
    print(deaths)

    print("\nTotal Active Cases:")

    if active is not None:
        print(active)
    else:
        print("Not available because recovered cases are unavailable")

    print("\n6. COUNTRY TIME-SERIES DATA")

    daily_data = country_data.groupby("Date")[
        ["Confirmed", "Recovered", "Deaths"]
    ].sum()

    daily_data["Active"] = (
        daily_data["Confirmed"]
        - daily_data["Recovered"]
        - daily_data["Deaths"]
    )

    print("\nFirst five records:")
    print(daily_data.head())

    print("\nLast five records:")
    print(daily_data.tail())

    print("\n7. COUNTRY STATISTICAL SUMMARY")

    print(daily_data.describe())

    print("\n8. COUNTRY TREND CHART")

    plt.figure(figsize=(10, 5))

    plt.plot(
        daily_data.index,
        daily_data["Confirmed"],
        label="Confirmed"
    )

    plt.plot(
        daily_data.index,
        daily_data["Recovered"],
        label="Recovered"
    )

    plt.plot(
        daily_data.index,
        daily_data["Deaths"],
        label="Deaths"
    )

    plt.plot(
        daily_data.index,
        daily_data["Active"],
        label="Active"
    )

    plt.title("COVID-19 Trend for " + country)
    plt.xlabel("Date")
    plt.ylabel("Cases")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    print("\n9. CASE DISTRIBUTION")

    if recovered_available:
        categories = [
            "Confirmed",
            "Recovered",
            "Deaths",
            "Active"
        ]

        values = [
            confirmed,
            recovered,
            deaths,
            active
        ]

        plt.figure(figsize=(8, 5))

        plt.bar(
            categories,
            values
        )

        plt.title("COVID-19 Case Distribution for " + country)
        plt.xlabel("Case Type")
        plt.ylabel("Number of Cases")
        plt.tight_layout()
        plt.show()

    else:
        categories = [
            "Confirmed",
            "Deaths"
        ]

        values = [
            confirmed,
            deaths
        ]

        plt.figure(figsize=(8, 5))

        plt.bar(
            categories,
            values
        )

        plt.title(
            "COVID-19 Case Distribution for "
            + country
            + " (Available Latest Data)"
        )

        plt.xlabel("Case Type")
        plt.ylabel("Number of Cases")
        plt.tight_layout()
        plt.show()

        print("\nRecovered and Active cases are not included")
        print("because recovered data is unavailable for the latest date.")

    print("\n10. COUNTRY DATA TABLE")

    print(daily_data)

    print("\n11. COUNTRY ANALYSIS COMPLETED")
    print("Country analysis generated successfully.")
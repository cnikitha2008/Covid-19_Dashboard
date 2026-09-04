import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/cleaned_covid_data.csv")
df["Date"] = pd.to_datetime(df["Date"])

print("COVID-19 COMPARISON AND TRENDS MODULE")

print("\n1. DATA LOADING")
print("Cleaned dataset loaded successfully.")

countries = sorted(df["Country/Region"].unique())

print("\n2. AVAILABLE COUNTRIES")
print("Total number of countries:")
print(len(countries))

print("\nCountry List:")
print(countries)

country1 = input("\nEnter first country: ").strip()
country2 = input("Enter second country: ").strip()

if country1 not in countries or country2 not in countries:

    print("\nInvalid country name.")

else:

    data1 = df[df["Country/Region"] == country1].copy()
    data2 = df[df["Country/Region"] == country2].copy()

    latest_date1 = data1["Date"].max()
    latest_date2 = data2["Date"].max()

    latest_data1 = data1[
        data1["Date"] == latest_date1
    ]

    latest_data2 = data2[
        data2["Date"] == latest_date2
    ]

    confirmed1 = latest_data1["Confirmed"].sum()
    recovered1 = latest_data1["Recovered"].sum()
    deaths1 = latest_data1["Deaths"].sum()

    confirmed2 = latest_data2["Confirmed"].sum()
    recovered2 = latest_data2["Recovered"].sum()
    deaths2 = latest_data2["Deaths"].sum()

    recovered_available1 = recovered1 > 0
    recovered_available2 = recovered2 > 0

    if recovered_available1:
        active1 = confirmed1 - recovered1 - deaths1
    else:
        active1 = None

    if recovered_available2:
        active2 = confirmed2 - recovered2 - deaths2
    else:
        active2 = None

    print("\n3. SELECTED COUNTRIES")

    print("\nCountry 1:")
    print(country1)

    print("\nCountry 2:")
    print(country2)

    print("\n4. LATEST AVAILABLE DATES")

    print("\n" + country1 + ":")
    print(latest_date1)

    print("\n" + country2 + ":")
    print(latest_date2)

    print("\n5. COUNTRY COMPARISON")

    print("\n" + country1)

    print("Confirmed Cases:")
    print(confirmed1)

    print("Recovered Cases:")

    if recovered_available1:
        print(recovered1)
    else:
        print("Not available for latest date")

    print("Deaths:")
    print(deaths1)

    print("Active Cases:")

    if active1 is not None:
        print(active1)
    else:
        print("Not available because recovered cases are unavailable")

    print("\n" + country2)

    print("Confirmed Cases:")
    print(confirmed2)

    print("Recovered Cases:")

    if recovered_available2:
        print(recovered2)
    else:
        print("Not available for latest date")

    print("Deaths:")
    print(deaths2)

    print("Active Cases:")

    if active2 is not None:
        print(active2)
    else:
        print("Not available because recovered cases are unavailable")

    print("\n6. COMPARISON TABLE")

    recovered_value1 = recovered1 if recovered_available1 else "Not Available"
    recovered_value2 = recovered2 if recovered_available2 else "Not Available"

    comparison_data = {
        "Country": [
            country1,
            country2
        ],
        "Confirmed": [
            confirmed1,
            confirmed2
        ],
        "Recovered": [
            recovered_value1,
            recovered_value2
        ],
        "Deaths": [
            deaths1,
            deaths2
        ]
    }

    comparison_df = pd.DataFrame(comparison_data)

    print(comparison_df)

    print("\n7. TIME-SERIES DATA")

    daily1 = data1.groupby("Date")[
        ["Confirmed", "Recovered", "Deaths"]
    ].sum()

    daily2 = data2.groupby("Date")[
        ["Confirmed", "Recovered", "Deaths"]
    ].sum()

    daily1["Active"] = (
        daily1["Confirmed"]
        - daily1["Recovered"]
        - daily1["Deaths"]
    )

    daily2["Active"] = (
        daily2["Confirmed"]
        - daily2["Recovered"]
        - daily2["Deaths"]
    )

    print("\n" + country1 + " First Five Records:")
    print(daily1.head())

    print("\n" + country1 + " Last Five Records:")
    print(daily1.tail())

    print("\n" + country2 + " First Five Records:")
    print(daily2.head())

    print("\n" + country2 + " Last Five Records:")
    print(daily2.tail())

    print("\n8. STATISTICAL SUMMARY")

    print("\nStatistics for " + country1)
    print(daily1.describe())

    print("\nStatistics for " + country2)
    print(daily2.describe())

    print("\n9. CONFIRMED CASE COMPARISON")

    plt.figure(figsize=(10, 5))

    plt.bar(
        [country1, country2],
        [confirmed1, confirmed2]
    )

    plt.title("Confirmed COVID-19 Cases Comparison")
    plt.xlabel("Country")
    plt.ylabel("Confirmed Cases")
    plt.tight_layout()
    plt.show()

    print("\n10. DEATH COMPARISON")

    plt.figure(figsize=(10, 5))

    plt.bar(
        [country1, country2],
        [deaths1, deaths2]
    )

    plt.title("COVID-19 Death Comparison")
    plt.xlabel("Country")
    plt.ylabel("Deaths")
    plt.tight_layout()
    plt.show()

    print("\n11. CONFIRMED CASE TREND COMPARISON")

    plt.figure(figsize=(10, 5))

    plt.plot(
        daily1.index,
        daily1["Confirmed"],
        label=country1
    )

    plt.plot(
        daily2.index,
        daily2["Confirmed"],
        label=country2
    )

    plt.title("Confirmed COVID-19 Cases Trend Comparison")
    plt.xlabel("Date")
    plt.ylabel("Confirmed Cases")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    print("\n12. DEATH TREND COMPARISON")

    plt.figure(figsize=(10, 5))

    plt.plot(
        daily1.index,
        daily1["Deaths"],
        label=country1
    )

    plt.plot(
        daily2.index,
        daily2["Deaths"],
        label=country2
    )

    plt.title("COVID-19 Death Trend Comparison")
    plt.xlabel("Date")
    plt.ylabel("Deaths")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    print("\n13. COMPARISON ANALYSIS COMPLETED")
    print("Country comparison and trend analysis generated successfully.")
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/cleaned_covid_data.csv")
df["Date"] = pd.to_datetime(df["Date"])

print("STATE/PROVINCE COVID-19 ANALYSIS MODULE")

print("\n1. DATA LOADING")
print("Cleaned dataset loaded successfully.")

countries = sorted(df["Country/Region"].unique())

print("\n2. AVAILABLE COUNTRIES")
print("Total number of countries:")
print(len(countries))

country = input("\nEnter country name: ").strip()

if country not in countries:
    print("\nInvalid country name.")
else:
    country_data = df[df["Country/Region"] == country].copy()

    regions = sorted(
        country_data[
            country_data["Province/State"] != "Unknown"
        ]["Province/State"].unique()
    )

    if len(regions) == 0:
        print("\nNo state/province data available for " + country + ".")
    else:
        print("\n3. AVAILABLE STATES/PROVINCES")
        print(regions)

        print("\nTotal States/Provinces:")
        print(len(regions))

        region = input("\nEnter state/province name: ").strip()

        if region not in regions:
            print("\nInvalid state/province name.")
        else:
            regional_data = country_data[
                country_data["Province/State"] == region
            ].copy()

            print("\n4. SELECTED STATE/PROVINCE")
            print("Country:")
            print(country)
            print("State/Province:")
            print(region)

            latest_date = regional_data["Date"].max()

            print("\n5. LATEST DATE")
            print("Latest available date:")
            print(latest_date)

            latest_data = regional_data[
                regional_data["Date"] == latest_date
            ]

            confirmed = latest_data["Confirmed"].sum()
            recovered = latest_data["Recovered"].sum()
            deaths = latest_data["Deaths"].sum()

            recovered_available = recovered > 0

            if recovered_available:
                active = confirmed - recovered - deaths
            else:
                active = None

            print("\n6. STATE/PROVINCE COVID-19 STATISTICS")

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

            print("\n7. STATE/PROVINCE TIME-SERIES DATA")

            daily_data = regional_data.groupby("Date")[
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

            print("\n8. STATE/PROVINCE STATISTICAL SUMMARY")

            print(daily_data.describe())

            print("\n9. STATE/PROVINCE TREND CHART")

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

            plt.title(
                "COVID-19 Trend for "
                + region
                + ", "
                + country
            )

            plt.xlabel("Date")
            plt.ylabel("Cases")
            plt.legend()
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()

            print("\n10. CASE DISTRIBUTION")

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

            else:

                categories = [
                    "Confirmed",
                    "Deaths"
                ]

                values = [
                    confirmed,
                    deaths
                ]

                print(
                    "\nRecovered and Active cases are not included"
                )

                print(
                    "because recovered data is unavailable for the latest date."
                )

            plt.figure(figsize=(8, 5))

            plt.bar(
                categories,
                values
            )

            plt.title(
                "COVID-19 Case Distribution for "
                + region
                + ", "
                + country
            )

            plt.xlabel("Case Type")
            plt.ylabel("Number of Cases")
            plt.tight_layout()
            plt.show()

            print("\n11. STATE/PROVINCE DATA TABLE")

            print(daily_data)

            print("\n12. STATE/PROVINCE ANALYSIS COMPLETED")
            print("State/Province analysis generated successfully.")
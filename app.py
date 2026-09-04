import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="COVID-19 Data Analysis Dashboard",
    page_icon="🌍",
    layout="wide"
)

df = pd.read_csv("data/cleaned_covid_data.csv")
df["Date"] = pd.to_datetime(df["Date"])

st.title("COVID-19 Data Analysis Dashboard")

st.sidebar.title("Navigation")

menu = st.sidebar.radio(
    "Select Analysis",
    [
        "🌍 Worldwide Dashboard",
        "📋 Worldwide Report",
        "🌎 Country Analysis",
        "🏙️ State/Province Analysis",
        "📊 Comparison & Trends"
    ]
)

st.sidebar.markdown("---")
st.sidebar.write("COVID-19 Data Analysis Project")
st.sidebar.write("Python • Pandas • NumPy • Matplotlib • Streamlit")


if menu == "🌍 Worldwide Dashboard":

    st.header("🌍 Worldwide Dashboard")

    latest_date = df["Date"].max()
    latest_data = df[df["Date"] == latest_date]

    confirmed = latest_data["Confirmed"].sum()
    deaths = latest_data["Deaths"].sum()
    recovered = latest_data["Recovered"].sum()

    recovered_available = recovered > 0

    st.subheader("Global Statistics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Confirmed Cases", f"{confirmed:,.0f}")

    with col2:
        st.metric("Deaths", f"{deaths:,.0f}")

    with col3:
        if recovered_available:
            st.metric("Recovered Cases", f"{recovered:,.0f}")
        else:
            st.metric("Recovered Cases", "Not Available")

    with col4:
        if recovered_available:
            active = confirmed - recovered - deaths
            st.metric("Active Cases", f"{active:,.0f}")
        else:
            st.metric("Active Cases", "Not Available")

    st.caption(
        f"Latest available date: {latest_date.strftime('%Y-%m-%d')}"
    )

    if not recovered_available:
        st.warning(
            "Recovered cases are not available for the latest date "
            "in the dataset. Therefore, active cases cannot be "
            "calculated for the latest date."
        )

    st.subheader("Worldwide Confirmed Cases Trend")

    daily_confirmed = (
        df.groupby("Date")["Confirmed"]
        .sum()
        .reset_index()
    )

    fig1, ax1 = plt.subplots()

    ax1.plot(
        daily_confirmed["Date"],
        daily_confirmed["Confirmed"]
    )

    ax1.set_xlabel("Date")
    ax1.set_ylabel("Confirmed Cases")
    ax1.set_title("Worldwide Confirmed Cases Over Time")

    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(fig1)

    st.subheader("Worldwide Deaths Trend")

    daily_deaths = (
        df.groupby("Date")["Deaths"]
        .sum()
        .reset_index()
    )

    fig2, ax2 = plt.subplots()

    ax2.plot(
        daily_deaths["Date"],
        daily_deaths["Deaths"]
    )

    ax2.set_xlabel("Date")
    ax2.set_ylabel("Deaths")
    ax2.set_title("Worldwide Deaths Over Time")

    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(fig2)

    st.subheader("Top 10 Countries by Confirmed Cases")

    country_confirmed = (
        latest_data.groupby("Country/Region")["Confirmed"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    st.bar_chart(country_confirmed)

    st.success("Worldwide Dashboard loaded successfully.")


elif menu == "📋 Worldwide Report":

    st.header("📋 Worldwide Report")

    latest_date = df["Date"].max()
    latest_data = df[df["Date"] == latest_date]

    confirmed = latest_data["Confirmed"].sum()
    deaths = latest_data["Deaths"].sum()
    recovered = latest_data["Recovered"].sum()

    recovered_available = recovered > 0

    st.subheader("Worldwide Summary")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Confirmed Cases", f"{confirmed:,.0f}")

    with col2:
        st.metric("Deaths", f"{deaths:,.0f}")

    with col3:
        if recovered_available:
            st.metric("Recovered Cases", f"{recovered:,.0f}")
        else:
            st.metric("Recovered Cases", "Not Available")

    st.caption(
        f"Report based on latest available date: "
        f"{latest_date.strftime('%Y-%m-%d')}"
    )

    if not recovered_available:
        st.warning(
            "Recovered cases are not available for the latest "
            "date in the dataset."
        )

    st.subheader("Top 10 Countries by Confirmed Cases")

    top_confirmed = (
        latest_data.groupby("Country/Region")["Confirmed"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    confirmed_table = top_confirmed.reset_index()

    confirmed_table.columns = [
        "Country/Region",
        "Confirmed Cases"
    ]

    st.dataframe(
        confirmed_table,
        use_container_width=True
    )

    st.subheader("Top 10 Countries by Deaths")

    top_deaths = (
        latest_data.groupby("Country/Region")["Deaths"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    deaths_table = top_deaths.reset_index()

    deaths_table.columns = [
        "Country/Region",
        "Deaths"
    ]

    st.dataframe(
        deaths_table,
        use_container_width=True
    )

    st.subheader("Statistical Summary")

    statistics = latest_data[
        ["Confirmed", "Recovered", "Deaths"]
    ].describe()

    st.dataframe(
        statistics,
        use_container_width=True
    )

    st.subheader("Key Findings")

    top_confirmed_country = top_confirmed.index[0]
    top_death_country = top_deaths.index[0]

    st.write(
        f"• {top_confirmed_country} has the highest confirmed "
        f"cases in the latest available data."
    )

    st.write(
        f"• {top_death_country} has the highest number of deaths "
        f"in the latest available data."
    )

    st.write(
        f"• The latest available date in the dataset is "
        f"{latest_date.strftime('%Y-%m-%d')}."
    )

    st.write(
        "• Recovered-case data is not available for the latest "
        "date, so active cases are not calculated for the "
        "latest worldwide report."
    )

    st.success("Worldwide Report loaded successfully.")


elif menu == "🌎 Country Analysis":

    st.header("🌎 Country Analysis")

    countries = sorted(
        df["Country/Region"].dropna().unique()
    )

    country = st.selectbox(
        "Select Country",
        countries
    )

    country_data = df[
        df["Country/Region"] == country
    ]

    latest_date = country_data["Date"].max()

    latest_data = country_data[
        country_data["Date"] == latest_date
    ]

    confirmed = latest_data["Confirmed"].sum()
    deaths = latest_data["Deaths"].sum()
    recovered = latest_data["Recovered"].sum()

    recovered_available = recovered > 0

    st.subheader(
        f"Statistics for {country}"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Confirmed Cases",
            f"{confirmed:,.0f}"
        )

    with col2:
        if recovered_available:
            st.metric(
                "Recovered Cases",
                f"{recovered:,.0f}"
            )
        else:
            st.metric(
                "Recovered Cases",
                "Not Available"
            )

    with col3:
        st.metric(
            "Deaths",
            f"{deaths:,.0f}"
        )

    with col4:
        if recovered_available:
            active = confirmed - recovered - deaths
            st.metric(
                "Active Cases",
                f"{active:,.0f}"
            )
        else:
            st.metric(
                "Active Cases",
                "Not Available"
            )

    st.caption(
        f"Latest available date: "
        f"{latest_date.strftime('%Y-%m-%d')}"
    )

    if not recovered_available:
        st.warning(
            "Recovered cases are not available for the latest "
            "date. Therefore, latest active cases cannot be "
            "calculated."
        )

    st.subheader(
        f"{country} Confirmed Cases Trend"
    )

    daily_country = (
        country_data.groupby("Date")["Confirmed"]
        .sum()
        .reset_index()
    )

    fig3, ax3 = plt.subplots()

    ax3.plot(
        daily_country["Date"],
        daily_country["Confirmed"]
    )

    ax3.set_xlabel("Date")
    ax3.set_ylabel("Confirmed Cases")
    ax3.set_title(
        f"Confirmed Cases Trend - {country}"
    )

    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(fig3)

    st.subheader(
        f"{country} Deaths Trend"
    )

    daily_country_deaths = (
        country_data.groupby("Date")["Deaths"]
        .sum()
        .reset_index()
    )

    fig4, ax4 = plt.subplots()

    ax4.plot(
        daily_country_deaths["Date"],
        daily_country_deaths["Deaths"]
    )

    ax4.set_xlabel("Date")
    ax4.set_ylabel("Deaths")
    ax4.set_title(
        f"Deaths Trend - {country}"
    )

    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(fig4)

    st.subheader("Country Statistical Summary")

    country_statistics = country_data[
        ["Confirmed", "Recovered", "Deaths"]
    ].describe()

    st.dataframe(
        country_statistics,
        use_container_width=True
    )

    st.success(
        f"Country Analysis for {country} loaded successfully."
    )


elif menu == "🏙️ State/Province Analysis":

    st.header("🏙️ State/Province Analysis")

    countries = sorted(
        df["Country/Region"].dropna().unique()
    )

    country = st.selectbox(
        "Select Country",
        countries
    )

    country_data = df[
        df["Country/Region"] == country
    ]

    regions = sorted(
        country_data[
            country_data["Province/State"] != "Unknown"
        ]["Province/State"]
        .dropna()
        .unique()
    )

    if len(regions) == 0:

        st.warning(
            f"No state/province data available for {country}."
        )

    else:

        region = st.selectbox(
            "Select State/Province",
            regions
        )

        region_data = country_data[
            country_data["Province/State"] == region
        ]

        latest_date = region_data["Date"].max()

        latest_data = region_data[
            region_data["Date"] == latest_date
        ]

        confirmed = latest_data["Confirmed"].sum()
        deaths = latest_data["Deaths"].sum()
        recovered = latest_data["Recovered"].sum()

        recovered_available = recovered > 0

        st.subheader(
            f"Statistics for {region}, {country}"
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Confirmed Cases",
                f"{confirmed:,.0f}"
            )

        with col2:
            if recovered_available:
                st.metric(
                    "Recovered Cases",
                    f"{recovered:,.0f}"
                )
            else:
                st.metric(
                    "Recovered Cases",
                    "Not Available"
                )

        with col3:
            st.metric(
                "Deaths",
                f"{deaths:,.0f}"
            )

        with col4:
            if recovered_available:
                active = confirmed - recovered - deaths
                st.metric(
                    "Active Cases",
                    f"{active:,.0f}"
                )
            else:
                st.metric(
                    "Active Cases",
                    "Not Available"
                )

        st.caption(
            f"Latest available date: "
            f"{latest_date.strftime('%Y-%m-%d')}"
        )

        if not recovered_available:
            st.warning(
                "Recovered cases are not available for the latest "
                "date. Therefore, latest active cases cannot be "
                "calculated."
            )

        st.subheader(
            f"{region} Confirmed Cases Trend"
        )

        daily_region = (
            region_data.groupby("Date")["Confirmed"]
            .sum()
            .reset_index()
        )

        fig5, ax5 = plt.subplots()

        ax5.plot(
            daily_region["Date"],
            daily_region["Confirmed"]
        )

        ax5.set_xlabel("Date")
        ax5.set_ylabel("Confirmed Cases")
        ax5.set_title(
            f"Confirmed Cases Trend - {region}"
        )

        plt.xticks(rotation=45)
        plt.tight_layout()

        st.pyplot(fig5)

        st.subheader(
            f"{region} Deaths Trend"
        )

        daily_region_deaths = (
            region_data.groupby("Date")["Deaths"]
            .sum()
            .reset_index()
        )

        fig6, ax6 = plt.subplots()

        ax6.plot(
            daily_region_deaths["Date"],
            daily_region_deaths["Deaths"]
        )

        ax6.set_xlabel("Date")
        ax6.set_ylabel("Deaths")
        ax6.set_title(
            f"Deaths Trend - {region}"
        )

        plt.xticks(rotation=45)
        plt.tight_layout()

        st.pyplot(fig6)

        st.subheader("Regional Statistical Summary")

        region_statistics = region_data[
            ["Confirmed", "Recovered", "Deaths"]
        ].describe()

        st.dataframe(
            region_statistics,
            use_container_width=True
        )

        st.success(
            f"State/Province Analysis for {region} loaded successfully."
        )


elif menu == "📊 Comparison & Trends":

    st.header("📊 Comparison & Trends")

    countries = sorted(
        df["Country/Region"].dropna().unique()
    )

    col1, col2 = st.columns(2)

    with col1:
        country1 = st.selectbox(
            "Select First Country",
            countries,
            index=countries.index("India")
            if "India" in countries else 0
        )

    with col2:
        country2 = st.selectbox(
            "Select Second Country",
            countries,
            index=countries.index("Canada")
            if "Canada" in countries else 1
        )

    if country1 == country2:

        st.warning(
            "Please select two different countries for comparison."
        )

    else:

        data1 = df[
            df["Country/Region"] == country1
        ]

        data2 = df[
            df["Country/Region"] == country2
        ]

        latest_date1 = data1["Date"].max()
        latest_date2 = data2["Date"].max()

        latest1 = data1[
            data1["Date"] == latest_date1
        ]

        latest2 = data2[
            data2["Date"] == latest_date2
        ]

        confirmed1 = latest1["Confirmed"].sum()
        deaths1 = latest1["Deaths"].sum()
        recovered1 = latest1["Recovered"].sum()

        confirmed2 = latest2["Confirmed"].sum()
        deaths2 = latest2["Deaths"].sum()
        recovered2 = latest2["Recovered"].sum()

        recovered_available1 = recovered1 > 0
        recovered_available2 = recovered2 > 0

        st.subheader("Country Statistics")

        col1, col2 = st.columns(2)

        with col1:

            st.write(f"### {country1}")

            st.metric(
                "Confirmed Cases",
                f"{confirmed1:,.0f}"
            )

            if recovered_available1:
                st.metric(
                    "Recovered Cases",
                    f"{recovered1:,.0f}"
                )
            else:
                st.metric(
                    "Recovered Cases",
                    "Not Available"
                )

            st.metric(
                "Deaths",
                f"{deaths1:,.0f}"
            )

            st.caption(
                f"Latest date: "
                f"{latest_date1.strftime('%Y-%m-%d')}"
            )

        with col2:

            st.write(f"### {country2}")

            st.metric(
                "Confirmed Cases",
                f"{confirmed2:,.0f}"
            )

            if recovered_available2:
                st.metric(
                    "Recovered Cases",
                    f"{recovered2:,.0f}"
                )
            else:
                st.metric(
                    "Recovered Cases",
                    "Not Available"
                )

            st.metric(
                "Deaths",
                f"{deaths2:,.0f}"
            )

            st.caption(
                f"Latest date: "
                f"{latest_date2.strftime('%Y-%m-%d')}"
            )

        st.subheader("Comparison Table")

        recovered_value1 = (
            recovered1
            if recovered_available1
            else "Not Available"
        )

        recovered_value2 = (
            recovered2
            if recovered_available2
            else "Not Available"
        )

        comparison = pd.DataFrame({
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
        })

        st.dataframe(
            comparison,
            use_container_width=True
        )

        st.subheader("Confirmed Cases Comparison")

        comparison_confirmed = pd.DataFrame({
            "Country": [
                country1,
                country2
            ],
            "Confirmed Cases": [
                confirmed1,
                confirmed2
            ]
        })

        st.bar_chart(
            comparison_confirmed.set_index("Country")
        )

        st.subheader("Deaths Comparison")

        comparison_deaths = pd.DataFrame({
            "Country": [
                country1,
                country2
            ],
            "Deaths": [
                deaths1,
                deaths2
            ]
        })

        st.bar_chart(
            comparison_deaths.set_index("Country")
        )

        st.subheader(
            "Confirmed Cases Trend Comparison"
        )

        trend1 = (
            data1.groupby("Date")["Confirmed"]
            .sum()
            .reset_index()
        )

        trend2 = (
            data2.groupby("Date")["Confirmed"]
            .sum()
            .reset_index()
        )

        fig7, ax7 = plt.subplots()

        ax7.plot(
            trend1["Date"],
            trend1["Confirmed"],
            label=country1
        )

        ax7.plot(
            trend2["Date"],
            trend2["Confirmed"],
            label=country2
        )

        ax7.set_xlabel("Date")
        ax7.set_ylabel("Confirmed Cases")
        ax7.set_title(
            "Confirmed Cases Trend Comparison"
        )

        ax7.legend()

        plt.xticks(rotation=45)
        plt.tight_layout()

        st.pyplot(fig7)

        st.subheader(
            "Deaths Trend Comparison"
        )

        death_trend1 = (
            data1.groupby("Date")["Deaths"]
            .sum()
            .reset_index()
        )

        death_trend2 = (
            data2.groupby("Date")["Deaths"]
            .sum()
            .reset_index()
        )

        fig8, ax8 = plt.subplots()

        ax8.plot(
            death_trend1["Date"],
            death_trend1["Deaths"],
            label=country1
        )

        ax8.plot(
            death_trend2["Date"],
            death_trend2["Deaths"],
            label=country2
        )

        ax8.set_xlabel("Date")
        ax8.set_ylabel("Deaths")
        ax8.set_title(
            "Deaths Trend Comparison"
        )

        ax8.legend()

        plt.xticks(rotation=45)
        plt.tight_layout()

        st.pyplot(fig8)

        st.subheader(
            f"Statistical Summary - {country1}"
        )

        statistics1 = data1[
            ["Confirmed", "Recovered", "Deaths"]
        ].describe()

        st.dataframe(
            statistics1,
            use_container_width=True
        )

        st.subheader(
            f"Statistical Summary - {country2}"
        )

        statistics2 = data2[
            ["Confirmed", "Recovered", "Deaths"]
        ].describe()

        st.dataframe(
            statistics2,
            use_container_width=True
        )

        st.success(
            f"Comparison between {country1} and {country2} "
            "loaded successfully."
        )
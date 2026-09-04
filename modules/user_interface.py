import streamlit as st

st.set_page_config(
    page_title="COVID-19 Data Analysis Dashboard",
    page_icon="🌍",
    layout="wide"
)

st.title(" COVID-19 Data Analysis Dashboard")

st.write(
    "Interactive dashboard for analyzing COVID-19 cases, "
    "deaths, recoveries and trends."
)

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

    st.info(
        "This section displays worldwide COVID-19 statistics "
        "and visual trends."
    )

    st.subheader("Global Statistics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Confirmed Cases",
            "View Analysis"
        )

    with col2:
        st.metric(
            "Deaths",
            "View Analysis"
        )

    with col3:
        st.metric(
            "Recovered Cases",
            "Data Limited"
        )

    with col4:
        st.metric(
            "Active Cases",
            "Data Limited"
        )

    st.subheader("Worldwide Analysis")

    st.write(
        "Worldwide confirmed cases and deaths can be analyzed "
        "using the cleaned COVID-19 dataset."
    )

elif menu == "📋 Worldwide Report":

    st.header("📋 Worldwide Report")

    st.info(
        "This section provides worldwide summary statistics, "
        "top countries and major findings."
    )

    st.subheader("Worldwide Summary")

    st.write(
        "The report summarizes the overall COVID-19 situation "
        "using the available dataset."
    )

    st.subheader("Top Countries")

    st.write(
        "Country rankings can be viewed based on confirmed cases "
        "and deaths."
    )

    st.subheader("Key Findings")

    st.write(
        "The report helps identify countries with high numbers "
        "of confirmed cases and deaths."
    )

elif menu == "🌎 Country Analysis":

    st.header("🌎 Country Analysis")

    st.info(
        "Select a country to analyze its COVID-19 statistics "
        "and historical trends."
    )

    st.selectbox(
        "Select Country",
        [
            "India",
            "Canada",
            "United States",
            "Brazil",
            "France"
        ]
    )

    st.subheader("Country Statistics")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Confirmed Cases",
            "View Data"
        )

    with col2:
        st.metric(
            "Recovered Cases",
            "Data Limited"
        )

    with col3:
        st.metric(
            "Deaths",
            "View Data"
        )

    st.subheader("Country Trend")

    st.write(
        "The selected country's confirmed cases, recoveries "
        "and deaths can be analyzed over time."
    )

elif menu == "🏙️ State/Province Analysis":

    st.header("🏙️ State/Province Analysis")

    st.info(
        "Select a country and state/province to analyze "
        "regional COVID-19 statistics."
    )

    country = st.selectbox(
        "Select Country",
        [
            "Canada",
            "China",
            "Australia",
            "United States"
        ]
    )

    st.selectbox(
        "Select State/Province",
        [
            "Select a country first"
        ]
    )

    st.subheader("Regional Statistics")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Confirmed Cases",
            "View Data"
        )

    with col2:
        st.metric(
            "Recovered Cases",
            "Data Limited"
        )

    with col3:
        st.metric(
            "Deaths",
            "View Data"
        )

    st.subheader("State/Province Trend")

    st.write(
        "Regional COVID-19 trends can be analyzed using "
        "the selected state or province."
    )

elif menu == "📊 Comparison & Trends":

    st.header("📊 Comparison & Trends")

    st.info(
        "Compare COVID-19 statistics and trends between "
        "two countries."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.selectbox(
            "Select First Country",
            [
                "India",
                "Canada",
                "United States",
                "Brazil",
                "France"
            ]
        )

    with col2:
        st.selectbox(
            "Select Second Country",
            [
                "Canada",
                "India",
                "United States",
                "Brazil",
                "France"
            ]
        )

    st.subheader("Comparison")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Confirmed Cases",
            "Compare"
        )

    with col2:
        st.metric(
            "Deaths",
            "Compare"
        )

    with col3:
        st.metric(
            "Recovered Cases",
            "Data Limited"
        )

    st.subheader("Trend Comparison")

    st.write(
        "Confirmed cases and death trends can be compared "
        "between the selected countries."
    )

st.sidebar.markdown("---")

st.sidebar.caption(
    "COVID-19 Data Analysis Dashboard"
)
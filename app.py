import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import urllib.request
import re

# Streamlit UI
st.set_page_config(page_title="COVID-19 Data Analysis Dashboard", page_icon="🌍", layout="wide")

# ==========================================
# WEEK 8: Reading files with Pandas
# ==========================================
try:
    df = pd.read_csv("data/cleaned_covid_data.csv")
except Exception:
    df = pd.read_csv("data/covid_data.csv")
    
df["Date"] = pd.to_datetime(df["Date"])

# ==========================================
# WEEK 6 & 7: Pandas features
# ==========================================
# Filling NaN with string/value
if "Province/State" not in df.columns:
    df["Province/State"] = "Unknown"
df["Province/State"] = df["Province/State"].fillna("Unknown")

# 1. FORCEFULLY ADD RECOVERY CASES
# Setting conditions and adding a new column
assumption_rate = 0.80
# If Recovered column doesn't exist, create it
if "Recovered" not in df.columns:
    df["Recovered"] = np.nan

df["Recovered"] = df["Recovered"].fillna(0)

# Apply assumption where recovery is 0 or missing
missing_recovery = df["Recovered"] == 0
df.loc[missing_recovery, "Recovered"] = df.loc[missing_recovery, "Confirmed"] * assumption_rate

# Ensure Recovered never exceeds Confirmed and is never negative
df["Recovered"] = np.where(df["Recovered"] > df["Confirmed"], df["Confirmed"], df["Recovered"])
df["Recovered"] = np.where(df["Recovered"] < 0, 0, df["Recovered"])

# Adding a new column Active
df["Active"] = df["Confirmed"] - df["Recovered"] - df["Deaths"]

# Sorting based on column values
df = df.sort_values(by=["Date", "Country/Region"])


# ==========================================
# WEEK 1-5 & 11: NumPy & Preprocessing Demo
# ==========================================
def demonstrate_numpy_and_preprocessing(confirmed_cases):
    """A simple function demonstrating NumPy and Preprocessing concepts."""
    # Week 1: Creating NumPy Arrays
    arr = np.array(confirmed_cases)
    zeros = np.zeros(3)
    ones = np.ones(3)
    random_arr = np.random.rand(3)
    identity = np.eye(3)
    spaced = np.arange(0, 10, 2)
    
    # Week 2: Shape and Reshaping
    if arr.size > 0:
        dim = arr.ndim
        shape = arr.shape
        size = arr.size
        if size >= 4:
            reshaped = arr[:4].reshape(2, -1)
            flattened = reshaped.flatten()
            transposed = reshaped.T
            
    # Week 3: Expanding and Squeezing
    if arr.size > 0:
        expanded = np.expand_dims(arr, axis=0)
        squeezed = np.squeeze(expanded)
        sorted_arr = np.sort(arr)
        
    # Week 4: Indexing and Slicing
    if arr.size > 5:
        slice_1d = arr[1:4]
        neg_slice = arr[-3:]
        
    # Week 5: Stacking and Concatenating
    if arr.size >= 2:
        a = arr[:2]
        b = arr[:2] * 2
        stacked = np.stack((a, b))
        concat = np.concatenate((a, b))
        # Broadcasting
        broadcast = a + 100
        
    # Week 11: Preprocessing (Feature Scaling - MinMax)
    if arr.size > 0 and arr.max() - arr.min() > 0:
        scaled = (arr - arr.min()) / (arr.max() - arr.min())
        # Standardization (Z-score)
        std_dev = arr.std()
        if std_dev > 0:
            standardized = (arr - arr.mean()) / std_dev
            
    return True

# Week 10: Web Scraping Demo
def get_covid_news():
    try:
        req = urllib.request.Request('https://en.wikipedia.org/wiki/COVID-19', headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req, timeout=3).read().decode('utf-8')
        match = re.search(r'<p>(.*?)</p>', html, re.IGNORECASE | re.DOTALL)
        if match:
            text = re.sub(r'<[^>]+>', '', match.group(1))
            return text[:200] + "..."
    except Exception:
        pass
    return "Web scraping news currently unavailable."


st.title("COVID-19 DATA ANALYSIS DASHBOARD")


# UI: Horizontal Menu using Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🌍 Worldwide Dashboard", 
    "📋 Worldwide Report", 
    "🌎 Country Analysis", 
    "🏙️ State/Province Analysis", 
    "📊 Comparison & Trends"
])

latest_date = df["Date"].max()
latest_data = df[df["Date"] == latest_date]

with tab1:
    st.header("🌍 Worldwide Dashboard")
    
    confirmed = latest_data["Confirmed"].sum()
    deaths = latest_data["Deaths"].sum()
    recovered = latest_data["Recovered"].sum()
    active = latest_data["Active"].sum()
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Confirmed", f"{confirmed:,.0f}")
    col2.metric("Total Deaths", f"{deaths:,.0f}")
    col3.metric("Total Recovered", f"{recovered:,.0f}")
    col4.metric("Active Cases", f"{active:,.0f}")
    
    # Week 12: Matplotlib Visualization
    st.subheader("Global Case Distribution")
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        # Pie Chart
        fig1, ax1 = plt.subplots()
        labels = ['Active', 'Recovered', 'Deaths']
        sizes = [active, recovered, deaths]
        colors = ['#ff9999','#66b3ff','#ffcc99']
        ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')
        ax1.set_title("Global Cases Distribution")
        st.pyplot(fig1)
        
    with col_chart2:
        # Line Chart
        daily_global = df.groupby("Date")[["Confirmed", "Recovered", "Deaths"]].sum().reset_index()
        fig2, ax2 = plt.subplots()
        ax2.plot(daily_global["Date"], daily_global["Confirmed"], label="Confirmed")
        ax2.plot(daily_global["Date"], daily_global["Recovered"], label="Recovered")
        ax2.plot(daily_global["Date"], daily_global["Deaths"], label="Deaths")
        ax2.set_xlabel("Date")
        ax2.set_ylabel("Cases")
        ax2.set_title("Worldwide Trend Over Time")
        ax2.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig2)
        
    # Execute NumPy Demo silently
    demonstrate_numpy_and_preprocessing(latest_data["Confirmed"].values)

with tab2:
    st.header("📋 Worldwide Report")
    st.write(f"Report based on latest available date: {latest_date.strftime('%Y-%m-%d')}")
    
    # Groupby for summary
    top_countries = latest_data.groupby("Country/Region")[["Confirmed", "Recovered", "Deaths"]].sum().sort_values(by="Confirmed", ascending=False).head(10)
    
    st.subheader("Top 10 Countries by Confirmed Cases")
    st.dataframe(top_countries, use_container_width=True)
    
    st.subheader("Latest COVID-19 Information (Web Scraping Demo)")
    st.write(get_covid_news())
    
    # Box Plot & Histogram
    col_chart3, col_chart4 = st.columns(2)
    with col_chart3:
        fig3, ax3 = plt.subplots()
        ax3.boxplot(top_countries["Confirmed"].dropna())
        ax3.set_title("Box Plot: Confirmed Cases (Top 10)")
        st.pyplot(fig3)
        
    with col_chart4:
        fig4, ax4 = plt.subplots()
        ax4.hist(latest_data["Confirmed"].dropna(), bins=20, color='skyblue', edgecolor='black')
        ax4.set_title("Histogram: Confirmed Cases Distribution")
        ax4.set_yscale("log")
        st.pyplot(fig4)

with tab3:
    st.header("🌎 Country Analysis")
    countries = sorted(df["Country/Region"].dropna().unique())
    selected_country = st.selectbox("Select Country", countries, key="country_select")
    
    country_data = df[df["Country/Region"] == selected_country]
    c_latest = country_data[country_data["Date"] == country_data["Date"].max()]
    
    c_conf = c_latest["Confirmed"].sum()
    c_dead = c_latest["Deaths"].sum()
    c_rec = c_latest["Recovered"].sum()
    c_act = c_latest["Active"].sum()
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Confirmed", f"{c_conf:,.0f}")
    c2.metric("Deaths", f"{c_dead:,.0f}")
    c3.metric("Recovered", f"{c_rec:,.0f}")
    c4.metric("Active", f"{c_act:,.0f}")
    
    # Subplots
    st.subheader("Trend Subplots")
    daily_c = country_data.groupby("Date")[["Confirmed", "Recovered", "Deaths"]].sum().reset_index()
    
    fig5, (ax_c1, ax_c2, ax_c3) = plt.subplots(3, 1, figsize=(8, 10))
    ax_c1.plot(daily_c["Date"], daily_c["Confirmed"], color='blue')
    ax_c1.set_title("Confirmed Trend")
    
    ax_c2.plot(daily_c["Date"], daily_c["Recovered"], color='green')
    ax_c2.set_title("Recovered Trend")
    
    ax_c3.plot(daily_c["Date"], daily_c["Deaths"], color='red')
    ax_c3.set_title("Deaths Trend")
    
    plt.tight_layout()
    st.pyplot(fig5)

with tab4:
    st.header("🏙️ State/Province Analysis")
    countries_with_states = df[df["Province/State"] != "Unknown"]["Country/Region"].unique()
    
    st_country = st.selectbox("Select Country", sorted(countries_with_states), key="state_country_select")
    state_data_full = df[df["Country/Region"] == st_country]
    states = sorted(state_data_full["Province/State"].unique())
    
    st_state = st.selectbox("Select State/Province", states)
    
    state_data = state_data_full[state_data_full["Province/State"] == st_state]
    s_latest = state_data[state_data["Date"] == state_data["Date"].max()]
    
    st.write(f"### Statistics for {st_state}, {st_country}")
    
    sc1, sc2, sc3, sc4 = st.columns(4)
    sc1.metric("Confirmed", f"{s_latest['Confirmed'].sum():,.0f}")
    sc2.metric("Deaths", f"{s_latest['Deaths'].sum():,.0f}")
    sc3.metric("Recovered", f"{s_latest['Recovered'].sum():,.0f}")
    sc4.metric("Active", f"{s_latest['Active'].sum():,.0f}")
    
    # Scatter Plot
    st.subheader("Scatter Plot: Confirmed vs Deaths")
    fig6, ax6 = plt.subplots()
    ax6.scatter(state_data["Confirmed"], state_data["Deaths"], alpha=0.5, color='purple')
    ax6.set_xlabel("Confirmed Cases")
    ax6.set_ylabel("Deaths")
    ax6.set_title(f"Confirmed vs Deaths in {st_state}")
    st.pyplot(fig6)

with tab5:
    st.header("📊 Comparison & Trends")
    comp_c1, comp_c2 = st.columns(2)
    with comp_c1:
        country1 = st.selectbox("Select First Country", countries, index=countries.index("India") if "India" in countries else 0)
    with comp_c2:
        country2 = st.selectbox("Select Second Country", countries, index=countries.index("Canada") if "Canada" in countries else 1)
        
    if country1 == country2:
        st.warning("Please select two different countries.")
    else:
        d1 = df[df["Country/Region"] == country1]
        d2 = df[df["Country/Region"] == country2]
        
        # Bar Graph for comparison
        st.subheader("Comparison of Latest Cases")
        
        latest_c1 = d1[d1["Date"] == d1["Date"].max()][["Confirmed", "Recovered", "Deaths"]].sum()
        latest_c2 = d2[d2["Date"] == d2["Date"].max()][["Confirmed", "Recovered", "Deaths"]].sum()
        
        comp_df = pd.DataFrame({
            country1: latest_c1,
            country2: latest_c2
        }).T
        
        fig7, ax7 = plt.subplots()
        comp_df.plot(kind='bar', ax=ax7)
        ax7.set_title("Cases Comparison")
        ax7.set_ylabel("Number of Cases")
        plt.xticks(rotation=0)
        st.pyplot(fig7)
        
        # Pandas concat demonstration (Week 6)
        concat_demo = pd.concat([d1.tail(1), d2.tail(1)])
        st.write("Recent Data Snippet (Concat Demo):")
        st.dataframe(concat_demo[["Date", "Country/Region", "Confirmed", "Recovered", "Deaths", "Active"]])
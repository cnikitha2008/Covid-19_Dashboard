import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import urllib.request
import re

# ==============================================================================
# PROJECT MODULE IMPORTS
# ------------------------------------------------------------------------------
# Here we import our custom modular packages from the 'modules' directory:
# 1. Module 1: data_management (handles loading, cleaning, recovery estimation,
#    active cases computation, and chronological sorting)
# 2. Module 2: worldwide_analysis (handles global metric aggregations, ranking
#    top countries, and compiling global daily time-series trends)
# ==============================================================================
import modules.data_management as data_management
import modules.worldwide_analysis as worldwide_analysis

# ==============================================================================
# STREAMLIT PAGE CONFIGURATION
# ------------------------------------------------------------------------------
# Configure browser tab title, dashboard icon, and wide responsive layout.
# ==============================================================================
st.set_page_config(
    page_title="COVID-19 Data Analysis Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==============================================================================
# HIDE SIDEBAR & STYLE MENU BUTTONS
# ------------------------------------------------------------------------------
# As requested, the sidebar is completely removed and hidden from the UI.
# Menu buttons are styled to display clean, prominent, and clickable names.
# ==============================================================================
st.markdown(
    """
    <style>
    /* Completely hide sidebar and collapse/expand arrow controls */
    [data-testid="stSidebar"], 
    [data-testid="collapsedControl"],
    section[data-testid="stSidebar"] {
        display: none !important;
    }
    /* Style menu and action buttons: compact, sleek rectangles with modern aesthetics */
    div.stButton > button {
        font-size: 1.05rem !important;
        font-weight: 600 !important;
        padding: 0.55rem 1.15rem !important;
        border-radius: 9px !important;
        margin-bottom: 0.5rem !important;
        border: 1px solid rgba(120, 144, 156, 0.3) !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04) !important;
    }
    div.stButton > button:hover {
        transform: translateY(-2px) !important;
        border-color: #1E88E5 !important;
        box-shadow: 0 6px 14px rgba(30, 136, 229, 0.16) !important;
        color: #1E88E5 !important;
    }
    div.stButton > button:active {
        transform: translateY(0px) !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ==============================================================================
# DATA MANAGEMENT MODULE EXECUTION
# ------------------------------------------------------------------------------
# Load and clean the COVID-19 dataset using our dedicated data management module.
# This ensures cached data processing, missing value imputation, and correct
# calculation of Active cases across all records.
# ==============================================================================
@st.cache_data
def load_cached_data():
    """
    Cached wrapper to load and preprocess the COVID-19 dataset once,
    improving dashboard performance across page transitions.
    """
    return data_management.load_and_clean_data()

df = load_cached_data()

# Identify the latest available date in the dataset for cross-section reports
latest_date = df["Date"].max()
latest_data = df[df["Date"] == latest_date]


# ==============================================================================
# NUMPY & PREPROCESSING DEMONSTRATION HELPER
# ----------------------------------------------------------------=============
def demonstrate_numpy_and_preprocessing(confirmed_cases):
    """
    Demonstrates foundational NumPy operations and preprocessing techniques:
    - Array initialization, reshaping, flattening, transposition
    - Expanding, squeezing, slicing, stacking, broadcasting
    - Min-Max feature scaling and Z-score standardization
    """
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
        broadcast = a + 100
        
    # Week 11: Preprocessing (Feature Scaling - MinMax)
    if arr.size > 0 and arr.max() - arr.min() > 0:
        scaled = (arr - arr.min()) / (arr.max() - arr.min())
        # Standardization (Z-score)
        std_dev = arr.std()
        if std_dev > 0:
            standardized = (arr - arr.mean()) / std_dev
            
    return True


# ==============================================================================
# NAVIGATION STATE MANAGEMENT
# ------------------------------------------------------------------------------
# Streamlit re-runs the entire script upon user interaction.
# We store 'current_page' in st.session_state so the dashboard can:
# 1. Start on the Main Menu page displaying the 5 core options.
# 2. Transition into the selected page upon user click.
# 3. Allow coming back to the Main Menu from any page.
# ==============================================================================
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "Home"

def navigate_to(page_name):
    """
    Helper function to change the active page in session state
    and trigger an immediate rerun of the Streamlit application.
    """
    st.session_state["current_page"] = page_name
    st.rerun()

def render_back_button(location_key="top"):
    """
    Renders a prominent '⬅️ Back to Main Menu' button.
    When clicked, returns the user to the landing menu with all 5 options.
    """
    if st.button("⬅️ Back to Main Menu", key=f"back_btn_{location_key}", use_container_width=False):
        navigate_to("Home")


# ==============================================================================
# ROUTE 1: MAIN MENU PAGE (Displays ONLY the 5 menu names)
# ------------------------------------------------------------------------------
# In accordance with requirements:
# 1. Sidebar is removed.
# 2. Direct page selector dropdown is removed.
# 3. Matter / descriptive paragraphs under menu names are removed.
# 4. Only the 5 menu names are displayed; clicking any name opens that page.
# ==============================================================================
if st.session_state["current_page"] == "Home":
    
    # Centered Header with title and subtitle
    st.markdown(
        """
        <div style="text-align: center; padding-top: 1.2rem; padding-bottom: 1.5rem;">
            <h1 style="font-size: 2.35rem; font-weight: 800; margin: 0; padding-bottom: 0.4rem; letter-spacing: -0.5px;">
                COVID-19 DATA ANALYSIS DASHBOARD
            </h1>
            <p style="color: #6c757d; font-size: 1.05rem; max-width: 620px; margin: 0.3rem auto 0 auto; line-height: 1.5;">
                Interactive epidemiological intelligence system analyzing confirmed cases, recoveries, mortality trajectories, and geographical comparisons.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("---")

    # Centered, compact menu card container to decrease the rectangle size around menu names
    col_l, col_menu, col_r = st.columns([1.2, 1.9, 1.2])

    with col_menu:
        st.markdown(
            """
            <div style="text-align: center; margin-bottom: 0.9rem;">
                <span style="font-size: 0.88rem; font-weight: 600; color: #78909C; text-transform: uppercase; letter-spacing: 1px;">
                    Select an Analysis View
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )

        # List of the 5 analysis menus (Display Name, Target Route Identifier)
        menu_items = [
            ("🌍 Worldwide Dashboard", "Worldwide Dashboard"),
            ("📋 Worldwide Report", "Worldwide Report"),
            ("🌎 Country Analysis", "Country Analysis"),
            ("🏙️ State or Province Analysis", "State or Province Analysis"),
            ("📊 Comparison and Trend", "Comparison and Trend")
        ]

        # Render menu names as compact, sleek clickable buttons
        for display_name, target_page in menu_items:
            if st.button(display_name, key=f"menu_btn_{target_page}", use_container_width=True):
                navigate_to(target_page)

        # Subtle summary feature pills below the menu
        st.markdown(
            """
            <div style="display: flex; justify-content: center; gap: 10px; margin-top: 1.5rem; flex-wrap: wrap;">
                <span style="font-size: 0.78rem; background: rgba(0,0,0,0.04); padding: 4px 10px; border-radius: 6px; color: #666; border: 1px solid rgba(0,0,0,0.06);">
                    📊 Multi-Metric Aggregation
                </span>
                <span style="font-size: 0.78rem; background: rgba(0,0,0,0.04); padding: 4px 10px; border-radius: 6px; color: #666; border: 1px solid rgba(0,0,0,0.06);">
                    📈 Longitudinal Trends
                </span>
                <span style="font-size: 0.78rem; background: rgba(0,0,0,0.04); padding: 4px 10px; border-radius: 6px; color: #666; border: 1px solid rgba(0,0,0,0.06);">
                    🗺️ Regional Breakdown
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )


# ==============================================================================
# ROUTE 2: WORLDWIDE DASHBOARD PAGE
# ------------------------------------------------------------------------------
# Displays worldwide overview: Total Confirmed, Deaths, Recovered, Active cases,
# global distribution pie chart, and daily multi-series time-series trend lines.
# ==============================================================================
elif st.session_state["current_page"] == "Worldwide Dashboard":
    
    # Navigation Header: Back Button & Page Breadcrumbs
    nav_col1, nav_col2 = st.columns([1, 4])
    with nav_col1:
        render_back_button(location_key="worldwide_dash_top")
    with nav_col2:
        st.caption("Navigation: 🏠 Main Menu > 🌍 Worldwide Dashboard")
        
    st.header("🌍 Worldwide Dashboard")
    st.write("Global aggregation and visual distribution of COVID-19 pandemic metrics.")
    st.markdown("---")
    
    # --------------------------------------------------------------------------
    # MODULE 2 USAGE: Worldwide Analysis Module (Global Metric Aggregations)
    # --------------------------------------------------------------------------
    # We call `worldwide_analysis.calculate_worldwide_totals()` to compute the
    # global aggregate sums for Confirmed, Deaths, Recovered, and Active cases.
    # --------------------------------------------------------------------------
    confirmed, deaths, recovered, active = worldwide_analysis.calculate_worldwide_totals(latest_data)
    
    # Display KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Confirmed", f"{confirmed:,.0f}")
    col2.metric("Total Deaths", f"{deaths:,.0f}")
    col3.metric("Total Recovered", f"{recovered:,.0f}")
    col4.metric("Active Cases", f"{active:,.0f}")
    
    st.markdown("---")
    st.subheader("Global Case Distribution & Trends")
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        # Pie Chart: Proportions of Active, Recovered, and Deaths
        fig1, ax1 = plt.subplots(figsize=(6, 5))
        labels = ['Active Cases', 'Recovered Cases', 'Reported Deaths']
        sizes = [active, recovered, deaths]
        colors = ['#ff9999', '#66b3ff', '#ffcc99']
        ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90, textprops={'fontsize': 10})
        ax1.axis('equal')
        ax1.set_title("Global Cases Distribution", fontsize=12, fontweight='bold', pad=12)
        st.pyplot(fig1)
        st.caption("Distribution Breakdown: Proportional share of active cases, recoveries, and deaths worldwide.")
        
    with col_chart2:
        # Line Chart Subplots: Global Trends Over Time
        # Plotting Confirmed, Recovered, and Deaths on separate subplots
        # ensures each scale is clearly legible.
        daily_global = worldwide_analysis.get_worldwide_daily_trends(df)

        fig2, (ax_conf, ax_rec, ax_dth) = plt.subplots(3, 1, figsize=(6, 8.5))

        ax_conf.plot(daily_global["Date"], daily_global["Confirmed"], color='#1E88E5', linewidth=1.8)
        ax_conf.set_title("Confirmed Cases Over Time", fontsize=11, fontweight='bold')
        ax_conf.set_xlabel("Date (Timeline)", fontsize=9, fontweight='semibold')
        ax_conf.set_ylabel("Confirmed Cases", fontsize=9, fontweight='semibold')
        ax_conf.grid(True, linestyle="--", alpha=0.4)
        ax_conf.tick_params(axis='x', rotation=30, labelsize=8)
        ax_conf.tick_params(axis='y', labelsize=8)

        ax_rec.plot(daily_global["Date"], daily_global["Recovered"], color='#43A047', linewidth=1.8)
        ax_rec.set_title("Recovered Cases Over Time", fontsize=11, fontweight='bold')
        ax_rec.set_xlabel("Date (Timeline)", fontsize=9, fontweight='semibold')
        ax_rec.set_ylabel("Recovered Cases", fontsize=9, fontweight='semibold')
        ax_rec.grid(True, linestyle="--", alpha=0.4)
        ax_rec.tick_params(axis='x', rotation=30, labelsize=8)
        ax_rec.tick_params(axis='y', labelsize=8)

        ax_dth.plot(daily_global["Date"], daily_global["Deaths"], color='#E53935', linewidth=1.8)
        ax_dth.set_title("Deaths Over Time", fontsize=11, fontweight='bold')
        ax_dth.set_xlabel("Date (Timeline)", fontsize=9, fontweight='semibold')
        ax_dth.set_ylabel("Reported Deaths", fontsize=9, fontweight='semibold')
        ax_dth.grid(True, linestyle="--", alpha=0.4)
        ax_dth.tick_params(axis='x', rotation=30, labelsize=8)
        ax_dth.tick_params(axis='y', labelsize=8)

        plt.tight_layout()
        st.pyplot(fig2)
        
    # Execute NumPy Demo silently in the background
    demonstrate_numpy_and_preprocessing(latest_data["Confirmed"].values)
    
    st.markdown("---")
    # Bottom Back button for convenience after scrolling through charts
    render_back_button(location_key="worldwide_dash_bottom")


# ==============================================================================
# ROUTE 3: WORLDWIDE REPORT PAGE
# ------------------------------------------------------------------------------
# Displays top 10 countries table, statistical box plot and logarithmic
# case distribution histogram.
# ==============================================================================
elif st.session_state["current_page"] == "Worldwide Report":
    
    # Navigation Header: Back Button & Page Breadcrumbs
    nav_col1, nav_col2 = st.columns([1, 4])
    with nav_col1:
        render_back_button(location_key="worldwide_rep_top")
    with nav_col2:
        st.caption("Navigation: 🏠 Main Menu > 📋 Worldwide Report")
        
    st.header("📋 Worldwide Report")
    st.write(f"Comprehensive report based on latest recorded date: **{latest_date.strftime('%Y-%m-%d')}**")
    st.markdown("---")
    
    # --------------------------------------------------------------------------
    # MODULE 2 USAGE: Top Countries Ranking
    # --------------------------------------------------------------------------
    # Extract the top 10 nations sorted by confirmed cases using Module 2.
    # --------------------------------------------------------------------------
    top_countries = worldwide_analysis.get_top_confirmed_countries(latest_data, n=10)
    
    st.subheader("Top 10 Countries by Confirmed Cases")
    st.dataframe(top_countries, use_container_width=True)
    
    # Statistical Distribution Analysis: Box Plot & Histogram
    st.markdown("---")
    st.subheader("Statistical Distributions")
    col_chart3, col_chart4 = st.columns(2)
    
    with col_chart3:
        # Box Plot of Confirmed Cases for Top 10 Countries
        fig3, ax3 = plt.subplots(figsize=(6, 4.5))
        ax3.boxplot(
            top_countries["Confirmed"].dropna(),
            patch_artist=True,
            boxprops=dict(facecolor='#BBDEFB', color='#1976D2'),
            medianprops=dict(color='#D32F2F', linewidth=2)
        )
        ax3.set_title("Box Plot: Confirmed Cases (Top 10 Nations)", fontsize=11, fontweight='bold', pad=10)
        ax3.set_xlabel("Top 10 Ranked Nations (X-Axis)", fontsize=10, fontweight='semibold')
        ax3.set_ylabel("Confirmed Cases Count (Y-Axis)", fontsize=10, fontweight='semibold')
        ax3.set_xticklabels(["Top 10 Countries"])
        ax3.grid(True, linestyle="--", alpha=0.4, axis='y')
        st.pyplot(fig3)
        
    with col_chart4:
        # Histogram: Confirmed cases distribution across all records with log scale
        fig4, ax4 = plt.subplots(figsize=(6, 4.5))
        ax4.hist(latest_data["Confirmed"].dropna(), bins=20, color='#64B5F6', edgecolor='#1565C0')
        ax4.set_title("Histogram: Confirmed Cases Distribution", fontsize=11, fontweight='bold', pad=10)
        ax4.set_xlabel("Confirmed Cases Range (X-Axis)", fontsize=10, fontweight='semibold')
        ax4.set_ylabel("Frequency of Records - Log Scale (Y-Axis)", fontsize=10, fontweight='semibold')
        ax4.set_yscale("log")
        ax4.grid(True, linestyle="--", alpha=0.4)
        st.pyplot(fig4)
        
    st.markdown("---")
    # Bottom Back button
    render_back_button(location_key="worldwide_rep_bottom")


# ==============================================================================
# ROUTE 4: COUNTRY ANALYSIS PAGE
# ------------------------------------------------------------------------------
# Allows selecting any country to inspect specific KPIs (Confirmed, Deaths,
# Recovered, Active) and 3-panel chronological trajectory subplots.
# ==============================================================================
elif st.session_state["current_page"] == "Country Analysis":
    
    # Navigation Header: Back Button & Page Breadcrumbs
    nav_col1, nav_col2 = st.columns([1, 4])
    with nav_col1:
        render_back_button(location_key="country_analysis_top")
    with nav_col2:
        st.caption("Navigation: 🏠 Main Menu > 🌎 Country Analysis")
        
    st.header("🌎 Country Analysis")
    st.write("Detailed country-level breakdown and longitudinal progression analysis.")
    st.markdown("---")
    
    # Country Dropdown Selector
    countries = sorted(df["Country/Region"].dropna().unique())
    selected_country = st.selectbox("Select Country to Analyze", countries, key="country_select")
    
    # Filter dataset for the selected country
    country_data = df[df["Country/Region"] == selected_country]
    c_latest = country_data[country_data["Date"] == country_data["Date"].max()]
    
    # Calculate country-level metric totals
    c_conf = c_latest["Confirmed"].sum()
    c_dead = c_latest["Deaths"].sum()
    c_rec = c_latest["Recovered"].sum()
    c_act = c_latest["Active"].sum()
    
    # Display Country Metrics
    st.write(f"### Current Statistics for {selected_country}")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Confirmed Cases", f"{c_conf:,.0f}")
    c2.metric("Deaths", f"{c_dead:,.0f}")
    c3.metric("Recovered", f"{c_rec:,.0f}")
    c4.metric("Active Cases", f"{c_act:,.0f}")
    
    # Chronological Trend Subplots
    st.markdown("---")
    st.subheader(f"Historical Trend Subplots: {selected_country}")
    daily_c = country_data.groupby("Date")[["Confirmed", "Recovered", "Deaths"]].sum().reset_index()
    
    fig5, (ax_c1, ax_c2, ax_c3) = plt.subplots(3, 1, figsize=(8, 10))
    ax_c1.plot(daily_c["Date"], daily_c["Confirmed"], color='#1E88E5', linewidth=1.8)
    ax_c1.set_title(f"{selected_country}: Confirmed Cases Trend", fontsize=11, fontweight='bold')
    ax_c1.set_xlabel("Date (Timeline)", fontsize=9, fontweight='semibold')
    ax_c1.set_ylabel("Confirmed Cases", fontsize=9, fontweight='semibold')
    ax_c1.grid(True, linestyle="--", alpha=0.4)
    ax_c1.tick_params(axis='x', rotation=30, labelsize=8)
    ax_c1.tick_params(axis='y', labelsize=8)
    
    ax_c2.plot(daily_c["Date"], daily_c["Recovered"], color='#43A047', linewidth=1.8)
    ax_c2.set_title(f"{selected_country}: Recovered Cases Trend", fontsize=11, fontweight='bold')
    ax_c2.set_xlabel("Date (Timeline)", fontsize=9, fontweight='semibold')
    ax_c2.set_ylabel("Recovered Cases", fontsize=9, fontweight='semibold')
    ax_c2.grid(True, linestyle="--", alpha=0.4)
    ax_c2.tick_params(axis='x', rotation=30, labelsize=8)
    ax_c2.tick_params(axis='y', labelsize=8)
    
    ax_c3.plot(daily_c["Date"], daily_c["Deaths"], color='#E53935', linewidth=1.8)
    ax_c3.set_title(f"{selected_country}: Deaths Trend", fontsize=11, fontweight='bold')
    ax_c3.set_xlabel("Date (Timeline)", fontsize=9, fontweight='semibold')
    ax_c3.set_ylabel("Reported Deaths", fontsize=9, fontweight='semibold')
    ax_c3.grid(True, linestyle="--", alpha=0.4)
    ax_c3.tick_params(axis='x', rotation=30, labelsize=8)
    ax_c3.tick_params(axis='y', labelsize=8)
    
    plt.tight_layout()
    st.pyplot(fig5)
    
    st.markdown("---")
    # Bottom Back button
    render_back_button(location_key="country_analysis_bottom")


# ==============================================================================
# ROUTE 5: STATE OR PROVINCE ANALYSIS PAGE
# ------------------------------------------------------------------------------
# Enables province/state level filtering and analysis, featuring metrics
# and Confirmed vs Deaths scatter plot correlations.
# ==============================================================================
elif st.session_state["current_page"] == "State or Province Analysis":
    
    # Navigation Header: Back Button & Page Breadcrumbs
    nav_col1, nav_col2 = st.columns([1, 4])
    with nav_col1:
        render_back_button(location_key="state_analysis_top")
    with nav_col2:
        st.caption("Navigation: 🏠 Main Menu > 🏙️ State or Province Analysis")
        
    st.header("🏙️ State or Province Analysis")
    st.write("Regional data exploration for countries with state/province breakdowns.")
    st.markdown("---")
    
    # Filter only countries that contain documented state/province entries
    countries_with_states = df[df["Province/State"] != "Unknown"]["Country/Region"].unique()
    
    col_sel1, col_sel2 = st.columns(2)
    with col_sel1:
        st_country = st.selectbox("Select Country", sorted(countries_with_states), key="state_country_select")
        
    state_data_full = df[df["Country/Region"] == st_country]
    states = sorted(state_data_full["Province/State"].unique())
    
    with col_sel2:
        st_state = st.selectbox("Select State / Province", states, key="state_select")
    
    # Filter data for chosen state/province
    state_data = state_data_full[state_data_full["Province/State"] == st_state]
    s_latest = state_data[state_data["Date"] == state_data["Date"].max()]
    
    st.write(f"### Statistics for **{st_state}**, {st_country}")
    
    # Display State Metrics
    sc1, sc2, sc3, sc4 = st.columns(4)
    sc1.metric("Confirmed", f"{s_latest['Confirmed'].sum():,.0f}")
    sc2.metric("Deaths", f"{s_latest['Deaths'].sum():,.0f}")
    sc3.metric("Recovered", f"{s_latest['Recovered'].sum():,.0f}")
    sc4.metric("Active", f"{s_latest['Active'].sum():,.0f}")
    
    # Scatter Plot: Confirmed Cases vs Deaths Correlation
    st.markdown("---")
    st.subheader(f"Scatter Plot: Confirmed vs Deaths in {st_state}")
    fig6, ax6 = plt.subplots(figsize=(7, 4.5))
    ax6.scatter(state_data["Confirmed"], state_data["Deaths"], alpha=0.6, color='#7B1FA2', edgecolors='none')
    ax6.set_xlabel("Confirmed Cases (X-Axis)", fontsize=10, fontweight='semibold')
    ax6.set_ylabel("Reported Deaths (Y-Axis)", fontsize=10, fontweight='semibold')
    ax6.set_title(f"Confirmed Cases vs Deaths Correlation ({st_state})", fontsize=11, fontweight='bold', pad=10)
    ax6.grid(True, linestyle="--", alpha=0.4)
    st.pyplot(fig6)
    
    st.markdown("---")
    # Bottom Back button
    render_back_button(location_key="state_analysis_bottom")


# ==============================================================================
# ROUTE 6: COMPARISON AND TREND PAGE
# ------------------------------------------------------------------------------
# Side-by-side comparative analysis between two countries with comparative
# bar charts and concatenated data inspection.
# ==============================================================================
elif st.session_state["current_page"] == "Comparison and Trend":
    
    # Navigation Header: Back Button & Page Breadcrumbs
    nav_col1, nav_col2 = st.columns([1, 4])
    with nav_col1:
        render_back_button(location_key="comp_trend_top")
    with nav_col2:
        st.caption("Navigation: 🏠 Main Menu > 📊 Comparison and Trend")
        
    st.header("📊 Comparison and Trend")
    st.write("Compare COVID-19 pandemic impacts across any two selected countries.")
    st.markdown("---")
    
    countries = sorted(df["Country/Region"].dropna().unique())
    comp_c1, comp_c2 = st.columns(2)
    
    with comp_c1:
        country1 = st.selectbox(
            "Select First Country",
            countries,
            index=countries.index("India") if "India" in countries else 0,
            key="comp_country1"
        )
    with comp_c2:
        country2 = st.selectbox(
            "Select Second Country",
            countries,
            index=countries.index("Canada") if "Canada" in countries else min(1, len(countries) - 1),
            key="comp_country2"
        )
        
    if country1 == country2:
        st.warning("⚠️ Please select two different countries to generate a comparative analysis.")
    else:
        d1 = df[df["Country/Region"] == country1]
        d2 = df[df["Country/Region"] == country2]
        
        # Comparative Bar Chart
        st.subheader(f"Comparison of Latest Cases: {country1} vs {country2}")
        
        latest_c1 = d1[d1["Date"] == d1["Date"].max()][["Confirmed", "Recovered", "Deaths"]].sum()
        latest_c2 = d2[d2["Date"] == d2["Date"].max()][["Confirmed", "Recovered", "Deaths"]].sum()
        
        comp_df = pd.DataFrame({
            country1: latest_c1,
            country2: latest_c2
        }).T
        
        fig7, ax7 = plt.subplots(figsize=(8, 5))
        comp_df.plot(kind='bar', ax=ax7, colormap="viridis")
        ax7.set_title(f"Cases Comparison: {country1} vs {country2}", fontsize=11, fontweight='bold', pad=10)
        ax7.set_xlabel("Selected Countries (X-Axis)", fontsize=10, fontweight='semibold')
        ax7.set_ylabel("Number of Cases (Y-Axis)", fontsize=10, fontweight='semibold')
        ax7.grid(True, linestyle="--", alpha=0.4, axis='y')
        plt.xticks(rotation=0)
        plt.tight_layout()
        st.pyplot(fig7)
        
        # Pandas Concatenation Demonstration
        st.markdown("---")
        st.subheader("Recent Data Records (Concatenation Demo)")
        concat_demo = pd.concat([d1.tail(1), d2.tail(1)])
        st.dataframe(
            concat_demo[["Date", "Country/Region", "Confirmed", "Recovered", "Deaths", "Active"]],
            use_container_width=True
        )
        
    st.markdown("---")
    # Bottom Back button
    render_back_button(location_key="comp_trend_bottom")
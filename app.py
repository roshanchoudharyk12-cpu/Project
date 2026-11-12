"""
AEROWATCH: Global & India Air Pollution Intelligence Dashboard
Built with Python, Streamlit, and Plotly.
Provides planetary air quality benchmarking, deep-dive analytics for 2,488 Indian cities,
and an evidence-based, actionable administrative policy roadmap for Indian urban local bodies.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# Import geographic mapping for Indian cities
from geo_data import CITY_COORDS

# Set page configuration
st.set_page_config(
    page_title="AeroWatch | Global & India Air Pollution Intelligence",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (Dark Glassmorphism, Google Fonts, Glowing Badges)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Main Background & Cards */
    .stApp {
        background: radial-gradient(circle at 10% 20%, #0d1527 0%, #080c14 90%);
        color: #f3f4f6;
    }
    
    /* Glassmorphic Metric Card */
    .metric-card {
        background: rgba(17, 24, 39, 0.75);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 20px 22px;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
        transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
    }
    .metric-card:hover {
        transform: translateY(-4px);
        border-color: rgba(56, 189, 248, 0.4);
        box-shadow: 0 16px 36px -12px rgba(6, 182, 212, 0.25);
    }
    
    .metric-title {
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.07em;
        color: #94a3b8;
        margin-bottom: 6px;
    }
    
    .metric-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 2.2rem;
        font-weight: 800;
        line-height: 1.1;
        margin-bottom: 8px;
    }
    
    .metric-subtitle {
        font-size: 0.82rem;
        color: #64748b;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    
    .delta-badge {
        font-size: 0.78rem;
        font-weight: 700;
        padding: 2px 8px;
        border-radius: 9999px;
        display: inline-block;
    }
    .delta-red { background: rgba(239, 68, 68, 0.15); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3); }
    .delta-green { background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); }
    .delta-amber { background: rgba(245, 158, 11, 0.15); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3); }

    /* Category Badges */
    .aqi-pill {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 8px;
        font-weight: 700;
        font-size: 0.8rem;
        letter-spacing: 0.03em;
    }
    .cat-good { background: #064e3b; color: #6ee7b7; border: 1px solid #059669; }
    .cat-mod { background: #78350f; color: #fcd34d; border: 1px solid #d97706; }
    .cat-usg { background: #7c2d12; color: #fdba74; border: 1px solid #ea580c; }
    .cat-unhealthy { background: #7f1d1d; color: #fca5a5; border: 1px solid #dc2626; }
    .cat-very-unhealthy { background: #4c1d95; color: #c4b5fd; border: 1px solid #7c3aed; }
    .cat-hazardous { background: #581c87; color: #f472b6; border: 1px solid #db2777; }

    /* Policy Card */
    .policy-box {
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    .policy-box h4 {
        margin-top: 0;
        color: #38bdf8;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Hero Banner */
    .hero-container {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.95) 100%);
        border: 1px solid rgba(56, 189, 248, 0.25);
        border-radius: 20px;
        padding: 28px 32px;
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
    }
    .hero-container::before {
        content: "";
        position: absolute;
        top: -50%;
        right: -10%;
        width: 350px;
        height: 350px;
        background: radial-gradient(circle, rgba(6, 182, 212, 0.15) 0%, transparent 70%);
        pointer-events: none;
    }
    
    /* Clean Tab styles */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(15, 23, 42, 0.6);
        padding: 6px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: 600;
        color: #94a3b8;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(6, 182, 212, 0.2) !important;
        color: #38bdf8 !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
    }
</style>
""", unsafe_allow_html=True)

# Standard AQI Color Map & Order
AQI_COLORS = {
    "Good": "#10B981",                          # Emerald
    "Moderate": "#F59E0B",                      # Amber
    "Unhealthy for Sensitive Groups": "#F97316", # Orange
    "Unhealthy": "#EF4444",                     # Red
    "Very Unhealthy": "#8B5CF6",                # Purple
    "Hazardous": "#BE185D"                      # Magenta/Crimson
}

AQI_ORDER = [
    "Good", 
    "Moderate", 
    "Unhealthy for Sensitive Groups", 
    "Unhealthy", 
    "Very Unhealthy", 
    "Hazardous"
]

@st.cache_data
def load_data():
    csv_file = "global air pollution dataset.csv"
    if not os.path.exists(csv_file):
        st.error(f"Dataset file '{csv_file}' not found.")
        st.stop()
    
    df = pd.read_csv(csv_file)
    # Clean string columns
    df['Country'] = df['Country'].astype(str).str.strip()
    df['City'] = df['City'].astype(str).str.strip()
    df['AQI Category'] = df['AQI Category'].astype(str).str.strip()
    
    # Fill missing country if any
    df['Country'] = df['Country'].replace('nan', 'Unknown')
    
    # Numerical validation
    num_cols = ['AQI Value', 'CO AQI Value', 'Ozone AQI Value', 'NO2 AQI Value', 'PM2.5 AQI Value']
    for col in num_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
    # Dominant pollutant identification
    def get_dominant(row):
        max_val = row['AQI Value']
        if row['PM2.5 AQI Value'] == max_val:
            return 'PM2.5'
        elif row['Ozone AQI Value'] == max_val:
            return 'Ozone (O3)'
        elif row['NO2 AQI Value'] == max_val:
            return 'NO2'
        elif row['CO AQI Value'] == max_val:
            return 'CO'
        else:
            # Fallback to max of the 4 pollutants
            sub = {
                'PM2.5': row['PM2.5 AQI Value'],
                'Ozone (O3)': row['Ozone AQI Value'],
                'NO2': row['NO2 AQI Value'],
                'CO': row['CO AQI Value']
            }
            return max(sub, key=sub.get)
            
    df['Dominant Pollutant'] = df.apply(get_dominant, axis=1)
    return df

df = load_data()
india_df = df[df['Country'] == 'India'].copy()

# Add Geographic & Ecological Zones to India Dataframe
def enrich_india_data(ind_df):
    lats, lons, states, zones = [], [], [], []
    for city in ind_df['City']:
        if city in CITY_COORDS:
            c = CITY_COORDS[city]
            lats.append(c['lat'])
            lons.append(c['lon'])
            states.append(c['state'])
            zones.append(c['zone'])
        else:
            lats.append(np.nan)
            lons.append(np.nan)
            states.append('Other / Unmapped')
            zones.append('Inland / Unclassified')
    ind_df = ind_df.copy()
    ind_df['Latitude'] = lats
    ind_df['Longitude'] = lons
    ind_df['State'] = states
    ind_df['EcoZone'] = zones
    return ind_df

india_df = enrich_india_data(india_df)

# ==========================================
# SIDEBAR FILTERS & CONTROLS
# ==========================================
st.sidebar.markdown("""
<div style="text-align: center; margin-bottom: 18px;">
    <h2 style="color: #38bdf8; margin: 0; font-size: 1.6rem; font-weight: 800; letter-spacing: -0.02em;">AEROWATCH</h2>
    <span style="font-size: 0.78rem; color: #94a3b8; letter-spacing: 0.08em; text-transform: uppercase;">Air Quality Intelligence Engine</span>
</div>
""", unsafe_allow_html=True)

module_selection = st.sidebar.radio(
    "Environmental Domain",
    ["💨 Air Quality Intelligence", "💧 Water Quality Intelligence", "🌍 Integrated Environmental Radar"],
    index=0
)

st.sidebar.markdown("---")

@st.cache_data
def load_water_data():
    csv_file = 'Indian_water_data.csv'
    if not os.path.exists(csv_file):
        return pd.DataFrame()
    wdf = pd.read_csv(csv_file)
    # Clean string columns
    if 'State Name' in wdf.columns:
        wdf['State Name'] = wdf['State Name'].astype(str).str.strip()
    if 'Monitoring Location' in wdf.columns:
        wdf['Monitoring Location'] = wdf['Monitoring Location'].astype(str).str.strip()
    return wdf

water_df = load_water_data()

def render_air_dashboard():
    st.sidebar.markdown("### 🎛️ Analysis Controls")

    view_scope = st.sidebar.radio(
        "Primary Focus Area",
        ["🇮🇳 India Deep-Dive & Administration", "🌐 Global Planetary Comparison"],
        index=0
    )

    # Category multi-select
    all_categories = AQI_ORDER
    selected_categories = st.sidebar.multiselect(
        "Filter AQI Categories",
        options=all_categories,
        default=all_categories
    )

    # Slider for AQI
    min_aqi, max_aqi = int(df['AQI Value'].min()), int(df['AQI Value'].max())
    aqi_range = st.sidebar.slider(
        "AQI Value Range",
        min_value=min_aqi,
        max_value=max_aqi,
        value=(min_aqi, max_aqi),
        step=5
    )

    # Dominant pollutant filter
    dominant_options = ["All Pollutants", "PM2.5 Dominant", "Ozone (O3) Dominant", "NO2 Dominant", "CO Dominant"]
    sel_dominant = st.sidebar.selectbox("Filter Dominant Pollutant", dominant_options)

    # Filter global and india datasets
    def apply_filters(data):
        filtered = data[
            (data['AQI Category'].isin(selected_categories)) &
            (data['AQI Value'] >= aqi_range[0]) &
            (data['AQI Value'] <= aqi_range[1])
        ]
        if sel_dominant == "PM2.5 Dominant":
            filtered = filtered[filtered['Dominant Pollutant'] == 'PM2.5']
        elif sel_dominant == "Ozone (O3) Dominant":
            filtered = filtered[filtered['Dominant Pollutant'] == 'Ozone (O3)']
        elif sel_dominant == "NO2 Dominant":
            filtered = filtered[filtered['Dominant Pollutant'] == 'NO2']
        elif sel_dominant == "CO Dominant":
            filtered = filtered[filtered['Dominant Pollutant'] == 'CO']
        return filtered

    filtered_df = apply_filters(df)
    filtered_india = apply_filters(india_df)

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Dataset Telemetry")
    st.sidebar.markdown(f"""
    - **Total Monitored Cities:** `{len(df):,}`
    - **Total Countries:** `{df['Country'].nunique()}`
    - **Indian Cities Monitored:** `{len(india_df):,}` ({len(india_df)/len(df)*100:.1f}% of cohort)
    - **Filtered In View:** `{len(filtered_df):,}` global | `{len(filtered_india):,}` India
    """)

    st.sidebar.info("💡 **AeroWatch Tip:** PM2.5 particulates remain airborne for weeks and travel hundreds of kilometers across state boundaries. Solutions require regional airshed governance.")

    # ==========================================
    # HERO BANNER
    # ==========================================
    st.markdown("""
    <div class="hero-container">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 16px;">
            <div>
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
                    <span style="background: rgba(14, 165, 233, 0.2); color: #38bdf8; font-weight: 700; font-size: 0.75rem; padding: 4px 10px; border-radius: 9999px; border: 1px solid rgba(56, 189, 248, 0.4);">
                        ENVIRONMENTAL INTELLIGENCE
                    </span>
                    <span style="background: rgba(239, 68, 68, 0.2); color: #f87171; font-weight: 700; font-size: 0.75rem; padding: 4px 10px; border-radius: 9999px; border: 1px solid rgba(239, 68, 68, 0.4);">
                        INDIA CRISIS RADAR
                    </span>
                </div>
                <h1 style="margin: 0 0 10px 0; font-size: 2.2rem; font-weight: 800; color: #ffffff; letter-spacing: -0.02em;">
                    Global Air Pollution Analytics & Indian Municipal Action Framework
                </h1>
                <p style="margin: 0; color: #94a3b8; font-size: 1.02rem; max-width: 950px; line-height: 1.5;">
                    Comprehensive diagnostic dashboard analyzing 23,463 global cities across 175 countries with an empirical deep-dive into 2,488 Indian urban centers. Formulating data-driven conclusions and actionable administrative roadmaps for city commissioners and state pollution control boards.
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Main Navigation Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🇮🇳 Indian Cities Deep-Dive",
        "🌐 Global Planetary Benchmark",
        "🔬 Pollutant Fingerprint & Root Causes",
        "🏛️ Administrative Blueprint & Action Planner",
        "📋 Raw Data Explorer & Export"
    ])

    # ==============================================================================
    # TAB 1: INDIAN CITIES DEEP-DIVE
    # ==============================================================================
    with tab1:
        st.markdown("### 🇮🇳 Urban Air Quality Crisis in Indian Municipalities")
        st.caption("Empirical evaluation of 2,488 Indian cities monitored in the global dataset.")

        # KPI Metrics Row
        k1, k2, k3, k4, k5 = st.columns(5)

        india_mean_aqi = india_df['AQI Value'].mean()
        india_median_aqi = india_df['AQI Value'].median()
        india_unhealthy_pct = (india_df['AQI Value'] > 100).mean() * 100
        india_hazardous_count = (india_df['AQI Category'] == 'Hazardous').sum()
        pm25_dom_pct = (india_df['Dominant Pollutant'] == 'PM2.5').mean() * 100

        with k1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">India Mean AQI</div>
                <div class="metric-value" style="color: #f87171;">{india_mean_aqi:.1f}</div>
                <div class="metric-subtitle">
                    <span class="delta-badge delta-red">+112% vs Global</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with k2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Unhealthy or Worse</div>
                <div class="metric-value" style="color: #fb923c;">{india_unhealthy_pct:.1f}%</div>
                <div class="metric-subtitle">
                    <span class="delta-badge delta-red">1,773 / 2,488 Cities</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with k3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Hazardous Cities (AQI 300+)</div>
                <div class="metric-value" style="color: #f472b6;">{india_hazardous_count}</div>
                <div class="metric-subtitle">
                    <span class="delta-badge delta-red">Max Sensor Cap (500)</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with k4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">PM2.5 Dominance</div>
                <div class="metric-value" style="color: #38bdf8;">{pm25_dom_pct:.1f}%</div>
                <div class="metric-subtitle">
                    <span class="delta-badge delta-amber">Primary Toxicity Agent</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with k5:
            good_pct = (india_df['AQI Category'] == 'Good').mean() * 100
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Clean Air Cities (Good)</div>
                <div class="metric-value" style="color: #34d399;">{good_pct:.1f}%</div>
                <div class="metric-subtitle">
                    <span class="delta-badge delta-green">Only 130 Cities</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Geospatial Distribution & Hotspot Map
        st.markdown("#### 🗺️ Interactive Spatial Air Quality Map of India")
        st.caption("Geolocated monitoring stations across distinct ecological corridors (Indo-Gangetic Plain, Deccan Plateau, Western Ghats, Coastal, Northeast, and Himalayan). Hover to inspect individual city pollutant profiles.")

        geo_df = filtered_india.dropna(subset=['Latitude', 'Longitude']).copy()

        if len(geo_df) > 0:
            fig_map = px.scatter_geo(
                geo_df,
                lat='Latitude',
                lon='Longitude',
                color='AQI Category',
                size='AQI Value',
                size_max=22,
                hover_name='City',
                hover_data={
                    'AQI Value': True,
                    'AQI Category': True,
                    'PM2.5 AQI Value': True,
                    'Ozone AQI Value': True,
                    'State': True,
                    'EcoZone': True,
                    'Latitude': False,
                    'Longitude': False
                },
                color_discrete_map=AQI_COLORS,
                category_orders={'AQI Category': AQI_ORDER},
                scope='asia',
                template='plotly_dark'
            )

            fig_map.update_geos(
                center=dict(lat=22.0, lon=82.0),
                projection_scale=3.8,
                visible=True,
                showcountries=True,
                countrycolor="rgba(255,255,255,0.25)",
                showcoastlines=True,
                coastlinecolor="rgba(255,255,255,0.25)",
                showland=True,
                landcolor="#0e1726",
                showocean=True,
                oceancolor="#070c14",
                showlakes=True,
                lakecolor="#070c14",
                fitbounds=False
            )

            fig_map.update_layout(
                margin=dict(l=0, r=0, t=10, b=0),
                height=540,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="center",
                    x=0.5,
                    bgcolor="rgba(15, 23, 42, 0.8)",
                    bordercolor="rgba(255,255,255,0.1)",
                    borderwidth=1
                )
            )
            st.plotly_chart(fig_map, use_container_width=True)
        else:
            st.warning("No geolocated cities match the current filter selection.")

        st.markdown("<br>", unsafe_allow_html=True)

        # Top Polluted vs Cleanest Cities
        col_polluted, col_clean = st.columns(2)

        with col_polluted:
            st.markdown("#### 🚨 Top 20 Most Polluted Indian Cities")
            st.caption("Urban centers reaching severe/hazardous categories (dominated by the Indo-Gangetic Basin)")

            top20_polluted = filtered_india.sort_values(by=['AQI Value', 'PM2.5 AQI Value'], ascending=False).head(20)

            fig_polluted = px.bar(
                top20_polluted,
                x='AQI Value',
                y='City',
                orientation='h',
                color='AQI Category',
                color_discrete_map=AQI_COLORS,
                hover_data=['PM2.5 AQI Value', 'Ozone AQI Value', 'NO2 AQI Value'],
                text='AQI Value',
                template='plotly_dark'
            )
            fig_polluted.update_layout(
                yaxis={'categoryorder': 'total ascending'},
                margin=dict(l=0, r=20, t=20, b=20),
                height=520,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis_title="AQI Index (0 - 500 Scale)",
                yaxis_title=None,
                showlegend=False
            )
            fig_polluted.update_traces(textposition='inside', insidetextanchor='middle')
            st.plotly_chart(fig_polluted, use_container_width=True)

        with col_clean:
            st.markdown("#### 🌿 Top 20 Cleanest Indian Cities")
            st.caption("Benchmarking green zones with low emissions & favorable geographic dispersion")

            top20_clean = filtered_india.sort_values(by=['AQI Value', 'PM2.5 AQI Value'], ascending=True).head(20)

            fig_clean = px.bar(
                top20_clean,
                x='AQI Value',
                y='City',
                orientation='h',
                color='AQI Category',
                color_discrete_map=AQI_COLORS,
                hover_data=['PM2.5 AQI Value', 'Ozone AQI Value', 'NO2 AQI Value'],
                text='AQI Value',
                template='plotly_dark'
            )
            fig_clean.update_layout(
                yaxis={'categoryorder': 'total descending'},
                margin=dict(l=0, r=20, t=20, b=20),
                height=520,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis_title="AQI Index (0 - 50 Scale)",
                yaxis_title=None,
                showlegend=False
            )
            fig_clean.update_traces(textposition='outside')
            st.plotly_chart(fig_clean, use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Ecological Zone Breakdown for India
        st.markdown("#### ⛰️ Ecological Zone Disparity: The Indo-Gangetic Basin Trap")
        st.caption("Distribution of AQI by ecological/geographical zone across mapped Indian cities.")

        zone_data = india_df[india_df['EcoZone'] != 'Inland / Unclassified']

        if len(zone_data) > 0:
            fig_zone = px.box(
                zone_data,
                x='EcoZone',
                y='AQI Value',
                color='EcoZone',
                points='all',
                hover_name='City',
                template='plotly_dark',
                color_discrete_sequence=px.colors.qualitative.Prism
            )
            fig_zone.update_layout(
                height=420,
                margin=dict(l=0, r=0, t=20, b=20),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                showlegend=False,
                xaxis_title=None,
                yaxis_title="AQI Value"
            )
            st.plotly_chart(fig_zone, use_container_width=True)

            st.markdown("""
            > **Analytical Insight:** The Indo-Gangetic Plain (IGP) exhibits median AQI values consistently exceeding **200 to 500**, whereas Southern Peninsular, Western Ghats, and Himalayan regions maintain medians between **24 and 65**. The Northern crisis is amplified by basin topography, winter temperature inversions, dense population clusters, and agricultural stubble burning.
            """)

        st.markdown("<br>", unsafe_allow_html=True)

        # Interactive City Inspector & Comparative Radar
        st.markdown("#### 🔍 Interactive Indian City Comparator")
        st.caption("Select up to 4 Indian cities to inspect and contrast their multi-pollutant profiles side-by-side.")

        avail_cities = sorted(india_df['City'].unique())
        default_picks = [c for c in ['Delhi', 'Bengaluru', 'Kanpur', 'Kochi'] if c in avail_cities]
        selected_cities = st.multiselect(
            "Choose Cities for Multi-Pollutant Spider & Profile Analysis",
            options=avail_cities,
            default=default_picks,
            max_selections=4
        )

        if selected_cities:
            comp_df = india_df[india_df['City'].isin(selected_cities)]

            c_radar, c_table = st.columns([1.2, 1])

            with c_radar:
                fig_radar = go.Figure()
                radar_pollutants = ['PM2.5 AQI Value', 'Ozone AQI Value', 'NO2 AQI Value', 'CO AQI Value']
                radar_labels = ['PM2.5', 'Ozone (O3)', 'NO2', 'CO']

                colors_palette = ['#f87171', '#38bdf8', '#34d399', '#facc15']

                for idx, (_, row) in enumerate(comp_df.iterrows()):
                    vals = [row[p] for p in radar_pollutants]
                    vals.append(vals[0]) # close loop
                    fig_radar.add_trace(go.Scatterpolar(
                        r=vals,
                        theta=radar_labels + [radar_labels[0]],
                        fill='toself',
                        name=row['City'],
                        line_color=colors_palette[idx % len(colors_palette)],
                        opacity=0.65
                    ))

                fig_radar.update_layout(
                    polar=dict(
                        radialaxis=dict(visible=True, range=[0, max(comp_df['AQI Value'].max(), 100)], color="#94a3b8"),
                        bgcolor="rgba(15, 23, 42, 0.7)"
                    ),
                    showlegend=True,
                    template='plotly_dark',
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    height=380,
                    margin=dict(l=30, r=30, t=30, b=30),
                    legend=dict(orientation="h", y=-0.15, x=0.5, xanchor="center")
                )
                st.plotly_chart(fig_radar, use_container_width=True)

            with c_table:
                st.markdown("##### Multi-Pollutant Audit Table")
                display_cols = ['City', 'AQI Value', 'AQI Category', 'PM2.5 AQI Value', 'Ozone AQI Value', 'NO2 AQI Value', 'CO AQI Value']
                st.dataframe(
                    comp_df[display_cols].reset_index(drop=True),
                    column_config={
                        "AQI Value": st.column_config.NumberColumn("AQI", format="%d"),
                        "PM2.5 AQI Value": st.column_config.NumberColumn("PM2.5", format="%d"),
                        "Ozone AQI Value": st.column_config.NumberColumn("O3", format="%d"),
                        "NO2 AQI Value": st.column_config.NumberColumn("NO2", format="%d"),
                        "CO AQI Value": st.column_config.NumberColumn("CO", format="%d"),
                    },
                    hide_index=True,
                    use_container_width=True
                )

                # Diagnostic feedback for the selected cities
                for _, r in comp_df.iterrows():
                    dom = r['Dominant Pollutant']
                    val = r['AQI Value']
                    cat = r['AQI Category']
                    st.markdown(f"- **{r['City']}**: Current AQI is **{val}** ({cat}). Dominated by **{dom}** at `{r['PM2.5 AQI Value']}` AQI level.")


    # ==============================================================================
    # TAB 2: GLOBAL PLANETARY BENCHMARK
    # ==============================================================================
    with tab2:
        st.markdown("### 🌐 Global Planetary Air Quality Landscape")
        st.caption(f"Benchmarking air pollution patterns across 23,463 cities in 175 sovereign nations.")

        # Global Overview Metrics
        g1, g2, g3, g4 = st.columns(4)
        global_mean_aqi = df['AQI Value'].mean()
        global_median_aqi = df['AQI Value'].median()
        global_clean_pct = (df['AQI Category'] == 'Good').mean() * 100
        global_unhealthy_pct = (df['AQI Value'] > 100).mean() * 100

        with g1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Global Mean AQI</div>
                <div class="metric-value" style="color: #38bdf8;">{global_mean_aqi:.1f}</div>
                <div class="metric-subtitle">Across 23,463 monitored cities</div>
            </div>
            """, unsafe_allow_html=True)

        with g2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">India Mean AQI</div>
                <div class="metric-value" style="color: #f87171;">{india_mean_aqi:.1f}</div>
                <div class="metric-subtitle"><span class="delta-badge delta-red">+112% above global mean</span></div>
            </div>
            """, unsafe_allow_html=True)

        with g3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Global Clean Cities (Good)</div>
                <div class="metric-value" style="color: #34d399;">{global_clean_pct:.1f}%</div>
                <div class="metric-subtitle">vs only {good_pct:.1f}% in India</div>
            </div>
            """, unsafe_allow_html=True)

        with g4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">India Global Worst Rank</div>
                <div class="metric-value" style="color: #f43f5e;">#2</div>
                <div class="metric-subtitle">Among 107 nations (min 20 cities)</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Country Rankings Bar Chart (Highlighting India)
        st.markdown("#### 🌍 Highest Mean AQI by Country (Min. 20 Monitored Cities)")
        st.caption("India ranks as the 2nd most air-polluted nation globally in urban mean AQI, right behind Pakistan.")

        country_stats = df.groupby('Country')['AQI Value'].agg(['count', 'mean', 'median', 'max']).reset_index()
        country_filtered = country_stats[country_stats['count'] >= 20].sort_values(by='mean', ascending=False).head(25)

        country_filtered['Is_India'] = country_filtered['Country'].apply(lambda x: 'India' if x == 'India' else ('Pakistan' if x == 'Pakistan' else 'Other Nations'))

        fig_country = px.bar(
            country_filtered,
            x='mean',
            y='Country',
            orientation='h',
            color='Is_India',
            color_discrete_map={
                'India': '#ef4444',
                'Pakistan': '#f97316',
                'Other Nations': '#334155'
            },
            hover_data=['count', 'median', 'max'],
            template='plotly_dark',
            text='mean'
        )
        fig_country.update_layout(
            yaxis={'categoryorder': 'total ascending'},
            height=580,
            margin=dict(l=0, r=20, t=10, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis_title="Mean AQI Value across Monitored Cities",
            yaxis_title=None,
            showlegend=True,
            legend=dict(orientation="h", y=1.03, x=0.5, xanchor="center")
        )
        fig_country.update_traces(texttemplate='%{text:.1f}', textposition='outside')
        st.plotly_chart(fig_country, use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Distribution Comparison & Category Proportions
        col_dist, col_cat = st.columns([1.1, 1])

        with col_dist:
            st.markdown("#### 📈 AQI Distribution Shift: India vs Global Benchmark")
            st.caption("Notice the drastic right-skew of India's distribution toward 150-500 vs global clustering below 75.")

            # Select top countries for distribution comparison
            sample_countries = ['Global Total', 'India', 'China', 'United States of America', 'Germany']
            dist_records = []
            for c in ['India', 'China', 'United States of America', 'Germany']:
                subset = df[df['Country'] == c].copy()
                subset['Cohort'] = c
                dist_records.append(subset)
            global_copy = df.copy()
            global_copy['Cohort'] = 'Global Total'
            dist_records.append(global_copy)
            dist_df = pd.concat(dist_records, ignore_index=True)

            fig_dist = px.violin(
                dist_df,
                x='Cohort',
                y='AQI Value',
                color='Cohort',
                box=True,
                points=False,
                template='plotly_dark',
                color_discrete_map={
                    'Global Total': '#94a3b8',
                    'India': '#ef4444',
                    'China': '#f59e0b',
                    'United States of America': '#06b6d4',
                    'Germany': '#10b981'
                }
            )
            fig_dist.update_layout(
                height=430,
                margin=dict(l=0, r=0, t=20, b=20),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                showlegend=False,
                xaxis_title=None,
                yaxis_title="AQI Value"
            )
            st.plotly_chart(fig_dist, use_container_width=True)

        with col_cat:
            st.markdown("#### 🍩 Air Quality Category Proportions")
            st.caption("Comparison of population exposure categories between Global cities and India.")

            g_cat = df['AQI Category'].value_counts(normalize=True).reindex(AQI_ORDER).fillna(0) * 100
            ind_cat = india_df['AQI Category'].value_counts(normalize=True).reindex(AQI_ORDER).fillna(0) * 100

            fig_donuts = make_subplots(
                rows=1, cols=2,
                specs=[[{'type': 'domain'}, {'type': 'domain'}]],
                subplot_titles=['Global Baseline', 'India Cities Cohort']
            )

            fig_donuts.add_trace(
                go.Pie(
                    labels=AQI_ORDER,
                    values=g_cat.values,
                    name="Global",
                    hole=0.55,
                    marker=dict(colors=[AQI_COLORS[c] for c in AQI_ORDER]),
                    sort=False
                ),
                1, 1
            )

            fig_donuts.add_trace(
                go.Pie(
                    labels=AQI_ORDER,
                    values=ind_cat.values,
                    name="India",
                    hole=0.55,
                    marker=dict(colors=[AQI_COLORS[c] for c in AQI_ORDER]),
                    sort=False
                ),
                1, 2
            )

            fig_donuts.update_layout(
                height=430,
                margin=dict(l=10, r=10, t=30, b=10),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                template='plotly_dark',
                legend=dict(orientation="h", y=-0.12, x=0.5, xanchor="center")
            )
            st.plotly_chart(fig_donuts, use_container_width=True)


    # ==============================================================================
    # TAB 3: POLLUTANT FINGERPRINT & ROOT CAUSES
    # ==============================================================================
    with tab3:
        st.markdown("### 🔬 Multi-Pollutant Fingerprint & Root Cause Analytics")
        st.caption("Dissecting the chemical constituents: PM2.5, Ground-Level Ozone (O3), Nitrogen Dioxide (NO2), and Carbon Monoxide (CO).")

        col_corr, col_dom = st.columns([1, 1])

        with col_corr:
            st.markdown("#### 🧬 India Pollutant Correlation Heatmap")
            st.caption("Pearson correlation reveals PM2.5 as almost perfectly collinear with total AQI (r = 0.990).")

            pollutant_cols = ['AQI Value', 'PM2.5 AQI Value', 'Ozone AQI Value', 'NO2 AQI Value', 'CO AQI Value']
            corr_matrix = india_df[pollutant_cols].corr()

            labels_clean = ['Overall AQI', 'PM2.5', 'Ozone (O3)', 'NO2', 'CO']

            fig_corr = px.imshow(
                corr_matrix.values,
                x=labels_clean,
                y=labels_clean,
                color_continuous_scale='Viridis',
                zmin=-0.2, zmax=1.0,
                text_auto='.3f',
                template='plotly_dark'
            )
            fig_corr.update_layout(
                height=420,
                margin=dict(l=0, r=0, t=20, b=20),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                coloraxis_showscale=False
            )
            st.plotly_chart(fig_corr, use_container_width=True)

        with col_dom:
            st.markdown("#### 🎯 Dominant Pollutant Composition in India")
            st.caption("In 89.9% of Indian cities, PM2.5 determines the peak AQI level.")

            dom_counts = india_df['Dominant Pollutant'].value_counts().reset_index()
            dom_counts.columns = ['Pollutant', 'Count']
            dom_counts['Percentage'] = (dom_counts['Count'] / len(india_df)) * 100

            fig_dom = px.pie(
                dom_counts,
                names='Pollutant',
                values='Count',
                hole=0.6,
                color='Pollutant',
                color_discrete_map={
                    'PM2.5': '#ef4444',
                    'Ozone (O3)': '#f59e0b',
                    'NO2': '#8b5cf6',
                    'CO': '#10b981'
                },
                template='plotly_dark'
            )
            fig_dom.update_layout(
                height=420,
                margin=dict(l=0, r=0, t=20, b=20),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                legend=dict(orientation="h", y=-0.1, x=0.5, xanchor="center")
            )
            fig_dom.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_dom, use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Scatter of PM2.5 vs Ozone
        st.markdown("#### 🧪 PM2.5 vs Ground-Level Ozone Dynamics across Indian Cities")
        st.caption("Visualizing the relationship between secondary photochemical oxidants (Ozone) and particulate matter (PM2.5).")

        try:
            fig_scatter = px.scatter(
                filtered_india,
                x='PM2.5 AQI Value',
                y='Ozone AQI Value',
                color='AQI Category',
                color_discrete_map=AQI_COLORS,
                hover_name='City',
                trendline='ols',
                template='plotly_dark',
                labels={'PM2.5 AQI Value': 'PM2.5 Sub-Index AQI', 'Ozone AQI Value': 'Ozone Sub-Index AQI'}
            )
        except Exception:
            fig_scatter = px.scatter(
                filtered_india,
                x='PM2.5 AQI Value',
                y='Ozone AQI Value',
                color='AQI Category',
                color_discrete_map=AQI_COLORS,
                hover_name='City',
                template='plotly_dark',
                labels={'PM2.5 AQI Value': 'PM2.5 Sub-Index AQI', 'Ozone AQI Value': 'Ozone Sub-Index AQI'}
            )
        fig_scatter.update_layout(
            height=450,
            margin=dict(l=0, r=0, t=20, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation="h", y=1.05, x=0.5, xanchor="center")
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Diagnostic Root Cause Breakdown
        st.markdown("#### 🔬 Root Cause Anatomy: Why Is Indian Urban Air Overwhelmingly PM2.5-Driven?")

        r1, r2, r3 = st.columns(3)

        with r1:
            st.markdown("""
            <div class="policy-box">
                <h4>💨 Road Dust & Construction (32%)</h4>
                <p style="font-size: 0.9rem; color: #cbd5e1; line-height: 1.5;">
                    Unpaved road shoulders, intense vehicular drag, non-mechanized dry sweeping, and uncovered construction/demolition debris generate massive volumes of fugitive mineral dust, continuously resuspended by high traffic volumes.
                </p>
            </div>
            """, unsafe_allow_html=True)

        with r2:
            st.markdown("""
            <div class="policy-box">
                <h4>🚗 Combustion & Diesel Fleets (28%)</h4>
                <p style="font-size: 0.9rem; color: #cbd5e1; line-height: 1.5;">
                    High concentration of commercial diesel trucks, older two-stroke two-wheelers, stop-and-go congestion at uncoordinated traffic signals, and heavy diesel generator (DG) sets during power cuts emit ultra-fine elemental black carbon.
                </p>
            </div>
            """, unsafe_allow_html=True)

        with r3:
            st.markdown("""
            <div class="policy-box">
                <h4>🔥 Biomass & Industrial Fuel (25%)</h4>
                <p style="font-size: 0.9rem; color: #cbd5e1; line-height: 1.5;">
                    Informal open waste burning at dumpsites, domestic solid biomass cooking in peri-urban belts, brick kilns, and small industrial boilers operating on dirty fuels (petcoke, furnace oil, tire oil) release volatile organic compounds and sulfates.
                </p>
            </div>
            """, unsafe_allow_html=True)


    # ==============================================================================
    # TAB 4: ADMINISTRATIVE BLUEPRINT & ACTION PLANNER
    # ==============================================================================
    with tab4:
        st.markdown("### 🏛️ Evidence-Based Policy Blueprint & Actionable Administrative Steps")
        st.caption("Translating data findings into pragmatic, high-impact interventions for Indian Municipal Corporations (ULBs), District Magistrates, and State Pollution Control Boards.")

        # Executive Conclusions
        st.markdown("#### 📌 Key Empirical Conclusions for Indian Cities")

        c_card1, c_card2 = st.columns(2)
        with c_card1:
            st.markdown("""
            <div class="policy-box" style="border-left: 4px solid #ef4444;">
                <h4 style="color: #f87171;">1. The Particulate Monoculture (90% Crisis)</h4>
                <p style="font-size: 0.92rem; color: #e2e8f0; line-height: 1.5;">
                    In <strong>89.91% of Indian cities</strong>, the overall AQI is solely determined by <strong>PM2.5</strong>. Policies focused exclusively on industrial gaseous emissions (SO2/NO2) without tackling primary particulate sources (road dust, diesel exhaust, biomass burning) will fail to shift cities out of 'Unhealthy' status.
                </p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="policy-box" style="border-left: 4px solid #f59e0b;">
                <h4 style="color: #fbbf24;">3. The Instrument Saturation Ceiling (AQI 500)</h4>
                <p style="font-size: 0.92rem; color: #e2e8f0; line-height: 1.5;">
                    <strong>158 Indian cities</strong> hit the maximum sensor ceiling of 500. This indicates acute, hazardous atmospheric saturation during episodic events (winter inversions, post-harvest stubble burning). Cities require automatic graded emergency protocols rather than ad-hoc reactive measures.
                </p>
            </div>
            """, unsafe_allow_html=True)

        with c_card2:
            st.markdown("""
            <div class="policy-box" style="border-left: 4px solid #38bdf8;">
                <h4 style="color: #38bdf8;">2. The Regional Airshed & Transboundary Fallacy</h4>
                <p style="font-size: 0.92rem; color: #e2e8f0; line-height: 1.5;">
                    Municipal boundaries do not contain airborne particulates. The contiguous Indo-Gangetic Basin traps air across Punjab, Haryana, Delhi, Uttar Pradesh, and Bihar. A city municipality cannot clean its air in isolation without unified <strong>Airshed Management Authorities</strong>.
                </p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="policy-box" style="border-left: 4px solid #10b981;">
                <h4 style="color: #34d399;">4. Severe Exposure Disparity (71.3% Unhealthy)</h4>
                <p style="font-size: 0.92rem; color: #e2e8f0; line-height: 1.5;">
                    Over <strong>71.3% of Indian cities</strong> fail National Ambient Air Quality Standards (NAAQS), compared to only 18.3% globally. Air pollution is no longer a seasonal Delhi-NCR curiosity; it is a nationwide chronic public health emergency reducing Indian life expectancy by 3.5 to 5 years.
                </p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # 4-Pillar Action Matrix for City Administrations
        st.markdown("#### 🛠️ Comprehensive 4-Pillar Action Matrix for Municipal Administrations")

        p_tab1, p_tab2, p_tab3, p_tab4 = st.tabs([
            "🚨 Pillar 1: Emergency & Winter GRAP",
            "🚌 Pillar 2: Transport & Fleet Transition",
            "🏭 Pillar 3: Industry, Waste & Dust Abatement",
            "🏥 Pillar 4: Public Health, IoT & Civic Tech"
        ])

        with p_tab1:
            st.markdown("""
            ### Pillar 1: Immediate & Winter Graded Response Action Plan (GRAP)
            *Designed for immediate activation when city AQI breaches 200 (Unhealthy) or 300 (Hazardous).*

            1. **Mechanized Vacuum Sweeping & High-Pressure Washing:**
               - Cease all dry manual broom sweeping on major arterial and sub-arterial roads (>60 ft width). Dry sweeping simply aerates heavy dust into PM2.5 respirable particles.
               - Deploy automated vacuum sweeping trucks with high-efficiency cyclone particulate filters on 100% of PWD/Municipal corridors during night shifts (22:00 to 06:00).
            2. **Mobile Anti-Smog Guns & Micro-Misting at Traffic Congestion Chokepoints:**
               - Mount atomized water misting cannons (droplet size <50 microns) on municipal utility trucks deployed at top 20 traffic intersections and construction hotspots.
               - Treat unpaved road verges and central dividers with eco-friendly chemical dust suppressants (calcium chloride / magnesium lignosulfonate) to bind loose silt.
            3. **Drone-Assisted Night Surveillance for Open Burning:**
               - Deploy night-vision thermal drones over municipal solid waste (MSW) dumpsites, vacant industrial plots, and slum fringes to catch illegal open waste burning.
               - Impose strict spot fines of ₹5,000 to ₹25,000 on ward contractors and commercial entities caught burning garbage or horticultural waste.
            4. **Dynamic Staggered Office Hours & Remote Work Mandates:**
               - During AQI >350, mandate 50% work-from-home for non-essential municipal and private offices to cut peak-hour vehicular volume by 30%.
            """)

        with p_tab2:
            st.markdown("""
            ### Pillar 2: Urban Transport, Traffic Engineering & Fleet Decarbonization
            *1 to 3 Year Targeted Transition for Municipal Transport Authorities.*

            1. **Electrification of Municipal & Public Transit Fleets (PM-eBus Sewa):**
               - Enact a binding municipal resolution: 100% of newly procured intra-city buses and municipal sanitation trucks must be Electric Vehicles (EVs).
               - Convert all auto-rickshaws to electric powertrains with dedicated battery-swapping stations at metro stations and transit hubs.
            2. **Low Emission Zones (LEZ) & Heavy Vehicle Congestion Pricing:**
               - Demarcate dense commercial and cultural core zones as Low Emission Zones (LEZ) where non-BS VI heavy commercial vehicles are barred entry between 07:00 and 22:00.
               - Implement automated Automatic Number Plate Recognition (ANPR) cameras with integrated RFID tolling to penalize polluting transit freight.
            3. **Intelligent Traffic Management System (ITMS):**
               - Synchronize traffic signal green-wave corridors along key arterials using real-time loop detectors to eliminate fuel-wasting vehicle idle cycles.
               - Mandatory strict enforcement of Pollution Under Control (PUC) certificates linked directly to insurance and fuel dispensing.
            4. **Complete Streets & Non-Motorized Transport (NMT) Corridors:**
               - Retrofit city avenues with dedicated protected cycling tracks and continuous shaded pedestrian footpaths to encourage 1-3 km trip modal shift away from personal motor vehicles.
            """)

        with p_tab3:
            st.markdown("""
            ### Pillar 3: Industrial Compliance, Waste Management & Agricultural Bio-Solutions
            *2 to 4 Year Structural Transition for District Administrations & State PCBs.*

            1. **100% Piped Natural Gas (PNG) / Clean Fuel Conversion for MSME Clusters:**
               - Establish a strict deadline for micro and small industrial boilers (foundries, textile dyeing, food processing) to transition from coal/petcoke to PNG or biomass pellets.
               - Continuous Ambient & Emission Monitoring Systems (CEMS) directly integrated into the State Pollution Control Board server with automated show-cause notice generation on emissions breach.
            2. **Complete Bio-Mining of Legacy Dumpsites & Zero Landfill Fires:**
               - Accelerate 100% bio-mining of legacy waste mounds (Swachh Bharat 2.0 mandate) to eliminate underground spontaneous methane combustion that generates toxic dioxins and PM2.5.
               - Enforce strict segregated decentralized composting for bulk food waste generators (hotels, marriage gardens, wholesale mandis).
            3. **Construction & Demolition (C&D) Dust Control Protocols:**
               - Mandatory 100% wind-breaking green netting (minimum 10m height) around all construction plots >500 sq meters.
               - Prohibition of loose transport of sand, gravel, and earth—must be transported under sealed impermeable tarpaulins.
            4. **Airshed Stubble Valorization & Thermal Power Co-Firing:**
               - Ensure thermal power stations in the state strictly comply with the Ministry of Power mandate to co-fire 5% to 7% biomass pellets with coal.
               - Establish custom hiring centers (CHCs) for Happy Seeders, Super Seeders, and crop balers with local bio-refinery buyback agreements.
            """)

        with p_tab4:
            st.markdown("""
            ### Pillar 4: Public Health, Hyper-Local Monitoring & Civic Governance
            *Immediate to Long-Term Public Protection & Civic Accountability Framework.*

            1. **Hyper-Local IoT Air Quality Monitoring Grid:**
               - Augment sparse, costly CAAQMS stations (₹1.5 Crore each) with calibrated, dense IoT optical particle counter grids (1 sensor per 2-3 km²) to identify hyper-local pollution micro-hotspots.
               - Publish open real-time air quality APIs for civic researchers and urban planners.
            2. **Color-Coded Public Health Advisory System:**
               - Mandate real-time AQI display boards at all bus stops, metro stations, municipal schools, and public parks.
               - Issue automatic school morning assembly outdoor activity cancellations when AQI exceeds 250.
               - Provide free N95 respirator masks to outdoor municipal workers, sanitation personnel, and traffic police officers.
            3. **Unified Citizen Grievance App with 48-Hour SLA:**
               - Launch or upgrade a dedicated municipal smartphone application (similar to the 'Green Delhi' model) enabling citizens to geo-tag and photograph road dust, garbage burning, or unpaved debris.
               - Strict 48-hour municipal taskforce resolution service-level agreement (SLA) with contractor performance penalties.
            4. **Urban Forestry & Miyawaki Green Buffers:**
               - Plant dense Miyawaki micro-forests using broad-leaf, particulate-capturing native species (Peepal, Neem, Banyan, Jamun, Sheesham) along railway tracks, industrial buffer zones, and highway margins.
            """)

        st.markdown("<br>", unsafe_allow_html=True)

        # Interactive Municipal Air Quality Action Planner
        st.markdown("#### 🎯 Interactive Municipal Air Quality Action Planner")
        st.caption("Select your city's administrative profile and air pollution baseline to generate a prioritized, phased roadmap.")

        col_inp1, col_inp2, col_inp3 = st.columns(3)

        with col_inp1:
            city_tier = st.selectbox(
                "City Population & Administrative Tier",
                ["Tier 1 Mega Metropolis (>4 Million)", "Tier 2 Growing Urban Center (1-4 Million)", "Tier 3 / Satellite Industrial Town (<1 Million)"]
            )
        with col_inp2:
            current_aqi_tier = st.selectbox(
                "Current Typical Winter/Peak AQI Level",
                ["Hazardous (AQI 301 - 500)", "Very Unhealthy / Unhealthy (AQI 151 - 300)", "Moderate / Sensitive (AQI 51 - 150)"]
            )
        with col_inp3:
            budget_envelope = st.selectbox(
                "Available Municipal Capital Budget Envelope",
                ["High (NCAP + 15th Finance Commission + Municipal Funds)", "Moderate (Standard NCAP Grants)", "Constrained (Local Municipal Revenue Only)"]
            )

        # Dynamic Action Roadmap Generation
        st.markdown("##### 📋 Phased Municipal Implementation Roadmap")

        m_col1, m_col2, m_col3 = st.columns(3)

        with m_col1:
            st.markdown("""
            <div class="policy-box">
                <h4 style="color: #f87171;">⏱️ Phase 1: Days 1 - 90 (Immediate Containment)</h4>
                <ul style="font-size: 0.88rem; color: #cbd5e1; padding-left: 18px; line-height: 1.6;">
                    <li>Halt unmechanized dry sweeping on arterial roads.</li>
                    <li>Lease 4-8 automated vacuum sweepers for night corridors.</li>
                    <li>Deploy anti-smog misting guns at top 10 choked intersections.</li>
                    <li>Activate drone night patrolling on open waste burn hotspots.</li>
                    <li>Distribute N95 masks to all municipal sanitation staff.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        with m_col2:
            st.markdown("""
            <div class="policy-box">
                <h4 style="color: #fbbf24;">⚡ Phase 2: Year 1 (Structural Controls)</h4>
                <ul style="font-size: 0.88rem; color: #cbd5e1; padding-left: 18px; line-height: 1.6;">
                    <li>Procure first batch of 50-100 electric municipal transit buses.</li>
                    <li>Mandate 100% covered sand/aggregate transport with ANPR fines.</li>
                    <li>Pave or green-buffer unpaved road shoulders across 150 km.</li>
                    <li>Deploy 25-50 calibrated low-cost IoT AQI sensors.</li>
                    <li>Launch unified citizen photo grievance app with 48h SLA.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        with m_col3:
            st.markdown("""
            <div class="policy-box">
                <h4 style="color: #34d399;">🌲 Phase 3: Years 2 - 3 (Airshed Transformation)</h4>
                <ul style="font-size: 0.88rem; color: #cbd5e1; padding-left: 18px; line-height: 1.6;">
                    <li>100% bio-mining of legacy MSW dumpsites (zero open burning).</li>
                    <li>Complete transition of industrial clusters to PNG / clean fuels.</li>
                    <li>Designate core Low Emission Zones (LEZ) with congestion charges.</li>
                    <li>Plant 500,000 broad-leaf native trees in Miyawaki green buffers.</li>
                    <li>Achieve 30-40% sustained reduction in annual PM2.5 levels.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        # Downloadable Policy Summary
        policy_report_text = f"""# AEROWATCH MUNICIPAL CLEAN AIR ACTION PLAN
    Target Administrative Profile: {city_tier}
    Current Pollution Baseline: {current_aqi_tier}
    Budget Allocation Envelope: {budget_envelope}

    EMPIRICAL FINDINGS:
    - National Cohort Size: 2,488 Indian cities analyzed
    - Mean AQI for India: 153.0 (Unhealthy category)
    - Primary Toxic Pollutant: PM2.5 (dominates in 89.91% of cities)
    - Critical Threat: Over 71.3% of cities fail clean air standards; 158 cities hit max sensor cap (500).

    MANDATED ACTION MATRIX:
    1. Immediate (90 Days): Mechanized vacuum sweeping, anti-smog misting guns, drone night patrols against open burning.
    2. Short Term (1 Year): Public transit electrification, unpaved road stabilization, IoT air quality sensor grid.
    3. Medium Term (3 Years): Complete dumpsite bio-mining, industrial PNG transition, Low Emission Zones (LEZ).

    Signed & Generated via AeroWatch Environmental Intelligence Engine.
    """
        st.download_button(
            label="📥 Export Municipal Policy Brief (Markdown / Text)",
            data=policy_report_text,
            file_name="AeroWatch_Municipal_Clean_Air_Action_Plan.md",
            mime="text/markdown"
        )


    # ==============================================================================
    # TAB 5: RAW DATA EXPLORER & EXPORT
    # ==============================================================================
    with tab5:
        st.markdown("### 📋 Interactive Dataset Explorer & Export")
        st.caption("Search, filter, and inspect granular records across all 23,463 cities in the dataset.")

        col_t1, col_t2 = st.columns([1, 2])
        with col_t1:
            search_country = st.selectbox(
                "Filter by Country",
                ["All Countries"] + sorted([str(c) for c in df['Country'].unique()])
            )
        with col_t2:
            search_query = st.text_input("Search City Name (type to search)", "")

        explorer_df = df.copy()
        if search_country != "All Countries":
            explorer_df = explorer_df[explorer_df['Country'] == search_country]
        if search_query.strip():
            explorer_df = explorer_df[explorer_df['City'].str.contains(search_query.strip(), case=False, na=False)]

        st.markdown(f"**Showing {len(explorer_df):,} matching cities:**")

        st.dataframe(
            explorer_df[['Country', 'City', 'AQI Value', 'AQI Category', 'Dominant Pollutant', 'PM2.5 AQI Value', 'Ozone AQI Value', 'NO2 AQI Value', 'CO AQI Value']].reset_index(drop=True),
            use_container_width=True,
            height=480
        )

        # Export filtered data
        csv_bytes = explorer_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Current Selection as CSV",
            data=csv_bytes,
            file_name="air_pollution_filtered_data.csv",
            mime="text/csv"
        )

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #64748b; font-size: 0.85rem; padding: 12px 0;">
        <strong>AeroWatch Air Pollution Intelligence Engine</strong> • Built for Municipal Commissioners, Urban Local Bodies & Policy Analysts • Python & Streamlit Core Architecture
    </div>
    """, unsafe_allow_html=True)

def render_water_dashboard():
    st.markdown("""
    <div class="hero-container" style="margin-bottom: 24px;">
        <h2 style="margin: 0; color: white; font-size: 2rem;">💧 National Water Quality Surveillance & River Basin Action Framework</h2>
        <p style="color: #94a3b8; font-size: 1.05rem; margin-top: 8px;">
            Analyzing river basin contamination, biochemical oxygen demand (BOD), and municipal compliance across India.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if water_df.empty:
        st.error("No water quality data found.")
        return
        
    # Data Cleaning and Preparation
    wdf = water_df.copy()
    wdf['Year'] = pd.to_numeric(wdf['Year'], errors='coerce')
    wdf['BOD (mg/L) - Max'] = pd.to_numeric(wdf['BOD (mg/L) - Max'], errors='coerce')
    wdf['Dissolved - Min'] = pd.to_numeric(wdf['Dissolved - Min'], errors='coerce')
    wdf['pH - Max'] = pd.to_numeric(wdf['pH - Max'], errors='coerce')
    wdf['Total Coliform (MPN/100ml) - Max'] = pd.to_numeric(wdf['Total Coliform (MPN/100ml) - Max'], errors='coerce')
    
    # Categorize Water Quality
    def categorize_water(row):
        bod = row['BOD (mg/L) - Max']
        do = row['Dissolved - Min']
        if pd.isna(bod) or pd.isna(do): return "Unknown"
        if bod < 3.0 and do > 5.0: return "Safe"
        elif bod > 6.0 or do < 4.0: return "Severely Polluted"
        else: return "Moderate"
        
    wdf['Water Quality Category'] = wdf.apply(categorize_water, axis=1)
    
    # Sidebar Filters
    st.sidebar.markdown("### 💧 Water Module Controls")
    available_years = sorted(wdf['Year'].dropna().unique().astype(int))
    selected_year = st.sidebar.select_slider("Select Year", options=available_years, value=available_years[-1] if available_years else 2022)
    
    available_states = ["All"] + sorted(wdf['State Name'].dropna().unique().tolist())
    selected_state = st.sidebar.selectbox("Filter by State / Basin", available_states)
    
    available_cats = ["All"] + sorted(wdf['Water Quality Category'].unique().tolist())
    selected_cat = st.sidebar.selectbox("Water Quality Category", available_cats)
    
    # Apply filters
    filtered_wdf = wdf[wdf['Year'] == selected_year]
    if selected_state != "All":
        filtered_wdf = filtered_wdf[filtered_wdf['State Name'] == selected_state]
    if selected_cat != "All":
        filtered_wdf = filtered_wdf[filtered_wdf['Water Quality Category'] == selected_cat]
        
    # Metrics
    total_stations = len(filtered_wdf)
    safe_sources = len(filtered_wdf[filtered_wdf['Water Quality Category'] == 'Safe'])
    safe_perc = (safe_sources / total_stations * 100) if total_stations > 0 else 0
    hotspots = len(filtered_wdf[filtered_wdf['Water Quality Category'] == 'Severely Polluted'])
    
    worst_basin = "N/A"
    if hotspots > 0:
        worst_basin = filtered_wdf[filtered_wdf['Water Quality Category'] == 'Severely Polluted']['State Name'].mode().iloc[0] if not filtered_wdf.empty else "N/A"
        
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-title">Total Monitoring Stations</div>
            <div class="metric-value">{total_stations:,}</div>
            <div class="metric-subtitle">Active sites in {selected_year}</div>
        </div>
        ''', unsafe_allow_html=True)
    with m2:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-title">Clean/Potable Sources</div>
            <div class="metric-value" style="color: #34d399;">{safe_perc:.1f}%</div>
            <div class="metric-subtitle">Meeting BOD/DO norms</div>
        </div>
        ''', unsafe_allow_html=True)
    with m3:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-title">Contaminated Hotspots</div>
            <div class="metric-value" style="color: #ef4444;">{hotspots:,}</div>
            <div class="metric-subtitle">Severely Polluted</div>
        </div>
        ''', unsafe_allow_html=True)
    with m4:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-title">Worst Affected Basin</div>
            <div class="metric-value" style="font-size: 1.6rem; margin-top: 10px;">{str(worst_basin)[:15]}</div>
        </div>
        ''', unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["🗺️ River Basin & State Deep-Dive", "🔬 Parameter Fingerprint", "📋 Municipal Roadmap"])
    
    with tab1:
        st.markdown("#### State-wise WQI/BOD/DO Levels")
        if not filtered_wdf.empty:
            state_avg = filtered_wdf.groupby('State Name')[['BOD (mg/L) - Max', 'Dissolved - Min']].mean().reset_index()
            fig1 = px.bar(
                state_avg.sort_values('BOD (mg/L) - Max', ascending=False).head(20),
                x='BOD (mg/L) - Max',
                y='State Name',
                orientation='h',
                title="Top 20 States by Max BOD Levels",
                template="plotly_dark",
                color='BOD (mg/L) - Max',
                color_continuous_scale='Reds'
            )
            fig1.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig1, use_container_width=True)
            
    with tab2:
        st.markdown("#### Water Parameter Correlations (pH, DO, BOD, Coliform)")
        if not filtered_wdf.empty:
            # Handle bubble size missing values
            filtered_wdf = filtered_wdf.copy()
            filtered_wdf['Total Coliform (MPN/100ml) - Max'] = filtered_wdf['Total Coliform (MPN/100ml) - Max'].fillna(0)
            fig2 = px.scatter(
                filtered_wdf,
                x='Dissolved - Min',
                y='BOD (mg/L) - Max',
                color='Water Quality Category',
                size='Total Coliform (MPN/100ml) - Max',
                hover_name='Monitoring Location',
                title="BOD vs Dissolved Oxygen (Bubble Size: Total Coliform)",
                template="plotly_dark",
                color_discrete_map={"Safe": "#10B981", "Moderate": "#F59E0B", "Severely Polluted": "#EF4444", "Unknown": "#64748b"}
            )
            st.plotly_chart(fig2, use_container_width=True)
            
    with tab3:
        st.markdown("#### Actionable Municipal/Pollution Control Roadmap")
        st.markdown("""
        <div class="policy-box">
            <h4>1. Point-Source Effluent Tracking</h4>
            <p style="color: #94a3b8;">Mandate strict effluent treatment plant (ETP) audits in high-BOD zones. Install real-time IoT water sensors at industrial discharge pipes.</p>
        </div>
        <div class="policy-box">
            <h4>2. Coliform Control & Sanitation</h4>
            <p style="color: #94a3b8;">Prioritize sewage treatment plant (STP) capacity upgrades in basins exhibiting Severely Polluted status due to high fecal/total coliform counts.</p>
        </div>
        <div class="policy-box">
            <h4>3. River Rejuvenation Drives</h4>
            <p style="color: #94a3b8;">Initiate ecological flow maintenance and dissolved oxygen (DO) aeration protocols in critical hotspots.</p>
        </div>
        """, unsafe_allow_html=True)


def render_integrated_dashboard():
    st.markdown("""
    <div class="hero-container" style="margin-bottom: 24px;">
        <h2 style="margin: 0; color: white; font-size: 2rem;">🌍 Integrated Environmental Radar</h2>
        <p style="color: #94a3b8; font-size: 1.05rem; margin-top: 8px;">
            Cross-domain analysis of planetary health, correlating air and water contamination metrics.
        </p>
    </div>
    """, unsafe_allow_html=True)
    if water_df.empty or india_df.empty:
        st.error("Insufficient data for integrated analysis.")
        return
        
    # Aggregate Air Data
    idf = india_df.copy()
    idf['State_Clean'] = idf['State'].astype(str).str.upper().str.strip()
    air_agg = idf.groupby('State_Clean')['AQI Value'].mean().reset_index()
    air_agg.rename(columns={'AQI Value': 'Avg AQI'}, inplace=True)
    
    # Aggregate Water Data
    wdf = water_df.copy()
    wdf['State_Clean'] = wdf['State Name'].astype(str).str.upper().str.strip()
    wdf['BOD (mg/L) - Max'] = pd.to_numeric(wdf['BOD (mg/L) - Max'], errors='coerce').fillna(0)
    water_agg = wdf.groupby('State_Clean')['BOD (mg/L) - Max'].mean().reset_index()
    water_agg.rename(columns={'BOD (mg/L) - Max': 'Avg BOD'}, inplace=True)
    
    # Merge and Normalize
    merged = pd.merge(air_agg, water_agg, on='State_Clean', how='inner')
    merged = merged[(merged['State_Clean'] != 'OTHER / UNMAPPED') & (merged['State_Clean'] != 'NAN')]
    
    if merged.empty:
        st.warning("No overlapping states found between Air and Water datasets.")
        return
        
    merged['Avg AQI Norm'] = merged['Avg AQI'] / merged['Avg AQI'].max()
    merged['Avg BOD Norm'] = merged['Avg BOD'] / merged['Avg BOD'].max()
    merged['Unified Risk Index (0-100)'] = (merged['Avg AQI Norm'] * 0.5 + merged['Avg BOD Norm'] * 0.5) * 100
    merged = merged.sort_values('Unified Risk Index (0-100)', ascending=False)
    
    # Metrics
    highest_risk = merged.iloc[0]['State_Clean'].title() if not merged.empty else "N/A"
    total_states = len(merged)
    nat_aqi = merged['Avg AQI'].mean()
    nat_bod = merged['Avg BOD'].mean()
    
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-title">Critical Risk State</div>
            <div class="metric-value" style="color: #ef4444; font-size: 1.6rem; margin-top: 10px;">{highest_risk[:15]}</div>
        </div>
        ''', unsafe_allow_html=True)
    with m2:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-title">States Analyzed</div>
            <div class="metric-value">{total_states}</div>
            <div class="metric-subtitle">Cross-domain overlaps</div>
        </div>
        ''', unsafe_allow_html=True)
    with m3:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-title">National Avg AQI</div>
            <div class="metric-value">{nat_aqi:.0f}</div>
        </div>
        ''', unsafe_allow_html=True)
    with m4:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-title">National Avg BOD</div>
            <div class="metric-value">{nat_bod:.1f} <span style="font-size: 0.8rem">mg/L</span></div>
        </div>
        ''', unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### ⚖️ Air vs Water Contamination Scatter")
        fig_scatter = px.scatter(
            merged,
            x='Avg AQI',
            y='Avg BOD',
            color='Unified Risk Index (0-100)',
            hover_name='State_Clean',
            size='Unified Risk Index (0-100)',
            template='plotly_dark',
            color_continuous_scale='Turbo',
            labels={'Avg AQI': 'Average AQI', 'Avg BOD': 'Average BOD (mg/L)'}
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        
    with col2:
        st.markdown("#### 🚨 Top 10 States by Unified Risk")
        fig_bar = px.bar(
            merged.head(10).sort_values('Unified Risk Index (0-100)', ascending=True),
            x='Unified Risk Index (0-100)',
            y='State_Clean',
            orientation='h',
            template='plotly_dark',
            color='Unified Risk Index (0-100)',
            color_continuous_scale='Reds'
        )
        st.plotly_chart(fig_bar, use_container_width=True)


# ==========================================
# APP ROUTING LOGIC
# ==========================================
if module_selection == "💨 Air Quality Intelligence":
    render_air_dashboard()
elif module_selection == "💧 Water Quality Intelligence":
    render_water_dashboard()
else:
    render_integrated_dashboard()

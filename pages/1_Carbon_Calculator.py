import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Carbon Calculator | DeforestWatch",
    page_icon="💨",
    layout="wide" 
)

# ── Same CSS theme ────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;700&display=swap');
* { font-family: 'Inter', sans-serif; }
.stApp { background-color: #010b0e; }
footer { visibility: hidden; }
#MainMenu { visibility: hidden; }
.block-container { padding-top: 1rem !important; }
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #011a1f 0%, #010e10 100%);
    border: 1px solid rgba(0,255,255,0.2);
    border-radius: 16px;
    padding: 20px !important;
}
[data-testid="stMetricLabel"] { color: #00ffff !important; font-size: 11px !important; font-weight: 600 !important; letter-spacing: 2px !important; text-transform: uppercase !important; }
[data-testid="stMetricValue"] { color: #ffffff !important; font-size: 26px !important; font-weight: 800 !important; }
[data-testid="stSidebar"] { background-color: #0d1a0d; border-right: 1px solid rgba(0,255,255,0.15); }
/* Keep collapse arrow always visible */
[data-testid="stSidebarCollapsedControl"] {
    display: block !important;
    visibility: visible !important;
    opacity: 1 !important;
    background-color: #010e10 !important;
}

button[data-testid="collapsedControl"] {
    display: block !important;
    visibility: visible !important;
    color: #00ffff !important;
}
hr { border-color: rgba(0,255,255,0.1) !important; }
.stSelectbox > div { background: #011a1f; border: 1px solid rgba(0,255,255,0.2); }
.result-card {
    background: linear-gradient(135deg, #011a1f, #010e10);
    border: 1px solid rgba(0,255,255,0.2);
    border-radius: 16px;
    padding: 24px;
    text-align: center;
    margin: 8px 0;
}
.big-number {
    font-size: 42px;
    font-weight: 900;
    font-family: 'JetBrains Mono', monospace;
}
.stSlider [data-baseweb="slider"] [role="progressbar"] {
    background: linear-gradient(90deg, #00ffff, #00ff99) !important;
}
</style>
""", unsafe_allow_html=True)

# ── Load data ─────────────────────────────────────────────────────
@st.cache_data
def load_data():
    return pd.read_csv('data/deforestation_clean.csv')

df = load_data()

# ── Carbon conversion constants ───────────────────────────────────
# 1 km² of tropical forest stores approximately 200 tonnes of carbon
# When burned/cleared, carbon releases as CO2 (multiply by 3.67)
CARBON_PER_KM2     = 200    # tonnes of carbon per km²
CO2_PER_KM2        = 200 * 3.67  # = 734 tonnes of CO2 per km²

# Real world CO2 comparisons
CO2_PER_FLIGHT     = 0.9    # tonnes CO2 per passenger, Delhi→New York
CO2_PER_CAR_YEAR   = 4.6    # tonnes CO2 per car per year
CO2_PER_HOME_YEAR  = 7.5    # tonnes CO2 per home per year
CO2_PER_BEEF_KG    = 0.027  # tonnes CO2 per kg of beef

# ── Hero ──────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center; padding:32px 0 16px 0;'>
    <div style='font-size:11px; letter-spacing:4px; color:#00ffff; font-weight:600; margin-bottom:12px;'>
        💨 CARBON IMPACT CALCULATOR
    </div>
    <h1 style='font-size:46px; font-weight:900; color:#ffffff; margin:0;
               text-shadow: 0 0 40px rgba(0,255,255,0.3);'>
        Deforestation →
        <span style='color:#00ffff;'>Carbon Emissions</span>
    </h1>
    <p style='color:#60a0a0; font-size:15px; margin-top:12px;'>
        See how forest loss translates into real-world carbon impact
    </p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ── Controls ──────────────────────────────────────────────────────
st.markdown("<p style='font-size:11px; color:#00ffff; letter-spacing:3px; font-weight:600;'>🎛️ SELECT YOUR PARAMETERS</p>", unsafe_allow_html=True)

ctrl1, ctrl2, ctrl3 = st.columns(3)

with ctrl1:
    selected_region = st.selectbox(
        "🌍 Select Region",
        options=['All Regions'] + list(df['region'].unique())
    )

with ctrl2:
    year_start = st.selectbox("📅 From Year", options=list(range(2001, 2025)), index=0)

with ctrl3:
    year_end = st.selectbox("📅 To Year", options=list(range(2001, 2025)), index=23)

# ── Calculate loss ────────────────────────────────────────────────
if selected_region == 'All Regions':
    region_df = df
else:
    region_df = df[df['region'] == selected_region]

filtered = region_df[region_df['year'].between(year_start, year_end)]
total_loss_km2 = filtered['loss_km2'].sum()

# Carbon calculations
total_co2       = total_loss_km2 * CO2_PER_KM2          # tonnes
total_co2_mega  = total_co2 / 1_000_000                  # megatonnes

# Equivalents
flights         = total_co2 / CO2_PER_FLIGHT
cars_year       = total_co2 / CO2_PER_CAR_YEAR
homes_year      = total_co2 / CO2_PER_HOME_YEAR
beef_kg         = total_co2 / CO2_PER_BEEF_KG

st.divider()

# ── Main result ───────────────────────────────────────────────────
st.markdown(f"""
<div style='background:linear-gradient(135deg, #1a0a00, #0e0500);
            border:2px solid rgba(255,165,0,0.4); border-radius:20px;
            padding:32px; text-align:center; margin:16px 0;'>
    <div style='font-size:13px; letter-spacing:3px; color:#ffa502; font-weight:600; margin-bottom:12px;'>
        ⚠️ TOTAL CO₂ RELEASED
    </div>
    <div style='font-size:64px; font-weight:900; color:#ffffff;
                font-family: JetBrains Mono, monospace;
                text-shadow: 0 0 40px rgba(255,165,0,0.5);'>
        {total_co2_mega:,.1f}
    </div>
    <div style='font-size:20px; color:#ffa502; font-weight:600;'>Megatonnes of CO₂</div>
    <div style='font-size:14px; color:#806040; margin-top:8px;'>
        From {total_loss_km2:,.0f} km² of forest lost
        · {selected_region} · {year_start}–{year_end}
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()

# ── Equivalents ───────────────────────────────────────────────────
st.markdown("<p style='font-size:11px; color:#00ffff; letter-spacing:3px; font-weight:600; margin-bottom:16px;'>🔄 WHAT DOES THIS EQUAL?</p>", unsafe_allow_html=True)

e1, e2, e3, e4 = st.columns(4)

equivalents = [
    (e1, '✈️', f'{flights/1_000_000:,.1f}M', 'Delhi → New York flights', '#00ffff'),
    (e2, '🚗', f'{cars_year/1_000_000:,.1f}M', 'Cars driven for a full year', '#00ff99'),
    (e3, '🏠', f'{homes_year/1_000_000:,.1f}M', 'Homes powered for a year', '#ffa502'),
    (e4, '🥩', f'{beef_kg/1_000_000_000:,.1f}B', 'kg of beef produced', '#ff4757'),
]

for col, icon, number, label, color in equivalents:
    with col:
        st.markdown(f"""
        <div class='result-card'>
            <div style='font-size:36px; margin-bottom:8px;'>{icon}</div>
            <div class='big-number' style='color:{color};
                         text-shadow: 0 0 20px {color}66;'>{number}</div>
            <div style='font-size:12px; color:#607070; margin-top:8px;
                        line-height:1.4;'>{label}</div>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# ── Year by year carbon chart ─────────────────────────────────────
st.markdown("<p style='font-size:11px; color:#00ffff; letter-spacing:3px; font-weight:600; margin-bottom:8px;'>📊 ANNUAL CARBON EMISSIONS FROM DEFORESTATION</p>", unsafe_allow_html=True)

filtered_copy = filtered.copy()
filtered_copy['co2_megatonnes'] = (filtered_copy['loss_km2'] * CO2_PER_KM2) / 1_000_000

COLORS = {'Amazon':'#ff4757','Congo':'#00ff99','SE Asia':'#ffa502','India':'#00d2ff'}

fig = px.bar(
    filtered_copy,
    x='year', y='co2_megatonnes', color='region',
    color_discrete_map=COLORS,
    labels={'co2_megatonnes': 'CO₂ Released (Megatonnes)', 'year': 'Year'},
    barmode='group'
)
fig.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#a0f0f0'),
    xaxis=dict(gridcolor='rgba(0,255,255,0.06)'),
    yaxis=dict(gridcolor='rgba(0,255,255,0.06)'),
    legend=dict(bgcolor='rgba(1,26,31,0.8)', bordercolor='rgba(0,255,255,0.2)', borderwidth=1),
    hoverlabel=dict(bgcolor='#011a1f', bordercolor='#00ffff'),
)
st.plotly_chart(fig, use_container_width=True)

st.divider()

# ── Personal offset calculator ────────────────────────────────────
st.markdown("<p style='font-size:11px; color:#00ffff; letter-spacing:3px; font-weight:600; margin-bottom:16px;'>🌱 PERSONAL OFFSET CALCULATOR</p>", unsafe_allow_html=True)
st.caption("How many trees would need to be planted to offset this deforestation?")

# 1 mature tree absorbs ~22 kg CO2 per year = 0.000022 tonnes
CO2_PER_TREE_YEAR = 0.000022
trees_needed_1yr  = total_co2 / CO2_PER_TREE_YEAR
trees_needed_10yr = trees_needed_1yr / 10
trees_needed_50yr = trees_needed_1yr / 50

t1, t2, t3 = st.columns(3)

tree_data = [
    (t1, f'{trees_needed_1yr/1_000_000_000:,.1f}B', 'trees needed', 'to offset in 1 year', '#ff4757'),
    (t2, f'{trees_needed_10yr/1_000_000_000:,.1f}B', 'trees needed', 'to offset in 10 years', '#ffa502'),
    (t3, f'{trees_needed_50yr/1_000_000:,.0f}M',     'trees needed', 'to offset in 50 years', '#00ff99'),
]

for col, number, unit, label, color in tree_data:
    with col:
        st.markdown(f"""
        <div class='result-card'>
            <div style='font-size:36px;'>🌳</div>
            <div class='big-number' style='color:{color};
                         text-shadow:0 0 20px {color}66; margin:8px 0;'>{number}</div>
            <div style='font-size:13px; color:#a0c0c0; font-weight:600;'>{unit}</div>
            <div style='font-size:12px; color:#607070; margin-top:4px;'>{label}</div>
        </div>
        """, unsafe_allow_html=True)

st.divider()
st.markdown("""
<div style='text-align:center; padding:16px; color:#304040; font-size:12px;'>
    Carbon estimates based on IPCC tropical forest carbon density standards (200 tC/km²)<br>
    CO₂ conversion factor: 3.67 · Flight emissions: atmosfair.de · Vehicle data: EPA
</div>
""", unsafe_allow_html=True)
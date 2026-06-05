import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="DeforestWatch | Global Forest Monitor",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── FULL CUSTOM CSS ───────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;700&display=swap');

* { font-family: 'Inter', sans-serif; }

.stApp {
    background-color: #010b0e;
    background-image:
        radial-gradient(ellipse at 20% 20%, rgba(0,255,255,0.03) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 80%, rgba(0,200,150,0.03) 0%, transparent 50%);
}

/* Hide streamlit defaults */
footer { visibility: hidden; }
#MainMenu { visibility: hidden; }
.block-container { padding-top: 1rem !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #010e10 0%, #010b0e 100%);
    border-right: 1px solid rgba(0,255,255,0.15);
}
[data-testid="stSidebar"] * { color: #a0f0f0 !important; }
/* Keep collapse arrow always visible */
[data-testid="stSidebarCollapsedControl"] {
    visibility: visible !important;
    opacity: 1 !important;
}
/* ── Metric cards ── */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #011a1f 0%, #010e10 100%);
    border: 1px solid rgba(0,255,255,0.2);
    border-radius: 16px;
    padding: 20px !important;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s;
}
[data-testid="stMetric"]:hover { border-color: rgba(0,255,255,0.6); }
[data-testid="stMetricLabel"] {
    color: #00ffff !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
}
[data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-size: 26px !important;
    font-weight: 800 !important;
}
[data-testid="stMetricDelta"] svg { display: none !important; }

/* ── Divider ── */
hr { border-color: rgba(0,255,255,0.1) !important; }

/* ── Expander ── */
[data-testid="stExpander"] {
    background: #011a1f;
    border: 1px solid rgba(0,255,255,0.15) !important;
    border-radius: 12px !important;
}

/* ── Multiselect tags ── */
[data-testid="stMultiSelect"] span[data-baseweb="tag"] {
    background-color: rgba(0,255,255,0.15) !important;
    border: 1px solid rgba(0,255,255,0.4) !important;
    color: #00ffff !important;
}

/* ── Slider ── */
[data-testid="stSlider"] [data-baseweb="slider"] [role="progressbar"] {
    background: linear-gradient(90deg, #00ffff, #00ff99) !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #010b0e; }
::-webkit-scrollbar-thumb { background: rgba(0,255,255,0.3); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ── Load data ─────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv('data/deforestation_clean.csv')
    return df

df = load_data()

COLORS = {
    'Amazon': '#ff4757',
    'Congo':  '#00ff99',
    'SE Asia':'#ffa502',
    'India':  '#00d2ff'
}

CHART_LAYOUT = dict(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#a0f0f0', family='Inter'),
    xaxis=dict(gridcolor='rgba(0,255,255,0.06)', zerolinecolor='rgba(0,255,255,0.1)', tickfont=dict(color='#60c0c0')),
    yaxis=dict(gridcolor='rgba(0,255,255,0.06)', zerolinecolor='rgba(0,255,255,0.1)', tickfont=dict(color='#60c0c0')),
    legend=dict(bgcolor='rgba(1,26,31,0.8)', bordercolor='rgba(0,255,255,0.2)', borderwidth=1, font=dict(color='#a0f0f0')),
    hoverlabel=dict(bgcolor='#011a1f', bordercolor='#00ffff', font=dict(color='#ffffff')),
    margin=dict(t=30, b=30, l=10, r=10)
)

# ── Sidebar ───────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:16px 0 8px 0;'>
        <div style='font-size:36px;'>🛰️</div>
        <div style='font-size:18px; font-weight:800; color:#00ffff; letter-spacing:2px;'>DEFORESTWATCH</div>
        <div style='font-size:11px; color:#406060; letter-spacing:1px; margin-top:4px;'>GLOBAL FOREST MONITOR</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.markdown("<p style='font-size:11px; color:#00ffff; letter-spacing:2px; font-weight:600;'>FILTERS</p>", unsafe_allow_html=True)

    selected_regions = st.multiselect(
        "Regions",
        options=df['region'].unique(),
        default=df['region'].unique()
    )

    year_range = st.slider("Year Range", 2001, 2024, (2001, 2024))

    st.divider()
    st.markdown("<p style='font-size:11px; color:#00ffff; letter-spacing:2px; font-weight:600;'>REGION LEGEND</p>", unsafe_allow_html=True)

    for region, color in COLORS.items():
        total_r = df[df['region']==region]['loss_km2'].sum()
        st.markdown(f"""
        <div style='display:flex; align-items:center; justify-content:space-between;
                    padding:8px 12px; margin:4px 0; border-radius:8px;
                    background:rgba(0,255,255,0.04); border:1px solid rgba(0,255,255,0.08);'>
            <div style='display:flex; align-items:center; gap:8px;'>
                <div style='width:10px; height:10px; border-radius:50%; background:{color};
                            box-shadow: 0 0 8px {color};'></div>
                <span style='color:#c0e8e8; font-size:13px; font-weight:500;'>{region}</span>
            </div>
            <span style='color:{color}; font-size:12px; font-weight:700;
                         font-family: JetBrains Mono, monospace;'>{total_r/1000:.0f}k km²</span>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.markdown("<p style='font-size:11px; color:#00ffff; letter-spacing:2px; font-weight:600;'>CRITICAL FACTS</p>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:12px; color:#80b0b0; line-height:1.8;'>
        🌲 1 football field lost <b style='color:#00ffff'>every second</b><br>
        🌡️ Causes <b style='color:#ffa502'>10% of CO₂</b> emissions<br>
        🦜 Home to <b style='color:#00ff99'>80% of species</b><br>
        💧 Forests hold <b style='color:#00d2ff'>75% of freshwater</b>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.markdown("<p style='font-size:10px; color:#304040; text-align:center;'>Hansen GFC 2025 · UMD · Google Earth Engine<br>30m resolution · 2001–2024</p>", unsafe_allow_html=True)

# ── Filter ────────────────────────────────────────────────────────
filtered = df[
    df['region'].isin(selected_regions) &
    df['year'].between(year_range[0], year_range[1])
]

# ── HERO ──────────────────────────────────────────────────────────
total_all = df['loss_km2'].sum()
france_germany_km2 = 1058000

st.markdown(f"""
<div style='text-align:center; padding:32px 0 8px 0;'>
    <div style='font-size:11px; letter-spacing:4px; color:#00ffff; font-weight:600; margin-bottom:12px;'>
        🛰️ SATELLITE FOREST INTELLIGENCE
    </div>
    <h1 style='font-size:52px; font-weight:900; color:#ffffff; margin:0; line-height:1.1;
               text-shadow: 0 0 40px rgba(0,255,255,0.3);'>
        Global Deforestation
        <span style='color:#00ffff;'>Tracker</span>
    </h1>
    <p style='color:#60a0a0; font-size:15px; margin-top:12px; font-weight:300;'>
        24 years · 4 regions · 30 metre resolution · Real satellite data
    </p>
</div>
""", unsafe_allow_html=True)

# ── Alert bar ─────────────────────────────────────────────────────
st.markdown(f"""
<div style='background:linear-gradient(90deg, rgba(255,71,87,0.15), rgba(255,71,87,0.05));
            border:1px solid rgba(255,71,87,0.4); border-radius:10px;
            padding:14px 24px; margin:16px 0; display:flex; align-items:center; gap:12px;'>
    <span style='font-size:20px;'>🚨</span>
    <span style='color:#ff8888; font-size:14px; font-weight:500;'>
        Since 2001, <b style='color:#ff4757; font-size:16px;'>{total_all:,.0f} km²</b>
        of forest has been lost across these 4 regions —
        <b style='color:#ffffff;'>larger than France and Germany combined.</b>
        This represents an irreversible loss of biodiversity and carbon storage.
    </span>
</div>
""", unsafe_allow_html=True)

st.divider()

# ── KPI Cards ─────────────────────────────────────────────────────
st.markdown("<p style='font-size:11px; color:#00ffff; letter-spacing:3px; font-weight:600; margin-bottom:12px;'>📊 KEY METRICS</p>", unsafe_allow_html=True)

k1, k2, k3, k4, k5 = st.columns(5)

with k1:
    total = filtered['loss_km2'].sum()
    st.metric("🌍 TOTAL LOST", f"{total/1000:,.1f}k km²", delta=f"↑ {year_range[0]}–{year_range[1]}", delta_color="inverse")

with k2:
    if selected_regions:
        worst_r = filtered.groupby('region')['loss_km2'].sum().idxmax()
        worst_v = filtered.groupby('region')['loss_km2'].sum().max()
        st.metric("🔴 HARDEST HIT", worst_r, delta=f"{worst_v/1000:,.1f}k km²", delta_color="inverse")

with k3:
    if len(filtered) > 0:
        wr = filtered.loc[filtered['loss_km2'].idxmax()]
        st.metric("📅 WORST YEAR", str(int(wr['year'])), delta=f"{wr['loss_km2']:,.0f} km²", delta_color="inverse")

with k4:
    avg = filtered.groupby('year')['loss_km2'].sum().mean()
    st.metric("📈 AVG / YEAR", f"{avg/1000:,.1f}k km²", delta="annual average", delta_color="off")

with k5:
    per_day = total / (365 * (year_range[1] - year_range[0] + 1))
    st.metric("⏱️ LOSS / DAY", f"{per_day:,.1f} km²", delta="every single day", delta_color="inverse")

st.divider()

# ── Impact context ────────────────────────────────────────────────
st.markdown("<p style='font-size:11px; color:#00ffff; letter-spacing:3px; font-weight:600; margin-bottom:12px;'>🌍 SCALE OF DESTRUCTION</p>", unsafe_allow_html=True)

region_data = [
    ('Amazon', '#ff4757', '🔴', 'Larger than Egypt', 'Worst year: 2024 (82,574 km²)', 'Agricultural expansion\n& cattle ranching'),
    ('SE Asia', '#ffa502', '🟠', 'Larger than Texas', 'Worst year: 2016 (55,483 km²)', 'Palm oil industry\n& logging'),
    ('Congo',   '#00ff99', '🟢', 'Larger than UK',    'Worst year: 2017 (22,174 km²)', 'Subsistence farming\n& charcoal production'),
    ('India',   '#00d2ff', '🔵', 'Larger than Kentucky','Worst year: 2017 (8,803 km²)', 'Infrastructure\n& urbanization'),
]

cols = st.columns(4)
for col, (region, color, emoji, scale, worst, cause) in zip(cols, region_data):
    total_r = df[df['region']==region]['loss_km2'].sum()
    with col:
        st.markdown(f"""
        <div style='background:linear-gradient(135deg, #011a1f, #010e10);
                    border:1px solid {color}33; border-top: 2px solid {color};
                    border-radius:16px; padding:20px; text-align:center; height:100%;'>
            <div style='font-size:28px; margin-bottom:8px;'>{emoji}</div>
            <div style='font-size:18px; font-weight:800; color:{color};
                        text-shadow: 0 0 20px {color}66;'>{region}</div>
            <div style='font-size:28px; font-weight:900; color:#ffffff; margin:10px 0;
                        font-family: JetBrains Mono, monospace;'>{total_r/1000:.0f}k</div>
            <div style='font-size:11px; color:#406060; margin-bottom:8px;'>km² total lost</div>
            <div style='font-size:12px; color:#a0c0c0; padding:6px 10px;
                        background:rgba(0,255,255,0.05); border-radius:6px; margin:6px 0;'>
                📐 {scale}
            </div>
            <div style='font-size:11px; color:#ff8888; margin:6px 0;'>⚠️ {worst}</div>
            <div style='font-size:11px; color:#607070; margin-top:8px;'>📌 {cause}</div>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# ── Charts ────────────────────────────────────────────────────────
st.markdown("<p style='font-size:11px; color:#00ffff; letter-spacing:3px; font-weight:600; margin-bottom:12px;'>📈 FOREST LOSS ANALYSIS</p>", unsafe_allow_html=True)

c1, c2 = st.columns(2)

with c1:
    st.markdown("<p style='color:#c0e0e0; font-weight:600; margin-bottom:4px;'>Annual Forest Loss Trend</p>", unsafe_allow_html=True)
    st.caption("Year-by-year loss — hover for exact values")
    fig1 = px.line(filtered, x='year', y='loss_km2', color='region',
                   markers=True, color_discrete_map=COLORS,
                   labels={'loss_km2':'Forest Lost (km²)','year':'Year'})
    fig1.update_traces(line=dict(width=2.5))
    fig1.update_layout(**CHART_LAYOUT, hovermode='x unified')
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    st.markdown("<p style='color:#c0e0e0; font-weight:600; margin-bottom:4px;'>Total Loss by Region</p>", unsafe_allow_html=True)
    st.caption("Cumulative comparison across full period")
    cum = filtered.groupby('region')['loss_km2'].sum().reset_index()
    fig2 = px.bar(cum, x='region', y='loss_km2', color='region',
                  color_discrete_map=COLORS, text='loss_km2',
                  labels={'loss_km2':'Total Lost (km²)'})
    fig2.update_traces(texttemplate='%{text:,.0f}', textposition='outside',
                       marker=dict(line=dict(width=0)),
                       opacity=0.9)
    fig2.update_layout(**CHART_LAYOUT, showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)

# Cumulative area chart
st.markdown("<p style='color:#c0e0e0; font-weight:600; margin-bottom:4px;'>Cumulative Forest Loss Over Time</p>", unsafe_allow_html=True)
st.caption("Accumulated total — steeper slope = accelerating destruction")
dfs = filtered.sort_values(['region','year']).copy()
dfs['cumulative_km2'] = dfs.groupby('region')['loss_km2'].cumsum()
fig3 = px.area(dfs, x='year', y='cumulative_km2', color='region',
               color_discrete_map=COLORS,
               labels={'cumulative_km2':'Cumulative Loss (km²)','year':'Year'})
fig3.update_layout(**CHART_LAYOUT, hovermode='x unified')
st.plotly_chart(fig3, use_container_width=True)

# Heatmap
st.markdown("<p style='color:#c0e0e0; font-weight:600; margin-bottom:4px;'>🔥 Deforestation Heatmap</p>", unsafe_allow_html=True)
st.caption("Colour intensity = forest loss magnitude. Spot the crisis years instantly.")
pivot = filtered.pivot_table(index='region', columns='year', values='loss_km2')
fig4 = go.Figure(data=go.Heatmap(
    z=pivot.values,
    x=[str(y) for y in pivot.columns.tolist()],
    y=pivot.index.tolist(),
    colorscale=[
        [0.0,  '#010e10'],
        [0.2,  '#003333'],
        [0.4,  '#006644'],
        [0.6,  '#ffa502'],
        [0.8,  '#ff6b35'],
        [1.0,  '#ff4757']
    ],
    hoverongaps=False,
    hovertemplate='<b>%{y}</b> · <b>%{x}</b><br>Loss: <b>%{z:,.0f} km²</b><extra></extra>'
))
fig4.update_layout(**{k:v for k,v in CHART_LAYOUT.items() if k != 'margin'}, height=220, margin=dict(t=10, b=10))
st.plotly_chart(fig4, use_container_width=True)

st.divider()

# ── Insights ──────────────────────────────────────────────────────
st.markdown("<p style='font-size:11px; color:#00ffff; letter-spacing:3px; font-weight:600; margin-bottom:12px;'>💡 KEY INSIGHTS</p>", unsafe_allow_html=True)

ins1, ins2, ins3, ins4 = st.columns(4)

insights = [
    ('#00ff99', '🟢', 'India — Policy Works',
     'India shows the lowest loss of all 4 regions. Government reforestation programs like the Green India Mission have kept deforestation significantly below global peers.'),
    ('#ff4757', '🔴', 'Amazon — Crisis Deepening',
     '2024 was the worst year on record with 82,574 km² lost — reversing years of progress made after 2004 policy reforms. Urgent intervention needed.'),
    ('#ffa502', '🟠', 'SE Asia — Palm Oil Threat',
     '723,904 km² lost since 2001, driven by palm oil expansion in Indonesia & Malaysia. This is one of the fastest deforestation rates globally.'),
    ('#00d2ff', '🔵', 'Congo — Silent Crisis',
     'Often overlooked, the Congo Basin is accelerating. Worst year was 2017 and the trend is rising, threatening the world\'s second largest tropical forest.'),
]

for col, (color, emoji, title, body) in zip([ins1, ins2, ins3, ins4], insights):
    with col:
        st.markdown(f"""
        <div style='background:linear-gradient(135deg,#011a1f,#010e10);
                    border:1px solid {color}33; border-left:3px solid {color};
                    border-radius:12px; padding:16px; height:100%;'>
            <div style='font-size:13px; font-weight:700; color:{color}; margin-bottom:8px;'>
                {emoji} {title}
            </div>
            <div style='font-size:12px; color:#80a0a0; line-height:1.6;'>{body}</div>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# ── Timeline ──────────────────────────────────────────────────────
st.markdown("<p style='font-size:11px; color:#00ffff; letter-spacing:3px; font-weight:600; margin-bottom:12px;'>🕐 CRITICAL EVENTS TIMELINE</p>", unsafe_allow_html=True)

events = [
    ('2004', '#ff4757', 'Amazon peaks at 46,703 km² — Brazil launches emergency deforestation controls'),
    ('2009', '#00ff99', 'Amazon drops to 21,571 km² — policies working, historic low at this point'),
    ('2015', '#ffa502', 'SE Asia crisis — El Niño driven fires destroy millions of hectares in Indonesia'),
    ('2016', '#ffa502', 'SE Asia worst year — 55,483 km² lost, largely palm oil driven'),
    ('2017', '#00d2ff', 'Congo & India both hit worst years — growing pressure from agriculture'),
    ('2019', '#ff4757', 'Amazon surges — policy rollbacks lead to sharp increase in Brazil'),
    ('2024', '#ff4757', 'Amazon worst year ever — 82,574 km² lost, all-time record in this dataset'),
]

for year, color, event in events:
    st.markdown(f"""
    <div style='display:flex; align-items:flex-start; gap:16px; padding:10px 0;
                border-bottom:1px solid rgba(0,255,255,0.05);'>
        <div style='min-width:52px; font-size:13px; font-weight:800; color:{color};
                    font-family: JetBrains Mono, monospace;
                    text-shadow: 0 0 10px {color}88;'>{year}</div>
        <div style='width:8px; height:8px; border-radius:50%; background:{color};
                    box-shadow:0 0 8px {color}; margin-top:5px; flex-shrink:0;'></div>
        <div style='font-size:13px; color:#80a0a0; line-height:1.5;'>{event}</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ── Raw data ──────────────────────────────────────────────────────
with st.expander("🛰️ View Raw Satellite Data"):
    st.dataframe(filtered, use_container_width=True)

# ── Footer ────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center; padding:32px 20px 20px 20px;'>
    <div style='font-size:11px; letter-spacing:3px; color:#00ffff; font-weight:600; margin-bottom:8px;'>
        DEFORESTWATCH
    </div>
    <div style='font-size:12px; color:#304040; line-height:1.8;'>
        Built with Google Earth Engine (JavaScript) · Python · Pandas · Plotly · Streamlit<br>
        Data: Hansen Global Forest Change 2025 · University of Maryland · 30m satellite resolution<br>
        <span style='color:#304040;'> Project in satellite data engineering & environmental analytics by Swapni Dubey</span>
    </div>
</div>
""", unsafe_allow_html=True)
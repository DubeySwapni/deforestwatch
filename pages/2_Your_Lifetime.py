import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(
    page_title="Your Lifetime | DeforestWatch",
    page_icon="🧬",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;700&display=swap');
* { font-family: 'Inter', sans-serif; }
.stApp { background-color: #010b0e; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1rem !important; }
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #011a1f, #010e10);
    border: 1px solid rgba(0,255,255,0.2);
    border-radius: 16px;
    padding: 20px !important;
}
[data-testid="stMetricLabel"] { color: #00ffff !important; font-size:11px !important; font-weight:600 !important; letter-spacing:2px !important; text-transform:uppercase !important; }
[data-testid="stMetricValue"] { color: #ffffff !important; font-size:26px !important; font-weight:800 !important; }
[data-testid="stSidebar"] { background:#0d1a0d; border-right:1px solid rgba(0,255,255,0.15); }
hr { border-color: rgba(0,255,255,0.1) !important; }
.stSlider [data-baseweb="slider"] [role="progressbar"] {
    background: linear-gradient(90deg, #00ffff, #00ff99) !important;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_csv('data/deforestation_clean.csv')

df = load_data()
COLORS = {'Amazon':'#ff4757','Congo':'#00ff99','SE Asia':'#ffa502','India':'#00d2ff'}
current_year = datetime.now().year

# ── Hero ──────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center; padding:32px 0 16px 0;'>
    <div style='font-size:11px; letter-spacing:4px; color:#00ffff; font-weight:600; margin-bottom:12px;'>
        🧬 PERSONALISED FOREST LOSS
    </div>
    <h1 style='font-size:46px; font-weight:900; color:#ffffff; margin:0;
               text-shadow: 0 0 40px rgba(0,255,255,0.3);'>
        Forest Lost In
        <span style='color:#00ffff;'>Your Lifetime</span>
    </h1>
    <p style='color:#60a0a0; font-size:15px; margin-top:12px;'>
        Enter your birth year and see exactly how much forest
        has disappeared since you were born
    </p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ── Input ─────────────────────────────────────────────────────────
st.markdown("<p style='font-size:11px; color:#00ffff; letter-spacing:3px; font-weight:600; margin-bottom:16px;'>👤 TELL US ABOUT YOURSELF</p>", unsafe_allow_html=True)

inp1, inp2, inp3 = st.columns([1, 1, 1])

with inp1:
    birth_year = st.slider(
        "🎂 Your Birth Year",
        min_value=2001,
        max_value=2024,
        value=2003,
        help="We only have data from 2001 onwards"
    )

with inp2:
    user_name = st.text_input("📝 Your Name (optional)", placeholder="e.g. Swapni")

with inp3:
    user_country = st.selectbox("🌍 Your Country", [
        "India"
    ])

# ── Calculate ─────────────────────────────────────────────────────
age = current_year - birth_year
lifetime_df = df[df['year'] >= birth_year]
total_lifetime = lifetime_df['loss_km2'].sum()
name_display = user_name if user_name else "You"

# ── Personal headline ─────────────────────────────────────────────
st.markdown(f"""
<div style='background:linear-gradient(135deg, #0a001a, #050010);
            border:2px solid rgba(150,0,255,0.4); border-radius:20px;
            padding:32px; text-align:center; margin:24px 0;'>
    <div style='font-size:14px; color:#a060ff; letter-spacing:2px; margin-bottom:16px;'>
        🎂 {name_display.upper()}, BORN {birth_year} · AGE {age}
    </div>
    <div style='font-size:16px; color:#c0a0e0; margin-bottom:8px;'>
        Since you were born, the world has lost
    </div>
    <div style='font-size:72px; font-weight:900; color:#ffffff;
                font-family: JetBrains Mono, monospace;
                text-shadow: 0 0 40px rgba(150,0,255,0.6);'>
        {total_lifetime/1000:,.0f}k
    </div>
    <div style='font-size:22px; color:#a060ff; font-weight:600;'>km² of forest</div>
    <div style='font-size:14px; color:#604080; margin-top:12px;'>
        Across Amazon · Congo · SE Asia · India
    </div>
</div>
""", unsafe_allow_html=True)

# ── Per region breakdown ──────────────────────────────────────────
st.markdown("<p style='font-size:11px; color:#00ffff; letter-spacing:3px; font-weight:600; margin-bottom:16px;'>🌍 BREAKDOWN BY REGION</p>", unsafe_allow_html=True)

r1, r2, r3, r4 = st.columns(4)

region_cols = [r1, r2, r3, r4]
regions     = ['Amazon', 'SE Asia', 'Congo', 'India']
emojis      = ['🔴', '🟠', '🟢', '🔵']

for col, region, emoji in zip(region_cols, regions, emojis):
    region_lifetime = lifetime_df[lifetime_df['region']==region]['loss_km2'].sum()
    with col:
        color = COLORS[region]
        st.markdown(f"""
        <div style='background:linear-gradient(135deg,#011a1f,#010e10);
                    border:1px solid {color}44; border-top:2px solid {color};
                    border-radius:16px; padding:20px; text-align:center;'>
            <div style='font-size:24px;'>{emoji}</div>
            <div style='font-size:16px; font-weight:700; color:{color}; margin:8px 0;'>{region}</div>
            <div style='font-size:28px; font-weight:900; color:#fff;
                        font-family:JetBrains Mono,monospace;'>{region_lifetime/1000:.1f}k</div>
            <div style='font-size:11px; color:#406060;'>km² since {birth_year}</div>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# ── Timeline chart ────────────────────────────────────────────────
st.markdown("<p style='font-size:11px; color:#00ffff; letter-spacing:3px; font-weight:600; margin-bottom:8px;'>📈 FOREST LOSS DURING YOUR LIFETIME</p>", unsafe_allow_html=True)
st.caption(f"Every bar = one year of forest loss since {birth_year}")

fig = px.bar(
    lifetime_df, x='year', y='loss_km2',
    color='region', color_discrete_map=COLORS,
    labels={'loss_km2': 'Forest Lost (km²)', 'year': 'Year'},
    barmode='stack'
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
# Add birth year line
fig.add_vline(x=birth_year, line_dash='dash', line_color='#00ffff',
              annotation_text=f"← {name_display} born", annotation_font_color='#00ffff')
st.plotly_chart(fig, use_container_width=True)

st.divider()

# ── Fun comparisons ───────────────────────────────────────────────
st.markdown("<p style='font-size:11px; color:#00ffff; letter-spacing:3px; font-weight:600; margin-bottom:16px;'>🤯 SCALE COMPARISONS</p>", unsafe_allow_html=True)

# Area of some Indian states for relatable comparison
comparisons = [
    ('Goa', 3.7, '🏖️'),
    ('Delhi', 1.5, '🏙️'),
    ('Mumbai', 0.6, '🌆'),
    ('Rajasthan', 342.2, '🏜️'),
]

c1, c2 = st.columns(2)
for i, (place, area_km2, icon) in enumerate(comparisons):
    times = total_lifetime / (area_km2 * 1000)
    col = c1 if i % 2 == 0 else c2
    with col:
        st.markdown(f"""
        <div style='background:linear-gradient(135deg,#011a1f,#010e10);
                    border:1px solid rgba(0,255,255,0.12); border-radius:12px;
                    padding:16px; margin:6px 0; display:flex;
                    align-items:center; gap:16px;'>
            <div style='font-size:32px;'>{icon}</div>
            <div>
                <div style='font-size:14px; color:#ffffff; font-weight:600;'>
                    {times:,.0f}× the size of {place}
                </div>
                <div style='font-size:12px; color:#406060; margin-top:4px;'>
                    lost since you were born in {birth_year}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# ── Share card ────────────────────────────────────────────────────
st.markdown("<p style='font-size:11px; color:#00ffff; letter-spacing:3px; font-weight:600; margin-bottom:16px;'>📢 SHARE YOUR STATS</p>", unsafe_allow_html=True)

share_text = f"Since I was born in {birth_year}, {total_lifetime/1000:,.0f}k km² of forest has been lost worldwide. That's larger than {user_country} itself. 🌳 #Deforestation #ClimateChange"

st.code(share_text, language=None)
st.caption("Copy and share on social media to raise awareness 🌍")
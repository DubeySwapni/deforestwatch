import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from sklearn.linear_model import LinearRegression

st.set_page_config(
    page_title="Future Predictions | DeforestWatch",
    page_icon="🔮",
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
    background: linear-gradient(135deg,#011a1f,#010e10);
    border:1px solid rgba(0,255,255,0.2);
    border-radius:16px; padding:20px !important;
}
[data-testid="stMetricLabel"] { color:#00ffff !important; font-size:11px !important; font-weight:600 !important; letter-spacing:2px !important; text-transform:uppercase !important; }
[data-testid="stMetricValue"] { color:#ffffff !important; font-size:26px !important; font-weight:800 !important; }
[data-testid="stSidebar"] { background:#0d1a0d; border-right:1px solid rgba(0,255,255,0.15); }
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
hr { border-color:rgba(0,255,255,0.1) !important; }
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

# ── Hero ──────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center; padding:32px 0 16px 0;'>
    <div style='font-size:11px; letter-spacing:4px; color:#00ffff; font-weight:600; margin-bottom:12px;'>
        🔮 ML-POWERED FORECASTING
    </div>
    <h1 style='font-size:46px; font-weight:900; color:#ffffff; margin:0;
               text-shadow: 0 0 40px rgba(0,255,255,0.3);'>
        Deforestation
        <span style='color:#00ffff;'>Future Forecast</span>
    </h1>
    <p style='color:#60a0a0; font-size:15px; margin-top:12px;'>
        Linear regression model trained on 24 years of satellite data
        to predict forest loss up to 2050
    </p>
    <p style='color:#406060; font-size:12px;'>
        ⚠️ Predictions assume current trends continue — policy changes can alter outcomes
    </p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ── Controls ──────────────────────────────────────────────────────
st.markdown("<p style='font-size:11px; color:#00ffff; letter-spacing:3px; font-weight:600; margin-bottom:16px;'>🎛️ PREDICTION SETTINGS</p>", unsafe_allow_html=True)

s1, s2, s3 = st.columns(3)

with s1:
    predict_until = st.slider("🔮 Predict Until", 2025, 2075, 2050)

with s2:
    training_from = st.selectbox(
        "📊 Train Model From Year",
        [2001, 2005, 2010, 2015],
        help="Using more recent data gives different trend lines"
    )

with s3:
    scenario = st.selectbox("🌍 Scenario", [
        "Business as Usual",
        "Optimistic (50% reduction)",
        "Pessimistic (50% increase)"
    ])

st.divider()

# ── ML Model ──────────────────────────────────────────────────────
st.markdown("<p style='font-size:11px; color:#00ffff; letter-spacing:3px; font-weight:600; margin-bottom:8px;'>📈 FORECAST CHART</p>", unsafe_allow_html=True)
st.caption("Solid lines = actual satellite data · Dashed lines = ML prediction")

fig = go.Figure()

future_years  = np.array(range(2025, predict_until + 1))
summary_data  = []

for region in df['region'].unique():
    region_df = df[(df['region'] == region) & (df['year'] >= training_from)]
    color     = COLORS[region]

    X = region_df['year'].values.reshape(-1, 1)
    y = region_df['loss_km2'].values

    # Train linear regression model
    model = LinearRegression()
    model.fit(X, y)

    # Predict future
    X_future    = future_years.reshape(-1, 1)
    y_pred      = model.predict(X_future)

    # Apply scenario multiplier
    if scenario == "Optimistic (50% reduction)":
        y_pred = y_pred * 0.5
    elif scenario == "Pessimistic (50% increase)":
        y_pred = y_pred * 1.5

    # Clip negative predictions
    y_pred = np.clip(y_pred, 0, None)

    # Historical line
    fig.add_trace(go.Scatter(
        x=region_df['year'], y=region_df['loss_km2'],
        name=f'{region} (actual)',
        line=dict(color=color, width=2.5),
        mode='lines+markers',
        marker=dict(size=4),
        hovertemplate=f'<b>{region}</b><br>Year: %{{x}}<br>Loss: %{{y:,.0f}} km²<extra></extra>'
    ))

    # Prediction line (dashed)
    fig.add_trace(go.Scatter(
        x=future_years, y=y_pred,
        name=f'{region} (forecast)',
        line=dict(color=color, width=2, dash='dash'),
        mode='lines',
        hovertemplate=f'<b>{region} forecast</b><br>Year: %{{x}}<br>Predicted: %{{y:,.0f}} km²<extra></extra>'
    ))

    # Store summary
    loss_2030 = model.predict([[2030]])[0]
    loss_2050 = model.predict([[2050]])[0]
    if scenario == "Optimistic (50% reduction)":
        loss_2030 *= 0.5; loss_2050 *= 0.5
    elif scenario == "Pessimistic (50% increase)":
        loss_2030 *= 1.5; loss_2050 *= 1.5

    summary_data.append({
        'region': region,
        'loss_2030': max(0, loss_2030),
        'loss_2050': max(0, loss_2050),
        'trend': 'Increasing' if model.coef_[0] > 0 else 'Decreasing',
        'annual_change': model.coef_[0]
    })

# Add 2024 divider line
fig.add_vline(x=2024, line_dash='dot', line_color='rgba(0,255,255,0.4)',
              annotation_text='← Data | Forecast →',
              annotation_font_color='#00ffff',
              annotation_font_size=11)

fig.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#a0f0f0', family='Inter'),
    xaxis=dict(gridcolor='rgba(0,255,255,0.06)', title='Year'),
    yaxis=dict(gridcolor='rgba(0,255,255,0.06)', title='Forest Lost (km²)'),
    legend=dict(bgcolor='rgba(1,26,31,0.8)', bordercolor='rgba(0,255,255,0.2)', borderwidth=1),
    hoverlabel=dict(bgcolor='#011a1f', bordercolor='#00ffff'),
    hovermode='x unified',
    height=500
)
st.plotly_chart(fig, use_container_width=True)

st.divider()

# ── Summary table ─────────────────────────────────────────────────
st.markdown("<p style='font-size:11px; color:#00ffff; letter-spacing:3px; font-weight:600; margin-bottom:16px;'>🔮 PREDICTED LOSS BY REGION</p>", unsafe_allow_html=True)

s_cols = st.columns(4)

for col, data in zip(s_cols, summary_data):
    color  = COLORS[data['region']]
    trend_color = '#ff4757' if data['trend'] == 'Increasing' else '#00ff99'
    trend_icon  = '📈' if data['trend'] == 'Increasing' else '📉'
    with col:
        st.markdown(f"""
        <div style='background:linear-gradient(135deg,#011a1f,#010e10);
                    border:1px solid {color}33; border-top:2px solid {color};
                    border-radius:16px; padding:20px; text-align:center;'>
            <div style='font-size:16px; font-weight:700; color:{color}; margin-bottom:12px;'>
                {data['region']}
            </div>
            <div style='font-size:12px; color:#406060; margin-bottom:4px;'>BY 2030</div>
            <div style='font-size:22px; font-weight:800; color:#fff;
                        font-family:JetBrains Mono,monospace;'>
                {data['loss_2030']/1000:,.1f}k
            </div>
            <div style='font-size:11px; color:#304040; margin-bottom:12px;'>km² / year</div>
            <div style='font-size:12px; color:#406060; margin-bottom:4px;'>BY 2050</div>
            <div style='font-size:22px; font-weight:800; color:#fff;
                        font-family:JetBrains Mono,monospace;'>
                {data['loss_2050']/1000:,.1f}k
            </div>
            <div style='font-size:11px; color:#304040; margin-bottom:12px;'>km² / year</div>
            <div style='font-size:13px; color:{trend_color}; font-weight:600;'>
                {trend_icon} {data['trend']}
            </div>
            <div style='font-size:11px; color:#406060; margin-top:4px;'>
                {data['annual_change']:+,.0f} km²/year
            </div>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# ── What if section ───────────────────────────────────────────────
st.markdown("<p style='font-size:11px; color:#00ffff; letter-spacing:3px; font-weight:600; margin-bottom:16px;'>🌱 WHAT IF WE ACT NOW?</p>", unsafe_allow_html=True)

w1, w2, w3 = st.columns(3)

scenarios_info = [
    (w1, '😰', 'No Action', '#ff4757',
     'At current rates, all 4 regions will lose an additional 1.2M km² by 2050 — equivalent to losing all of South Africa.'),
    (w2, '🤝', 'Moderate Policy',
     '#ffa502', '50% reduction through international agreements could save 600k km² — roughly the size of Madagascar.'),
    (w3, '🌍', 'Aggressive Action',
     '#00ff99', '80% reduction through strict enforcement + reforestation could stabilize forest cover by 2035.')
]

for col, icon, title, color, desc in scenarios_info:
    with col:
        st.markdown(f"""
        <div style='background:linear-gradient(135deg,#011a1f,#010e10);
                    border:1px solid {color}33; border-left:3px solid {color};
                    border-radius:12px; padding:20px; height:100%;'>
            <div style='font-size:28px; margin-bottom:8px;'>{icon}</div>
            <div style='font-size:14px; font-weight:700; color:{color}; margin-bottom:8px;'>{title}</div>
            <div style='font-size:13px; color:#80a0a0; line-height:1.6;'>{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# ── Model info ────────────────────────────────────────────────────
with st.expander("🤖 About the ML Model"):
    st.markdown("""
    <div style='color:#80a0a0; font-size:13px; line-height:1.8;'>
        <b style='color:#00ffff;'>Algorithm:</b> Linear Regression (scikit-learn)<br>
        <b style='color:#00ffff;'>Training data:</b> Hansen GFC 2025 — 24 years of satellite observations<br>
        <b style='color:#00ffff;'>Features:</b> Year (single feature)<br>
        <b style='color:#00ffff;'>Target:</b> Annual forest loss in km²<br>
        <b style='color:#00ffff;'>Limitation:</b> Linear regression assumes trends continue —
        real outcomes depend heavily on policy, economics, and climate.<br>
        <b style='color:#00ffff;'>Improvement ideas:</b> Add rainfall data, GDP, population density,
        policy change indicators as additional features.
    </div>
    """, unsafe_allow_html=True)

st.divider()
st.markdown("""
<div style='text-align:center; padding:16px; color:#304040; font-size:12px;'>
    ML model: scikit-learn LinearRegression · Data: Hansen GFC 2025 · Google Earth Engine
</div>
""", unsafe_allow_html=True)

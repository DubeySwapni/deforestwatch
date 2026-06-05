import pandas as pd
import plotly.express as px

df = pd.read_csv('data/deforestation_clean.csv')

COLORS = {
    'Amazon': '#e74c3c',
    'Congo':  '#27ae60',
    'SE Asia':'#f39c12'
}

# ── Chart 1: Line chart — annual trend ───────────────────────────
fig1 = px.line(
    df,
    x='year',
    y='loss_km2',
    color='region',
    markers=True,
    title='Annual Forest Loss by Region (2001–2024)',
    labels={'loss_km2': 'Forest Lost (km²)', 'year': 'Year'},
    color_discrete_map=COLORS
)
fig1.update_layout(
    plot_bgcolor='white',
    hovermode='x unified',
    title_font_size=18
)
fig1.write_image('charts/chart_trend.png')
fig1.write_html('charts/chart_trend.html')
print('✅ Chart 1 saved — trend line')

# ── Chart 2: Bar chart — total loss comparison ────────────────────
cumulative = df.groupby('region')['loss_km2'].sum().reset_index()
cumulative['loss_km2'] = cumulative['loss_km2'].round(1)

fig2 = px.bar(
    cumulative,
    x='region',
    y='loss_km2',
    color='region',
    title='Total Forest Loss 2001–2024 (km²)',
    labels={'loss_km2': 'Total Forest Lost (km²)'},
    color_discrete_map=COLORS,
    text='loss_km2'
)
fig2.update_traces(texttemplate='%{text:,.0f} km²', textposition='outside')
fig2.update_layout(
    plot_bgcolor='white',
    showlegend=False,
    title_font_size=18
)
fig2.write_image('charts/chart_totals.png')
fig2.write_html('charts/chart_totals.html')
print('✅ Chart 2 saved — totals bar chart')

# ── Chart 3: Area chart — cumulative loss over time ───────────────
df_sorted = df.sort_values(['region','year'])
df_sorted['cumulative_km2'] = df_sorted.groupby('region')['loss_km2'].cumsum()

fig3 = px.area(
    df_sorted,
    x='year',
    y='cumulative_km2',
    color='region',
    title='Cumulative Forest Loss Over Time (km²)',
    labels={'cumulative_km2': 'Cumulative Loss (km²)', 'year': 'Year'},
    color_discrete_map=COLORS
)
fig3.update_layout(
    plot_bgcolor='white',
    hovermode='x unified',
    title_font_size=18
)
fig3.write_image('charts/chart_cumulative.png')
fig3.write_html('charts/chart_cumulative.html')
print('✅ Chart 3 saved — cumulative area chart')

print('\n🎉 All charts saved in charts/ folder!')
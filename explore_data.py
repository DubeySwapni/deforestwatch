import pandas as pd

# Load your data
df = pd.read_csv('data/deforestation_data.csv')

# Remove columns GEE adds that we don't need
df = df.drop(columns=['.geo', 'system:index'], errors='ignore')

# Make sure year is a number
df['year'] = df['year'].astype(int)

# Round loss to 1 decimal
df['loss_km2'] = df['loss_km2'].round(1)

# Show first 10 rows
print("=== First 10 rows ===")
print(df.head(10))

# Show total loss per region
print("\n=== Total forest lost per region (km²) ===")
print(df.groupby('region')['loss_km2'].sum().sort_values(ascending=False))

# Show worst single year per region
print("\n=== Worst year per region ===")
print(df.loc[df.groupby('region')['loss_km2'].idxmax()][['region','year','loss_km2']])

# Save cleaned data
df.to_csv('data/deforestation_clean.csv', index=False)
print("\n✅ Cleaned data saved!")
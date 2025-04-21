import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd

st.set_page_config(page_title="Terrorism Analysis Dashboard", layout="wide")
st.title("🌍 Global Terrorist Attacks - Data Visualization")

# Load and concatenate datasets
@st.cache_data
def load_data():
    data = pd.read_csv(r'C:\Users\rawat\PycharmProjects\PythonProject\a.csv', encoding='ISO-8859-1', low_memory=False)
    data1 = pd.read_csv(r'C:\Users\rawat\PycharmProjects\PythonProject\b.csv', encoding='ISO-8859-1', low_memory=False)
    data2 = pd.read_csv(r'C:\Users\rawat\PycharmProjects\PythonProject\c.csv', encoding='ISO-8859-1', low_memory=False)
    data3 = pd.read_csv(r'C:\Users\rawat\PycharmProjects\PythonProject\d.csv', encoding='ISO-8859-1', low_memory=False)
    df = pd.concat([data, data1, data2, data3], ignore_index=True)
    return df

df = load_data()

# Final dataset load
df = pd.read_csv(r'C:\Users\rawat\PycharmProjects\PythonProject\df.csv', encoding='ISO-8859-1', low_memory=False)

# Plot 1: Attacks Per Year
st.subheader("📈 Number of Terrorist Attacks Per Year")
attacks_per_year = df['iyear'].value_counts().sort_index()
fig, ax = plt.subplots(figsize=(12,6))
sns.lineplot(x=attacks_per_year.index, y=attacks_per_year.values, marker="o", ax=ax)
ax.set(title="Number of Terrorist Attacks Per Year", xlabel="Year", ylabel="Number of Attacks")
ax.grid(True)
st.pyplot(fig)

# Plot 2: Deadliest Years
st.subheader("☠️ Total Deaths from Terrorist Attacks Per Year")
deadly_years = df.groupby('iyear')['nkill'].sum()
fig, ax = plt.subplots(figsize=(12,6))
sns.lineplot(x=deadly_years.index, y=deadly_years.values, marker="o", color="red", ax=ax)
ax.set(title="Total Deaths from Terrorist Attacks Per Year", xlabel="Year", ylabel="Number of Deaths")
ax.grid(True)
st.pyplot(fig)

# Plot 3: Top Countries
st.subheader("🌍 Top 10 Countries by Number of Attacks")
top_countries = df['country_txt'].value_counts().head(10)
fig, ax = plt.subplots(figsize=(10,6))
sns.barplot(y=top_countries.index, x=top_countries.values, ax=ax, palette='viridis')
ax.set(title="Top 10 Countries by Number of Attacks", xlabel="Number of Attacks")
st.pyplot(fig)

# Plot 4: Attack Types
st.subheader("💣 Most Common Types of Attacks")
attack_types = df['attacktype1_txt'].value_counts()
fig, ax = plt.subplots(figsize=(10,6))
sns.barplot(y=attack_types.index, x=attack_types.values, ax=ax, palette='magma')
ax.set(title="Most Common Types of Attacks", xlabel="Number of Attacks")
st.pyplot(fig)

# Plot 5: Deadliness by Attack Type
st.subheader("💀 Average Number of People Killed by Attack Type")
deadly_attacks = df.groupby('attacktype1_txt')['nkill'].mean().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(10,6))
sns.barplot(x=deadly_attacks.values, y=deadly_attacks.index, ax=ax, palette='Reds')
ax.set(title="Average Number of People Killed by Attack Type", xlabel="Average Kill Count")
st.pyplot(fig)

# Plot 6: Target Types
st.subheader("🎯 Most Targeted Groups / Entities")
target_types = df['targtype1_txt'].value_counts().head(10)
fig, ax = plt.subplots(figsize=(10,6))
sns.barplot(y=target_types.index, x=target_types.values, ax=ax, palette='cubehelix')
ax.set(title="Most Targeted Groups / Entities", xlabel="Number of Attacks")
st.pyplot(fig)

# Summary Stats
st.subheader("📊 Summary Statistics")
total_killed = int(df['nkill'].sum())
total_wounded = int(df['nwound'].sum())
suicide_attacks = df[df['suicide'] == 1].shape[0]

st.write(f"**Total Killed:** {total_killed}")
st.write(f"**Total Wounded:** {total_wounded}")
st.write(f"**Total Suicide Attacks:** {suicide_attacks}")

if 'propvalue' in df.columns:
    total_damage = df['propvalue'].sum()
    st.write(f"**Total Property Damage Value:** {total_damage}")
else:
    st.warning("Property damage data not available in this version.")

# Plot 7: World Heatmap
st.subheader("🗺️ Global Terrorist Attacks Heatmap")
world = gpd.read_file(r"C:/Users/rawat/Documents/WorldShapefile/ne_110m_admin_0_countries.shp")
country_attacks = df['country_txt'].value_counts().reset_index()
country_attacks.columns = ['NAME', 'Attacks']

merged = world.merge(country_attacks, on='NAME', how='left')
merged['Attacks'] = merged['Attacks'].fillna(0)

fig, ax = plt.subplots(figsize=(15,10))
merged.plot(column='Attacks', cmap='OrRd', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True)
ax.set_title('Global Terrorist Attacks Heatmap')
st.pyplot(fig)

st.success("✅ Analysis Complete!")

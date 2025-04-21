import streamlit as st
import pandas as pd

import seaborn as sns
import geopandas as gpd
import os
import folium
from streamlit_folium import st_folium  # This allows you to display folium maps in Streamlit

# Streamlit App Configuration
st.set_page_config(page_title="Terrorism Data Analysis", layout="centered")

# Shapefile path
shapefile_path = r"C:\Users\rawat\PycharmProjects\PythonProject\ne_110m_admin_0_countries.shp"

# Check if shapefile exists
if not os.path.exists(shapefile_path):
    st.error(f"Shapefile not found at {shapefile_path}. Please check the file path.")
else:
    # Load shapefile
    world = gpd.read_file(shapefile_path)

    # App Title
    st.title("🌍 Global Terrorism Data Dashboard")

    # Load CSV files
    try:
        data = pd.read_csv("a.csv", encoding='ISO-8859-1', low_memory=False)
        data1 = pd.read_csv("b.csv", encoding='ISO-8859-1', low_memory=False)
        data2 = pd.read_csv("c.csv", encoding='ISO-8859-1', low_memory=False)
        data3 = pd.read_csv("d.csv", encoding='ISO-8859-1', low_memory=False)
    except Exception as e:
        st.error(f"Error loading CSV files: {e}")
        st.stop()

    # Combine all datasets
    df = pd.concat([data, data1, data2, data3], ignore_index=True)

    # --- Chart 1: Attacks per Year ---
    st.subheader("📈 Number of Terrorist Attacks Per Year")
    attacks_per_year = df['iyear'].value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.lineplot(x=attacks_per_year.index, y=attacks_per_year.values, marker="o", ax=ax)
    ax.set_title("Attacks Per Year")
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Attacks")
    ax.grid(True)
    st.pyplot(fig)

    # --- Chart 2: Deadliest Years ---
    st.subheader("💀 Total Deaths From Terrorist Attacks Per Year")
    deadly_years = df.groupby('iyear')['nkill'].sum()
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.lineplot(x=deadly_years.index, y=deadly_years.values, marker="o", ax=ax, color="red")
    ax.set_title("Total Deaths Per Year")
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Deaths")
    ax.grid(True)
    st.pyplot(fig)

    # --- Chart 3: Top 10 Countries by Attacks ---
    st.subheader("🌏 Top 10 Countries by Number of Attacks")
    top_countries = df['country_txt'].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(y=top_countries.index, x=top_countries.values, palette='viridis', ax=ax)
    ax.set_title("Top 10 Countries")
    ax.set_xlabel("Number of Attacks")
    st.pyplot(fig)

    # --- Chart 4: Attack Types ---
    st.subheader("💣 Most Common Attack Types")
    attack_types = df['attacktype1_txt'].value_counts()
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(y=attack_types.index, x=attack_types.values, palette='magma', ax=ax)
    ax.set_title("Attack Types")
    ax.set_xlabel("Number of Attacks")
    st.pyplot(fig)

    # --- Chart 5: Deadliness by Attack Type ---
    st.subheader("📊 Average Kill Count by Attack Type")
    deadly_attacks = df.groupby('attacktype1_txt')['nkill'].mean().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(x=deadly_attacks.values, y=deadly_attacks.index, palette='Reds', ax=ax)
    ax.set_title("Average Kills per Attack Type")
    ax.set_xlabel("Average Kill Count")
    st.pyplot(fig)

    # --- Chart 6: Targeted Groups ---
    st.subheader("🎯 Most Targeted Groups/Entities")
    target_types = df['targtype1_txt'].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(y=target_types.index, x=target_types.values, palette='cubehelix', ax=ax)
    ax.set_title("Top Targets")
    ax.set_xlabel("Number of Attacks")
    st.pyplot(fig)

    # --- Summary Statistics ---
    st.subheader("📌 Summary Statistics")
    total_killed = int(df['nkill'].sum(skipna=True))
    total_wounded = int(df['nwound'].sum(skipna=True))
    suicide_attacks = df[df['suicide'] == 1].shape[0]

    st.write(f"💀 **Total Killed:** {total_killed}")
    st.write(f"🩸 **Total Wounded:** {total_wounded}")
    st.write(f"💣 **Total Suicide Attacks:** {suicide_attacks}")

    if 'propvalue' in df.columns:
        total_damage = df['propvalue'].sum(skipna=True)
        st.write(f"🏠 **Total Property Damage Value:** {total_damage}")
    else:
        st.write("⚠️ Property damage data not available.")

    # --- Chart 7: Interactive World Map ---
    st.subheader("🗺️ Global Terrorist Attacks Heatmap")

    # Prepare data for country attacks
    country_attacks = df['country_txt'].value_counts().reset_index()
    country_attacks.columns = ['country_txt', 'attack_count']

    # Create a folium map
    folium_map = folium.Map(location=[20, 0], zoom_start=2)

    # Adding countries to the map with interactive popups
    for _, country in world.iterrows():
        country_name = country['geometry']
        if country_name in country_attacks['country_txt'].values:
            attack_count = country_attacks[country_attacks['country_txt'] == country_name]['attack_count'].values[0]
        else:
            attack_count = 0

        # Adding a popup for each country
        folium.GeoJson(
            country['geometry'],
            tooltip=folium.Tooltip(country_name),
            popup=folium.Popup(f"{country_name}: {attack_count} Attacks", parse_html=True)
        ).add_to(folium_map)

    # Render the map in Streamlit
    st_folium(folium_map, width=700, height=500)

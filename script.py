import pandas as pd
import streamlit as st
import folium
from streamlit_folium import folium_static

# --- 1️⃣ CHARGEMENT DES DONNÉES ---
st.title("📊 Députés & Stress Hydrique en France")

# Charger les données
file_path = "deputy_circo_waterstress_with_coords.xlsx"

try:
    df = pd.read_excel(file_path, engine="openpyxl")

    # Vérifier les valeurs manquantes
    df.fillna({"water_stress_level": "Unknown"}, inplace=True)

    # --- 2️⃣ FILTRAGE INTERACTIF ---
    stress_levels = df["water_stress_level"].unique()
    selected_stress = st.sidebar.multiselect(
        "Filtrer par niveau de stress hydrique", stress_levels, default=stress_levels
    )

    # Champs de filtrage par nom et prénom
    nom_filter = st.sidebar.text_input("Filtrer par nom du député")
    prenom_filter = st.sidebar.text_input("Filtrer par prénom du député")

    # Appliquer les filtres
    filtered_df = df[df["water_stress_level"].isin(selected_stress)]

    if nom_filter:
        filtered_df = filtered_df[
            filtered_df["deputy_lastname"].str.contains(nom_filter, case=False, na=False)
        ]
    
    if prenom_filter:
        filtered_df = filtered_df[
            filtered_df["deputy_firstname"].str.contains(prenom_filter, case=False, na=False)
        ]

    # --- 3️⃣ AFFICHAGE DU TABLEAU ---
    st.write("🔍 Tableau des députés :")
    st.dataframe(filtered_df)

    # --- 4️⃣ CARTE INTERACTIVE ---
    m = folium.Map(location=[46.603354, 1.888334], zoom_start=5)

    # Vérifier que les colonnes nécessaires existent
    if "latitude" in df.columns and "longitude" in df.columns:
        for _, row in filtered_df.iterrows():
            if pd.notnull(row["latitude"]) and pd.notnull(row["longitude"]):
                deputé = f"{row['deputy_firstname']} {row['deputy_lastname']}"
                circo = row["full_circonscription_nb"]
                stress = row["water_stress_level"]

                # Définir une couleur selon le stress hydrique
                color = "red" if stress == "High" else "orange" if stress == "Medium" else "green"

                folium.Marker(
                    location=[row["latitude"], row["longitude"]],
                    popup=f"{deputé} ({circo}) - Stress: {stress}",
                    icon=folium.Icon(color=color),
                ).add_to(m)

        # Afficher la carte
        st.write("🗺️ Carte des Députés et du Stress Hydrique :")
        folium_static(m)

    else:
        st.warning("Les coordonnées (latitude/longitude) ne sont pas disponibles dans le fichier.")

except FileNotFoundError:
    st.error(f"❌ Erreur : Le fichier `{file_path}` est introuvable.")
except Exception as e:
    st.error(f"❌ Une erreur est survenue : {e}")
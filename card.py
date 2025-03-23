import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium  # Utilisation de st_folium pour l'affichage dans Streamlit
from geopy.geocoders import Nominatim

# Charger le fichier enrichi avec les coordonnées
df = pd.read_excel("deputy_circo_waterstress_with_coords.xlsx")

# Initialiser le géocodeur pour la géolocalisation inverse
geolocator = Nominatim(user_agent="geoapiExercises")

# Définir les limites géographiques de la France (environ)
FRANCE_BOUNDS = {
    "north": 51.124199,  # Latitude nord
    "south": 41.303925,  # Latitude sud
    "east": 9.6625,      # Longitude est
    "west": -5.2299      # Longitude ouest
}

# Créer une carte centrée sur la France
m = folium.Map(location=[46.603354, 1.888334], zoom_start=6)

# Fonction pour vérifier si une localisation est dans les limites géographiques de la France
def is_in_france(lat, lon):
    return FRANCE_BOUNDS["south"] <= lat <= FRANCE_BOUNDS["north"] and FRANCE_BOUNDS["west"] <= lon <= FRANCE_BOUNDS["east"]

# Fonction pour déterminer la couleur en fonction du niveau de stress hydrique
def get_color(water_stress_level):
    if "Low (<10%)" in water_stress_level:
        return "green"
    elif "Low - Medium (10-20%)" in water_stress_level:
        return "yellow"
    elif "Medium - High (20-40%)" in water_stress_level:
        return "orange"
    elif "High (40-80%)" in water_stress_level:
        return "red"
    elif "Extremely High (>80%)" in water_stress_level:
        return "purple" 
    return "gray"  # Par défaut si la valeur ne correspond pas

# Ajouter les marqueurs pour chaque circonscription
for _, row in df.iterrows():
    lat, lon = row["latitude"], row["longitude"]
    
    # Vérifier si les coordonnées sont dans les limites géographiques de la France
    if pd.notna(lat) and pd.notna(lon):
        if is_in_france(lat, lon):
            # Déterminer la couleur en fonction du niveau de stress hydrique
            color = get_color(row["water_stress_level"])
            
            # Ajouter un marqueur avec une couleur visible
            folium.CircleMarker(
                location=[lat, lon],
                radius=8,  # Taille du marqueur
                color=color,  # Couleur du cercle
                fill=True,  # Remplissage du cercle
                fill_color=color,  # Couleur de remplissage
                fill_opacity=0.6,  # Opacité du remplissage
                popup=f"{row['deputy_firstname']} {row['deputy_lastname']} - {row['water_stress_level']}",
                tooltip=row['full_circonscription_nb']
            ).add_to(m)

# Afficher la carte dans Streamlit avec st_folium
st.title("🗺️ Carte des Députés et Zones de Stress Hydrique")
st_folium(m)
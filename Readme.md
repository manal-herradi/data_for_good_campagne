# Deputies and Water Stress Zones Map

## Description

This project uses **Streamlit** and **Folium** to display an interactive map of French deputies' constituencies in relation to their water stress levels. The data comes from an Excel file containing the geographic coordinates of deputies and their constituency's water stress levels.

## Features

- **Interactive Map**: Visualize the constituencies of deputies on a map with colored markers representing different levels of water stress.
- **Dynamic Filtering**: Filter deputies by water stress level using an interactive interface in Streamlit.
- **Data Table**: Display filtered data in a table for detailed review.

## Requirements

1. Python 3.x
2. The following libraries must be installed:
    - `streamlit`
    - `folium`
    - `streamlit_folium`
    - `geopy`
    - `pandas`
    - `openpyxl` (for reading Excel files)

You can install them using `pip`:
```bash
pip install streamlit folium streamlit-folium geopy pandas openpyxl
```

## Usage

1. **Load the Data**: The `deputy_circo_waterstress_with_coords.xlsx` file should contain the following columns: `deputy_firstname`, `deputy_lastname`, `latitude`, `longitude`, `water_stress_level`, `full_circonscription_nb`.
2. **Run the Application**: In the terminal, execute the following command to start the Streamlit app:
    ```bash
    streamlit run app.py
    ```
3. **Interactive**: Use the filtering panel in the sidebar to filter deputies by water stress level and view the results on the map.

## How It Works

- **Map**: A map centered on France is generated, and each deputy is represented by a colored marker based on the water stress level of their constituency.
- **Filtering**: Users can select different water stress levels to adjust the displayed data.
- **Deputy Table**: A table with deputy information is displayed based on the applied filter.
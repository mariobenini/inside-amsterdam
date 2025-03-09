import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import geopandas as gpd
from folium.plugins import MarkerCluster

# Set page layout
st.set_page_config(layout="wide")

# Load data
@st.cache_data
def load_data():
    listings = pd.read_csv("data_cleansed/listings_cleansed.csv")
    neighbourhoods = gpd.read_file("data_raw/neighbourhoods.geojson")
    return listings, neighbourhoods

listings, neighbourhoods = load_data()

# Create two columns (1:2 ratio)
col1, col2 = st.columns([1, 2])

# Left column (1/3 of the screen)
with col1:
    st.header("Amsterdam")
    
    # Add "Amsterdam (all areas)" option to the neighborhood filter
    neighbourhood_options = ["Amsterdam (all areas)"] + sorted(listings["neighbourhood_cleansed"].unique())
    neighbourhood = st.selectbox("Filter by Neighbourhood:", neighbourhood_options)

    # Filter data
    if neighbourhood == "Amsterdam (all areas)":
        # Show all listings
        filtered_listings = listings
    else:
        # Show listings for the selected neighborhood and price range
        filtered_listings = listings[
            (listings["neighbourhood_cleansed"] == neighbourhood)
        ]

    # Display analytics
    st.write(f"**Total Listings:** {len(filtered_listings)}")
    st.write(f"**Average Price:** ${filtered_listings['price_cleansed'].mean():.2f}")
    st.write(f"**Most Common Room Type:** {filtered_listings['room_type'].mode()[0]}")

# Right column (2/3 of the screen)
with col2:
    st.header("Map")

    # Create map
    m = folium.Map(location=[listings["latitude"].mean(), listings["longitude"].mean()], zoom_start=12)

    # Highlight the selected neighborhood or the Amsterdam (all areas)
    if neighbourhood == "Amsterdam (all areas)":
        # Highlight the entire city by combining all neighborhood geometries
        city_boundary = neighbourhoods.dissolve()  # Combine all geometries into one
        folium.GeoJson(
            city_boundary,
            name="Amsterdam (all areas)",
            style_function=lambda x: {"fillColor": "yellow", "color": "black", "weight": 2},
        ).add_to(m)
    else:
        # Highlight the selected neighborhood
        selected_neighbourhood_geo = neighbourhoods[neighbourhoods["neighbourhood"] == neighbourhood]
        folium.GeoJson(
            selected_neighbourhood_geo,
            name="Selected Neighbourhood",
            style_function=lambda x: {"fillColor": "yellow", "color": "black", "weight": 2},
        ).add_to(m)

    # Create a MarkerCluster layer
    marker_cluster = MarkerCluster().add_to(m)

    # Add listings to the map with popups
    for _, row in filtered_listings.iterrows():
        popup_content = f"""
        <b>Name:</b> {row['name']}<br>
        <b>Price:</b> ${row['price_cleansed']}<br>
        <b>Room Type:</b> {row['room_type']}<br>
        <b>Reviews:</b> {row['number_of_reviews']}<br>
        <b>Link:</b> <a href="{row['listing_url']}" target="_blank">View Listing</a>
        """
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=5,
            color="blue",
            fill=True,
            fill_color="blue",
            fill_opacity=0.5,
            popup=folium.Popup(popup_content, max_width=300),
        ).add_to(marker_cluster)

    # Save the map to an HTML string
    map_html = m.get_root().render()

    # Embed the map with custom CSS
    st.components.v1.html(
        f"""
        <div style="width: 100%; height: 100vh;">
            {map_html}
        </div>
        """,
        height=800,
    )
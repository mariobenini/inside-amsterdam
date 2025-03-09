import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import geopandas as gpd
from folium.plugins import MarkerCluster
import plotly.express as px

# Set page layout
st.set_page_config(layout="wide")

# Load data
@st.cache_data
def load_data():
    listings = pd.read_csv("data_cleansed/listings_cleansed.csv", converters={"review_scores_rating": str}, parse_dates=["host_since"])
    neighbourhoods = gpd.read_file("data_raw/neighbourhoods.geojson")
    return listings, neighbourhoods

listings, neighbourhoods = load_data()

# Define reusable functions for analysis and visualizations
def rooms_analysis(data):
    st.write('### Rooms')
    st.write(f"**Entire home/apt:** {data.loc[data['room_type']=='Entire home/apt']['room_type'].count()} ({(data.loc[data['room_type']=='Entire home/apt']['room_type'].count())/len(data)*100:.1f}%)")
    st.write(f"**Hotel room:** {data.loc[data['room_type']=='Hotel room']['room_type'].count()} ({(data.loc[data['room_type']=='Hotel room']['room_type'].count())/len(data)*100:.1f}%)")
    st.write(f"**Private room:** {data.loc[data['room_type']=='Private room']['room_type'].count()} ({(data.loc[data['room_type']=='Private room']['room_type'].count())/len(data)*100:.1f}%)")
    st.write(f"**Shared room:** {data.loc[data['room_type']=='Shared room']['room_type'].count()} ({(data.loc[data['room_type']=='Shared room']['room_type'].count())/len(data)*100:.1f}%)")

def values_analysis(data):
    st.write('### Values')
    st.write(f"**Avg Price p/ Night:** €{data['price_cleansed'].mean():.2f}")
    st.write(f"**Avg Minimum Cost for Booking:** €{data['price_cleansed'].mean()*data['minimum_nights'].mean():.2f}")
    st.write(f"**Avg Monthly Income of Hosts:** €{(data['price_cleansed'].mean())*(365-data['availability_365'].mean())/12:.2f}")

def hosts_analysis(data):
    st.write('### Hosts')
    st.write(f"**SuperHosts:** {data['host_is_superhost'].sum()} ({data['host_is_superhost'].sum()/data['host_is_superhost'].count()*100:.1f}%)")
    st.write(f"**Total Hosts:** {len(data['host_id'].unique())}")
    st.write('**New Hosts:**')
    # histogram for quantity of new hosts
    date_counts = data.groupby('host_since').size().reset_index(name='count')
    fig = px.histogram(date_counts, x='host_since', y='count')
    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='New Hosts',
        template='plotly_white',
        bargap=0.1
    )
    st.plotly_chart(fig)

# Sidebar for filters and analytics
with st.sidebar:
    st.header("Inside Amsterdam")
    st.write('---')
    
    # Add "Amsterdam (all areas)" option to the neighborhood filter
    neighbourhood_options = ["Amsterdam (all areas)"] + sorted(listings["neighbourhood_cleansed"].unique())
    neighbourhood = st.selectbox("Filter by Neighbourhood:", neighbourhood_options)

    # Filter data
    if neighbourhood == "Amsterdam (all areas)":
        # Show all listings
        filtered_listings = listings
    else:
        # Show listings for the selected neighborhood
        filtered_listings = listings[
            (listings["neighbourhood_cleansed"] == neighbourhood)
        ]

    # Display analytics
    if neighbourhood == "Amsterdam (all areas)":
        st.subheader("City-Wide Analysis")
        st.write(f"**Total Listings:** {len(filtered_listings)}")

        st.write("**Top 5 Neighborhoods by Listings:**")
        # Create a table for the top 5 neighborhoods by number of listings
        top_neighbourhoods = filtered_listings["neighbourhood_cleansed"].value_counts().nlargest(5).reset_index()
        top_neighbourhoods.columns = ["Neighbourhood", "Listings"]
        top_neighbourhoods.index = top_neighbourhoods.index + 1
        st.dataframe(top_neighbourhoods)

        st.write("**Neighborhoods by Average Price p/ Night:**")
        # Calculate the average price for each neighborhood
        avg_prices = filtered_listings.groupby("neighbourhood_cleansed")["price_cleansed"].mean().round(2).reset_index()
        avg_prices.columns = ["Neighbourhood", "Average Price (€)"]
        # Sort by average price in descending order and get the top 5
        top_avg_prices = avg_prices.sort_values(by="Average Price (€)", ascending=False).reset_index(drop=True)
        top_avg_prices.index = top_avg_prices.index + 1
        st.dataframe(top_avg_prices)

        st.write('---')

        rooms_analysis(filtered_listings)
        st.write('---')
        values_analysis(filtered_listings)
        st.write('---')
        hosts_analysis(filtered_listings)
    else:
        st.subheader("Neighbourhood Analysis")
        st.write(f"**Total Listings:** {len(filtered_listings)} ({(len(filtered_listings)/len(listings))*100:.1f}% of Amsterdam's listings)")
        st.write('---')
        rooms_analysis(filtered_listings)
        st.write('---')
        values_analysis(filtered_listings)
        st.write('---')
        hosts_analysis(filtered_listings)

# Right side of the page
url = "https://insideairbnb.com"
st.write("Data collected on 2024-12-07 by [Inside Airbnb](%s)" % url)

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
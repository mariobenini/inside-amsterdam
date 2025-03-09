# Inside Amsterdam: Airbnb Listings Analysis 🏡🌍

## Overview 📊
This project is a **data analysis and visualization tool** built using **Python** and **Streamlit**. It provides insights into Airbnb listings in **Amsterdam**, allowing users to explore data at both the **city-wide** and **neighborhood** levels. 

The app includes **interactive filters**, **visualizations**, and an **interactive map** to highlight key metrics such as **total listings, prices, room types, and host information**.

---

## Features 🚀

### 🔎 Interactive Filters:
- Filter listings by **neighborhood** or view **city-wide** data.
- Explore specific metrics for selected neighborhoods.

### 📈 Analytics:
#### **City-Wide Analysis:**
- **Total listings** count.
- **Top 5 neighborhoods** by number of listings.
- **Neighborhoods** by average price.

#### **Neighborhood Analysis:**
- Total listings and **percentage of city-wide listings**.
- **Room type** distribution.
- **Average price**, **minimum booking cost**, and **monthly income of hosts**.
- **SuperHosts** and **new hosts over time**.

### 📊 Visualizations:
- **Interactive tables** for top neighborhoods by listings and average price.
- **Histograms** for new hosts over time.

### 🗺️ Interactive Map:
- Highlight **selected neighborhoods** or **the entire city**.
- Display listings as **clickable markers** with popups showing details.

---

## Technologies Used 🛠️
- **Python** 🐍 - Primary programming language.
- **Streamlit** 🎈 - Framework for building the web app.
- **Pandas** 📊 - Data manipulation and analysis.
- **Geopandas** 🌍 - Handling geospatial data.
- **Folium** 🗺️ - Interactive map visualization.
- **Plotly** 📈 - Interactive charts and graphs.

---

## Installation ⚙️
To run this project locally, follow these steps:

### 1️⃣ Clone the Repository:
```bash
git clone https://github.com/your-username/inside-amsterdam.git
cd inside-amsterdam
```

### 2️⃣ Set Up a Virtual Environment (Optional but Recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3️⃣ Install Dependencies:
```bash
pip install -r requirements.txt
```

### 4️⃣ Run the Streamlit App:
```bash
streamlit run app.py
```

### 5️⃣ Access the App:
Open your browser and navigate to: **[http://localhost:8501](http://localhost:8501)**

---

## Data Sources 📂
- **Listings Data:** Cleaned Airbnb listings data (`listings_cleansed.csv`).
- **Neighborhood Boundaries:** GeoJSON file (`neighbourhoods.geojson`) containing neighborhood boundaries for Amsterdam.

---

## Usage 📢
### 🎯 Select a Neighborhood:
- Use the **dropdown menu** in the sidebar to select a specific **neighborhood** or view **city-wide data**.

### 📊 Explore Analytics:
- The **sidebar displays key metrics** and visualizations based on the selected neighborhood or city-wide data.

### 🗺️ Interact with the Map:
- The **main area** displays an **interactive map** highlighting the selected neighborhood or the entire city.
- **Click on markers** to view details about individual listings.

---

## Contributing 🤝
Contributions are welcome! Follow these steps to contribute:

1. **Fork** the repository.
2. Create a new branch: `git checkout -b feature/your-feature-name`.
3. Commit your changes: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin feature/your-feature-name`.
5. **Open a pull request**.

---

## License 📜
This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments 🙌
- Data sourced from [**Inside Airbnb**](https://insideairbnb.com/).
- Built using **Python** and **Streamlit**.

---

## Contact 📬
For any questions or feedback, feel free to reach out! ✉️

---

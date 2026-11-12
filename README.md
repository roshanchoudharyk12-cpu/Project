# AeroWatch: Global & India Air Pollution Intelligence Dashboard 🌍💨

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B.svg)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-5.15%2B-3F4F75.svg)](https://plotly.com/)

**AeroWatch** is an environmental data intelligence platform and interactive dashboard built with Python, Streamlit, and Plotly. It provides planetary air quality benchmarking across 23,463 cities in 175 countries, an in-depth analytics cohort for 2,488 Indian cities, and an evidence-based administrative policy roadmap for urban local bodies.

---

## 🚀 Key Features

- **Global Air Quality Benchmarking**:
  - Comprehensive analysis of 23,463 monitored cities across 175 sovereign nations.
  - Multi-pollutant tracking: AQI, PM2.5, Ozone, NO2, and CO.
  - Country-level aggregation and ranking metrics.

- **India Cohort Deep-Dive**:
  - High-resolution spatial mapping and analysis across 2,488 Indian urban centers.
  - Geo-coordinate mapping for major cities (`geo_data.py`).
  - Identification of PM2.5 particulate monoculture (dominant in ~90% of Indian cities).
  - Geographic disparity analysis (Indo-Gangetic Basin vs. Peninsular & Coastal dispersion).

- **Water Quality Intelligence**:
  - Integration with Indian water quality monitoring data (`Indian_water_data.csv`).

- **Policy & Administrative Blueprint**:
  - Actionable municipal interventions, graded response action plans, and airshed governance recommendations.
  - Comprehensive analytical whitepaper: [`INDIAN_CITIES_AIR_POLLUTION_ANALYSIS.md`](INDIAN_CITIES_AIR_POLLUTION_ANALYSIS.md).

- **Modern Interactive UI**:
  - Responsive Streamlit interface with dark glassmorphism theme, metric cards, interactive maps, and correlation heatmaps.

---

## 📁 Repository Structure

```
Project/
├── .streamlit/
│   └── config.toml                         # Streamlit server & dark theme configuration
├── app.py                                  # Main AeroWatch Streamlit application
├── geo_data.py                             # Geographic coordinates dictionary for Indian cities
├── global air pollution dataset.csv        # Planetary air quality dataset (23,463 cities)
├── Indian_water_data.csv                   # Auxiliary Indian water quality monitoring data
├── INDIAN_CITIES_AIR_POLLUTION_ANALYSIS.md # Detailed analytical whitepaper & policy blueprint
├── eda.py                                  # Exploratory data analysis scripts
├── find_cities.py                          # Coordinate lookup and matching utilities
├── refactor.py                             # Modular refactoring helper script
├── test_st.py                              # Streamlit environment verification test
├── requirements.txt                        # Python dependencies
├── .gitignore                              # Git ignore rules
└── README.md                               # Project overview and documentation
```

---

## 🛠️ Installation & Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/roshanchoudharyk12-cpu/Project.git
   cd Project
   ```

2. **Create and Activate a Virtual Environment** (optional but recommended):
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Linux/macOS:
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the Dashboard**:
   ```bash
   streamlit run app.py
   ```
   The dashboard will open automatically in your browser at `http://localhost:8501`.

---

## 📊 Datasets

- **Global Air Pollution Dataset**: Multi-pollutant readings covering 23,463 cities worldwide (`global air pollution dataset.csv`).
- **Indian Water Quality Monitoring Dataset**: State-wise biochemical parameters and water quality indices (`Indian_water_data.csv`).

---

## 📄 License & Attribution

This project is created for environmental analytics, data science research, and public health policy planning.

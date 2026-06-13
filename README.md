# 🛰️ DeforestWatch — Global Deforestation Tracker

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-239120?style=for-the-badge&logo=plotly&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Google Earth Engine](https://img.shields.io/badge/Google%20Earth%20Engine-4285F4?style=for-the-badge&logo=google&logoColor=white)

> 24 years of satellite-based forest loss monitoring across Amazon, Congo Basin, SE Asia & India — built with real data from Google Earth Engine.

## 🔴 Live Demo
### **[deforest-watch.streamlit.app](https://deforest-watch.streamlit.app)**

---

## 📌 Overview

DeforestWatch is an end-to-end data pipeline and interactive web dashboard that extracts 24 years of satellite imagery data from Google Earth Engine, processes it with Python, and visualizes global deforestation trends across 4 major tropical forest regions from 2001 to 2024.

The project uses the **Hansen Global Forest Change 2025** dataset (University of Maryland / Google) — the gold standard for satellite-based forest monitoring, used by governments, researchers, and conservation organizations worldwide.

---

## 📱 Pages & Features

| Page | Description |
|------|-------------|
| 🌍 **Home Dashboard** | Annual loss trends, cumulative area chart, deforestation heatmap, region cards, key insights, and critical events timeline (2001–2024) |
| 💨 **Carbon Calculator** | Converts km² of forest loss into CO₂ megatonnes with real-world equivalents — flights, cars, homes, and tree offsets |
| 🧬 **Your Lifetime** | Enter your birth year and see exactly how much forest has disappeared since you were born, with region breakdown and size comparisons |
| 🔮 **Future Predictions** | ML-powered forecast to 2050 using scikit-learn Linear Regression with 3 scenario modes — Business as Usual, Optimistic, and Pessimistic |

---

## 🔍 Key Findings

| Region | Total Loss (2001–2024) | Worst Year | Loss That Year |
|--------|----------------------|------------|----------------|
| 🔴 Amazon | 955,300 km² | 2024 | 82,574 km² |
| 🟠 SE Asia | 723,904 km² | 2016 | 55,483 km² |
| 🟢 Congo Basin | 271,177 km² | 2017 | 22,174 km² |
| 🔵 India | 94,138 km² | 2017 | 8,803 km² |
| **Total** | **2,044,520 km²** | | |

- 🌍 Combined loss is **larger than France and Germany combined**
- ⏱️ Average of **233 km² lost every single day** across these 4 regions
- 🟢 India shows the **lowest loss** due to active government reforestation programs (Green India Mission)
- 🔴 Amazon 2024 was the **worst year ever recorded** — reversing years of progress after 2004 policy reforms
- 📉 Amazon deforestation dropped 54% from 2004 to 2009, proving that policy intervention works

---

## 🗂️ How the Data Pipeline Works

```
Google Earth Engine (JavaScript API)
        ↓
Load Hansen GFC 2025 — UMD/hansen/global_forest_change_2025_v1_13
        ↓
Filter loss layer by 4 regions × 24 years (2001–2024)
        ↓
Calculate annual forest loss area (km²) at 500m scale
        ↓
Export as CSV to Google Drive
        ↓
Python + Pandas — clean, process, derive metrics
        ↓
Plotly — interactive charts and visualizations
        ↓
Streamlit — multi-page web dashboard
        ↓
Deployed at deforest-watch.streamlit.app
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Satellite data extraction | Google Earth Engine (JavaScript API) |
| Dataset | Hansen Global Forest Change 2025 — `UMD/hansen/global_forest_change_2025_v1_13` |
| Resolution | 30 metres (global coverage) |
| Data processing | Python, Pandas |
| Visualizations | Plotly Express, Plotly Graph Objects |
| Web dashboard | Streamlit (multi-page) |
| ML forecasting | scikit-learn Linear Regression |
| Deployment | Streamlit Cloud |
| Version control | Git, GitHub |

---

## 📡 Dataset Details

**Hansen Global Forest Change 2025**
- **Source:** University of Maryland / Google Earth Engine
- **Dataset ID:** `UMD/hansen/global_forest_change_2025_v1_13`
- **Resolution:** 30 metres
- **Coverage:** Global
- **Period:** 2000–2024
- **Bands used:** `loss` (binary loss mask), `lossyear` (year of loss), `treecover2000` (baseline cover)
- **Export scale:** 500m (for regional aggregation)

---

## 🗂️ Project Structure

```
deforestwatch/
├── Home.py                       # Main dashboard — trends, heatmap, insights
├── pages/
│   ├── 1_Carbon_Calculator.py    # CO₂ emissions calculator with real-world equivalents
│   ├── 2_Your_Lifetime.py        # Personalised forest loss by birth year
│   └── 3_Future_Predictions.py   # ML forecast to 2050 with 3 scenarios
├── data/
│   ├── deforestation_data.csv    # Raw export from Google Earth Engine
│   └── deforestation_clean.csv   # Processed and cleaned dataset
├── requirements.txt              # Python dependencies
├── runtime.txt                   # Python 3.11 specification
└── README.md
```

---

## 🚀 Run Locally

```bash
# Clone the repo
git clone https://github.com/DubeySwapni/deforestwatch
cd deforestwatch

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run Home.py
```

App opens at `http://localhost:8501`

---

## 🌍 Real-World Use Cases

This type of satellite forest monitoring is actively used by:
- **Governments** — tracking policy effectiveness and enforcing forest protection laws
- **Climate researchers** — calculating carbon emissions from land use change for IPCC reports
- **NGOs** — WWF, Greenpeace use this data to detect illegal logging in real time
- **Corporations** — ESG compliance and supply chain deforestation tracking
- **Data journalists** — BBC, NYT, Guardian use Hansen GFC data for environmental reporting

---

## 🤖 About the ML Model

**Algorithm:** Linear Regression (scikit-learn)  
**Training data:** 24 years of Hansen GFC satellite observations (2001–2024)  
**Feature:** Year  
**Target:** Annual forest loss in km² per region  
**Scenarios modelled:**
- Business as Usual — current trend extrapolated
- Optimistic — 50% reduction (policy intervention)
- Pessimistic — 50% increase (accelerating loss)

---

## 👩‍💻 Author

**Swapni Dubey**  
CSE Student  
[GitHub](https://github.com/DubeySwapni)

---

## 📄 License

MIT License — free to use and modify
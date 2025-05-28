
# 💧 82 Below: Chicago Lead Risk Analysis

### Visualizing and Prioritizing Lead Service Line Replacements in Chicago  
[Pranav Kuchibhotla](https://github.com/pranav-here), [Obaid Bin-Mahfoudh](https://github.com/obinmahfoudh), [Sebastian Buzenas](https://github.com/sabuzenas), [Gavin Coffer](https://github.com/c03u5-1), [Thailer Simmons](https://github.com/ThailerSimmons)

*Illinois Institute of Technology, Spring 2025 – IPRO 497*


---

## 🌆 Overview

Chicago has over **400,000 lead service lines**—the most in any U.S. city. Lead exposure, especially in children and vulnerable populations, causes irreversible health effects. Our project aims to:

- Visualize geospatial lead contamination risk
- Analyze seasonal and temperature-driven trends
- Prioritize equitable service line replacement using public health data

**🔗 Live demo:** [82-below.vercel.app](https://82-below.vercel.app)

---

## 📊 Key Components

### 🔹 FOIA + Census-Based Risk Modeling
- Geocoded 400k+ addresses from city inventory and matched with assessor data
- Calculated **Cost of Lead (CoL)** and **Likelihood of Lead (LoL)** scores at the census block group level
- Final **Risk Score** = `CoL × LoL`

### 🔹 Getis-Ord Gi* Hotspot Analysis
- Conducted statistical hotspot mapping across:
  - % of youth population
  - % uninsured
  - Median income
  - % suspected/public/private lead lines
- Combined to highlight tracts where **equity and infrastructure risks intersect**

### 🔹 Seasonal + Temperature Analysis
- Used 10 years of lead sample test data
- Bootstrapped 90th percentile lead levels across seasons
- Found statistically significant increases in **summer/fall**, peaking in **September–October**
- Validated using permutation tests and Euclidean distance metrics

### 🔹 Visual Tools & Outputs
- **Animated choropleths** of rolling 30-day lead 90th percentile levels by ZIP
- **ZIP-level seasonal risk maps** (`Warm Lead90 / Cold Lead90`)
- **Property age risk curves**, residence-type heatmaps, and equity overlays

### 🧭 Public Website: Check My Address Tool

We created a public-facing website to help Chicago residents visualize nearby lead service lines and understand their local risk.

🔗 **Live Site**: [Check your address](https://82-below.vercel.app/check-my-address)

**Key Features:**
- 🔎 **Search by Address** — View nearby service line data for any Chicago location
- 🗺️ **Interactive Map** with markers for:
  - 🔴 Lead / Galvanized Requiring Replacement
  - 🟢 Copper / Not Lead
  - ⚪ Unknown
- 📍 **Details Panel** with:
  - Distance from the searched location
  - Pipe material (Public/Private)
  - Classification of each line
- 🎯 Adjustable search radius (1–20 nearest lines)

**Example Result:**  
Search for `1050 N Harding Ave, Chicago, IL 60651` returns **5 nearby service lines**, all classified as **Lead**:

| Address                      | Classification | Public Material | Private Material | Gooseneck/Pigtail | Distance (ft) |
|-----------------------------|----------------|------------------|------------------|-------------------|---------------|
| 1100 N HARDING AVE          | Lead           | L                | U                | L                 | 145           |
| 1058 N HARDING AVE          | Lead           | L                | L                | L                 | 177           |
| 1103 N HARDING AVE          | Lead           | L                | U                | L                 | 174           |
| 1056 N HARDING AVE          | Lead           | L                | U                | L                 | 189           |
| 1106 N HARDING AVE          | Lead           | L                | U                | L                 | 206           |

📍 **Location Coordinates**:  
Latitude: `41.900553`  
Longitude: `-87.725318`

This result highlights how the tool empowers residents in high-risk zones to discover real risks based on public data.

**Why it matters:**  
With over 400,000 lines in Chicago, this tool offers residents personalized transparency and encourages action—especially in high-risk zones.

---

## 📂 Repository Structure

```
📁 data/               # Raw datasets (FOIA, census, assessor, test results)
📁 scripts/            # Processing, scoring, cleaning (Python)
📁 notebooks/          # EDA, time series, statistical testing
📁 visualizations/     # Heatmaps, choropleths, rolling GIFs, static plots
📁 docs/               # Midterm, final reports, presentation assets
README.md             # You are here
```

### 📦 Full Dataset & High-Resolution Assets

Due to GitHub file size limitations, our **complete raw datasets, GIS files, high-resolution maps, posters, and presentation materials** are hosted externally.

📁 **Access full project assets via OneDrive**:  
🔗 [IPRO 497 S25 – Data Visualization Folder (OneDrive)](https://iit0-my.sharepoint.com/personal/obinmahfoudh_hawk_iit_edu/Documents/IPRO%20497%20S25%20Data%20Visualization)

**Includes:**
- FOIA files and lead test inventory
- Census & ADI demographic data
- Final presentation PDFs and posters
- Animated maps, ArcGIS files, ZIP-level risk tables

Use this folder if you'd like to **reproduce the full analysis or access high-res visuals** that aren’t stored in the GitHub repo.


---

## 📈 Methods + Stats

We employed a combination of spatial analysis, statistical testing, and temporal modeling techniques to build a robust, data-driven understanding of lead contamination in Chicago:

- **📍 Kernel Density Estimation (KDE)**: Used to generate both static and interactive maps showing spatial clusters of lead service lines, highlighting high-density areas across the city.
- **🌡️ Bootstrap Confidence Intervals**: Seasonal lead sample data was bootstrapped 10,000 times to produce reliable, non-parametric confidence intervals for both the mean and 90th percentile lead levels.
- **🎲 Permutation Testing**: Conducted 1,000 permutations to statistically validate the alignment of temperature trends and lead level peaks, confirming a ~2-month lag effect in seasonal risk.
- **🧪 Risk Scoring Framework**: Developed a composite score (`Risk = CoL × LoL`) using social vulnerability indicators (ADI, children under 5) and lead likelihood estimates from infrastructure data.
- **🗺️ Getis-Ord Gi* Hotspot Analysis**: Applied spatial statistics to identify tracts with significantly higher vulnerability and lead presence, combining multiple demographic and infrastructure layers.
- **🎞️ Animated Time Series Visualizations**: Rolling 30-day 90th percentile maps were animated to reveal lead level evolution over time, emphasizing seasonality and data gaps in specific ZIP codes.

These methods allowed us to triangulate where, when, and why lead exposure is most dangerous — forming the basis for our prioritization and public outreach strategies.

---

## 🔥 Key Insights

- **2172**: Estimated full replacement timeline with current budget ($16,000/line, $53M/year)
- **Summer = Risk**: Lead90 peaks lag temperature by ~2 months (confirmed statistically)
- **Most vulnerable ZIPs**: 60608, 60609, 60629, 60644 (stat sig spikes, high Risk Scores)
- **Mid-century homes** (1940–70s) have highest lead levels
- **HERZL Elementary** flagged for extreme seasonal sensitivity

---

## 📌 Recommendations

1. **Targeted Replacements**: Focus on mid-century homes and high-Risk ZIPs
2. **Preemptive Summer Alerts**: Launch campaigns in May
3. **Hotspot Monitoring**: Prioritize statistically validated ZIPs (Risk Score > 1.5)
4. **Grey Zones**: Expand sampling in ZIPs with insufficient test coverage
5. **Public Tooling**: Use ZIP lookup for residents to check risk estimates

---

## 👥 Contributors

- **Pranav Kuchibhotla**: Temp-driven trend analysis, bootstrapping, animated maps, repo + visual design  
- **Obaid Bin-Mahfoudh**: FOIA coordination, risk scoring model, street-level analysis, cost model  
- **Sebastian Buzenas**: ArcGIS visualizations, hotspot analysis, census data integration  
- **Gavin Coffer**: Website (v0.dev), temperature testing, poster edits  
- **Thailer Simmons**: SQL database setup, VM optimization, multithreaded geocoding

---

## 🧠 Acknowledgments

- **Advisor**: Prof. Robert Ellis, College of Computing, Illinois Institute of Technology  
- **Expert**: Elin Betanzo, P.E., Safe Water Engineering  
- **Data Sources**: FOIA Requests, US Census, ADI, City of Chicago, EPA, NOAA

---

## 📄 License

MIT License — See [LICENSE](LICENSE)

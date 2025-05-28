
# 💧 82 Below: Chicago Lead Risk Analysis

### Visualizing and Prioritizing Lead Service Line Replacements in Chicago  
*Pranav Kuchibhotla, Obaid Bin-Mahfoudh, Sebastian Buzenas, Gavin Coffer, Thailer Simmons*  
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

---

## 📈 Methods + Stats

| Method | Description |
|--------|-------------|
| `bootstrap_seasonal.py` | Bootstrap CI for seasonal 90th percentile (Lead90) |
| `permutation_test_temp_vs_lead.py` | Validates temp-lead correlation (p < 0.0001) |
| `LeadDensityAnalysis.py` | KDE and interactive lead maps |
| `Lead_Risk_Mapping.py` | Risk-weighted map markers and clusters |
| `rolling_heatmap_generator.ipynb` | Creates animated 30-day Lead90 choropleths |
| `hotspot_getis_ord.py` | Getis-Ord Gi* hotspot detection and combination |

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

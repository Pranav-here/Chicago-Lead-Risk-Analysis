# Lead Service Line Analysis

## Overview
This project focuses on mapping and analyzing lead service lines using geospatial data. We integrate property data, assessor information, and service line details to visualize areas affected by lead exposure.

## Repository Structure
```
📂 Lead_Service_Line_Analysis/
│── 📂 data/                     # Raw and processed datasets
│── 📂 scripts/                  # Python scripts for data processing & mapping
│── 📂 notebooks/                # Jupyter Notebooks for analysis & visualization
│── 📂 visualizations/           # PNGs, HTML maps, and other visual outputs
│── 📂 docs/                     # Documentation files & reports
│── .gitignore                   # Ignore unnecessary files
│── README.md                    # Project documentation
```

## Data Sources
- **Service Line Data:** Contains geocoded addresses and neighborhood mapping.
- **Assessor Data:** Provides property characteristics and location.

## Setup & Installation
1. Clone this repository:
   ```sh
   git clone https://github.com/your-repo/Lead_Service_Line_Analysis.git
   cd Lead_Service_Line_Analysis
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run Jupyter Notebooks:
   ```sh
   jupyter notebook
   ```

## Key Scripts
| Script | Description |
|--------|-------------|
| `Core_Lead_Service_Line_Visualisation.py` | Generates lead density maps |
| `LeadDensityAnalysis.py` | Analyzes lead risk per neighborhood |
| `PublicPrivateMapping.py` | Differentiates public and private service lines |

## Visualizations
Generated maps and insights are stored in the **`visualizations/`** folder, including:
- `lead_risk_map.png`
- `interactive_lead_density_map.html`

## Contributors
- **Sebastian Buzenas**
- **Obaid Bin-Mahfoudh**
- **Pranav Kuchibhotla**
- **Gavin Coffer**
- **Thailer Simmons**

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

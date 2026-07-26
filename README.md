# UK Crime Data Analysis

Exploring recorded crime across London (and, later, other UK cities) using open
data from the UK police, joined with deprivation and population data.

## Question we're starting with

> How does crime vary across London's boroughs, and how much of that variation
> tracks with deprivation and population?

## Data sources

| Source | What it gives us | Link |
|--------|------------------|------|
| data.police.uk | Street-level crime by month + LSOA | https://data.police.uk/data/ |
| ONS population estimates (mid-2024) | Population per London borough, for per-capita rates | https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/datasets/populationestimatesforukenglandandwalesscotlandandnorthernireland |
| MHCLG Index of Multiple Deprivation 2019 (File 10, borough summaries) | Deprivation score per London borough | https://www.gov.uk/government/statistics/english-indices-of-deprivation-2019 |

**Data is not stored in git** (see `.gitignore`). To reproduce:

- **Crime data**: use the custom download at https://data.police.uk/data/ —
  select "Metropolitan Police Service" and a date range, extract the monthly
  CSVs into `data/raw/london/<year-month>/`.
- **Population data**: download the "mid-2024" xlsx from the ONS link above
  and save it as `data/raw/population/mye24tablesuk.xlsx`.
- **Deprivation data**: from the gov.uk link above, download "File 10:
  Local Authority District Summaries (lower-tier)" and save it as
  `data/raw/deprivation/File_10_LAD_summaries.xlsx`.

## Project structure

```
data/
  raw/         # original, immutable downloads — NEVER edit by hand
  processed/   # cleaned/derived data our code produces
notebooks/     # Jupyter notebooks for exploration & analysis
src/           # reusable Python (cleaning functions, helpers)
outputs/       # figures and exported tables
```

## Setup

```bash
# 1. Create a virtual environment
python -m venv .venv

# 2. Activate it
#    Windows (PowerShell):
.venv\Scripts\Activate.ps1
#    macOS/Linux:
#    source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch Jupyter
jupyter lab
```

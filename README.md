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
| ONS / Index of Multiple Deprivation | Deprivation score per LSOA (added later) | https://www.gov.uk/government/statistics/english-indices-of-deprivation-2019 |
| ONS population estimates | Population per LSOA/borough for per-capita rates (added later) | https://www.ons.gov.uk/ |

**Data is not stored in git** (see `.gitignore`). To reproduce, download the
raw data into `data/raw/` — see notes in `notebooks/`.

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

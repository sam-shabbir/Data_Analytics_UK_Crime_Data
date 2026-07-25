"""Cleaning helpers for the street-level crime data."""

import pandas as pd

# The 32 London boroughs (ONS naming as it appears in LSOA names) plus the
# separate City of London Police force area — together, "Greater London".
LONDON_BOROUGHS = {
    "Barking and Dagenham", "Barnet", "Bexley", "Brent", "Bromley", "Camden",
    "Croydon", "Ealing", "Enfield", "Greenwich", "Hackney",
    "Hammersmith and Fulham", "Haringey", "Harrow", "Havering", "Hillingdon",
    "Hounslow", "Islington", "Kensington and Chelsea", "Kingston upon Thames",
    "Lambeth", "Lewisham", "Merton", "Newham", "Redbridge",
    "Richmond upon Thames", "Southwark", "Sutton", "Tower Hamlets",
    "Waltham Forest", "Wandsworth", "Westminster", "City of London",
}

# Columns identified as redundant/empty during exploration in 01_explore.ipynb.
DROP_COLUMNS = ["Reported by", "Falls within", "LSOA code", "Context", "source_file"]


def clean_crime_data(df: pd.DataFrame) -> pd.DataFrame:
    """Drop the columns we established add no information."""
    # The [c for c in ... if c in df.columns] guard means this won't error
    # if a column's already missing (e.g. if you clean the same df twice).
    return df.drop(columns=[c for c in DROP_COLUMNS if c in df.columns])


def add_borough_column(df: pd.DataFrame) -> pd.DataFrame:
    """Parse a 'Borough' column out of 'LSOA name' (e.g. 'Camden 021A' -> 'Camden').

    rsplit(" ", n=1) splits from the right, at most once, so multi-word
    borough names like 'Kensington and Chelsea 003C' split correctly into
    ['Kensington and Chelsea', '003C'] instead of breaking on every space.
    """
    df = df.copy()
    df["Borough"] = df["LSOA name"].str.rsplit(" ", n=1).str[0]
    return df

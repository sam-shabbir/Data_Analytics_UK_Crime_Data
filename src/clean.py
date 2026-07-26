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

# The 9 local authorities covered by West Mercia Police, confirmed against
# the actual data in notebooks/west-mercia/01_explore.ipynb (LSOA-name
# extraction found these 9 hold the overwhelming majority of rows; ~3% of
# geolocated rows fall just over the Welsh border instead).
WEST_MERCIA_DISTRICTS = {
    "Herefordshire", "Shropshire", "Telford and Wrekin",
    "Bromsgrove", "Malvern Hills", "Redditch", "Worcester", "Wychavon",
    "Wyre Forest",
}

# Some government sources use a different official name than the crime
# data's LSOA names do. Found this because "Herefordshire" alone didn't
# match the ONS population/IMD/boundary files at all -- their official
# name is "Herefordshire, County of" (a ceremonial-county naming quirk).
# Loaders apply this rename right after reading each source, so every
# DataFrame in the project agrees on "Herefordshire".
NAME_ALIASES = {
    "Herefordshire, County of": "Herefordshire",
}

# Columns identified as redundant/empty during exploration in 01_explore.ipynb.
DROP_COLUMNS = ["Reported by", "Falls within", "LSOA code", "Context", "source_file"]


def clean_crime_data(df: pd.DataFrame) -> pd.DataFrame:
    """Drop the columns we established add no information."""
    # The [c for c in ... if c in df.columns] guard means this won't error
    # if a column's already missing (e.g. if you clean the same df twice).
    return df.drop(columns=[c for c in DROP_COLUMNS if c in df.columns])


def add_area_column(df: pd.DataFrame, column_name: str = "Borough") -> pd.DataFrame:
    """Parse an area name out of 'LSOA name' (e.g. 'Camden 021A' -> 'Camden').

    rsplit(" ", n=1) splits from the right, at most once, so multi-word
    area names like 'Kensington and Chelsea 003C' split correctly into
    ['Kensington and Chelsea', '003C'] instead of breaking on every space.
    Rows with a missing 'LSOA name' (e.g. West Mercia's "No Location" rows)
    come out with a missing value here too, rather than erroring — pandas'
    .str methods pass NaN through unchanged.

    `column_name` lets the result be called "Borough" (London) or
    "District" (West Mercia) depending on context, since it's the same
    parsing logic either way.
    """
    df = df.copy()
    df[column_name] = df["LSOA name"].str.rsplit(" ", n=1).str[0]
    return df


def add_borough_column(df: pd.DataFrame) -> pd.DataFrame:
    """London-specific alias for add_area_column — kept so existing London
    notebooks don't need to change."""
    return add_area_column(df, column_name="Borough")

"""Load monthly street-level crime CSVs from data.police.uk into one DataFrame."""

from pathlib import Path

import geopandas as gpd
import pandas as pd

from clean import LONDON_BOROUGHS, NAME_ALIASES

# __file__ is this script's own path. .parent twice walks up:
# src/load_data.py -> src/ -> data-projs/  then down into data/raw.
# Building the path this way means the code works no matter which folder
# you happen to run Python from.
RAW_DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"


def load_force_data(force: str) -> pd.DataFrame:
    """Load and concatenate all monthly CSVs for one police force.

    `force` is the subfolder name under data/raw/, e.g. "london" or
    "west-mercia". Each of those folders contains one sub-folder per
    month (e.g. "2025-05"), each holding one CSV.
    """
    force_dir = RAW_DATA_DIR / force

    # glob("*/*.csv") matches: any folder, then any .csv inside it —
    # i.e. exactly the "month-folder/file.csv" layout the download gave us.
    # sorted() makes sure the months come back in chronological order.
    csv_paths = sorted(force_dir.glob("*/*.csv"))

    if not csv_paths:
        raise FileNotFoundError(f"No CSV files found under {force_dir}")

    frames = []
    for path in csv_paths:
        df = pd.read_csv(path)
        # Tag every row with the file it came from, so if we ever spot
        # something odd we can trace it back to a specific month's file.
        df["source_file"] = path.name
        frames.append(df)

    # concat stacks all the monthly DataFrames on top of each other.
    # ignore_index=True renumbers rows 0..N instead of repeating each
    # month's own 0..N index.
    return pd.concat(frames, ignore_index=True)


def load_population(names: set[str], name_column: str = "Borough") -> pd.DataFrame:
    """Load ONS mid-2024 population estimates for a given set of local authorities.

    Source: ONS "Population estimates for England and Wales: mid-2024" —
    sheet "MYE2 - Persons" holds population by single year of age for every
    UK local authority; we only need the "All ages" total. We filter by
    `names` directly rather than by the sheet's own "Geography" category
    (e.g. "London Borough", "Unitary Authority", "Non-metropolitan
    District"), since a mixed set like West Mercia's 9 districts spans
    several of those categories.
    """
    path = RAW_DATA_DIR / "population" / "mye24tablesuk.xlsx"

    # header=7 tells pandas the real column headers are on the 8th row
    # (0-indexed row 7) of the sheet — the rows above it are ONS cover
    # notes, not data.
    df = pd.read_excel(path, sheet_name="MYE2 - Persons", header=7)
    df["Name"] = df["Name"].replace(NAME_ALIASES)

    result = df[df["Name"].isin(names)][["Name", "All ages"]]
    return result.rename(columns={"Name": name_column, "All ages": "Population"})


def load_borough_population() -> pd.DataFrame:
    """London-specific wrapper around load_population(), kept so existing
    London notebooks don't need to change."""
    return load_population(LONDON_BOROUGHS, name_column="Borough")


def load_deprivation(names: set[str], name_column: str = "Borough") -> pd.DataFrame:
    """Load IMD 2019 local-authority-level deprivation scores for a given set.

    Source: MHCLG "English Indices of Deprivation 2019", File 10 (Local
    Authority District Summaries, lower-tier). This file is pre-aggregated
    to local-authority level by MHCLG themselves, which sidesteps a real
    problem: IMD 2019 is built on 2011 LSOA boundaries, while our crime data
    uses 2021 LSOA boundaries. Reconciling those at LSOA level would need a
    boundary-change lookup table; aggregating first avoids the issue, since
    the local authority boundaries themselves (London boroughs, West
    Mercia's districts) haven't changed.

    Returns one row per area with two independent deprivation measures:
    - IMD_score: the overall composite score (higher = more deprived).
      NOTE: this composite includes a "Crime" sub-domain (~9.3% weight)
      that is itself partly built from recorded police crime data — so
      correlating our crime counts against IMD_score isn't a fully
      independent comparison.
    - Income_score: the Income domain alone (proportion of the population
      experiencing income deprivation). This doesn't include crime data
      at all, so it's a cleaner variable to check IMD_score's story against.
    """
    path = RAW_DATA_DIR / "deprivation" / "File_10_LAD_summaries.xlsx"

    def _load_sheet(sheet_name: str, score_column: str, rename_to: str) -> pd.DataFrame:
        df = pd.read_excel(path, sheet_name=sheet_name, header=0)
        # These government spreadsheets have trailing spaces in column
        # headers (e.g. "IMD - Average score ") — strip them so we can
        # refer to columns cleanly by name.
        df.columns = df.columns.str.strip()
        df["Local Authority District name (2019)"] = (
            df["Local Authority District name (2019)"].replace(NAME_ALIASES)
        )
        df = df[["Local Authority District name (2019)", score_column]]
        return df.rename(columns={
            "Local Authority District name (2019)": name_column,
            score_column: rename_to,
        })

    imd = _load_sheet("IMD", "IMD - Average score", "IMD_score")
    income = _load_sheet("Income", "Income - Average score", "Income_score")
    combined = imd.merge(income, on=name_column, how="left", validate="one_to_one")

    # This file covers all ~317 English local authorities; filter down to
    # just the requested set so this function is self-contained, rather
    # than relying on a caller to filter it later.
    return combined[combined[name_column].isin(names)].reset_index(drop=True)


def load_borough_deprivation() -> pd.DataFrame:
    """London-specific wrapper around load_deprivation(), kept so existing
    London notebooks don't need to change."""
    return load_deprivation(LONDON_BOROUGHS, name_column="Borough")


def load_lad_boundaries(names: set[str], name_column: str = "Borough") -> gpd.GeoDataFrame:
    """Load local authority district boundary polygons for a given set of names.

    Source: ONS local authority district boundaries (2013 vintage), mirrored
    as GeoJSON by the community "UK-GeoJSON" project. 2013 boundaries are
    fine for our purposes: none of the local authorities we work with
    (London boroughs, West Mercia's districts) have changed boundaries
    since then.

    `names` filters the ~326 England-wide districts down to just the ones
    you want (e.g. `clean.LONDON_BOROUGHS`) — a general-purpose function,
    not London-specific, so the same code will serve the West Mercia map
    later. `name_column` lets the output column match whatever you're
    merging it against (e.g. "Borough" for London, "District" for West
    Mercia), instead of hard-coding one name for every use.
    """
    path = RAW_DATA_DIR / "geography" / "england_lad.geojson"

    # geopandas' read_file works like pd.read_csv, but understands
    # geographic file formats (GeoJSON, Shapefile, ...) and returns a
    # GeoDataFrame -- a regular DataFrame plus a "geometry" column holding
    # each row's shape.
    gdf = gpd.read_file(path)
    gdf = gdf.rename(columns={"LAD13NM": name_column})
    gdf[name_column] = gdf[name_column].replace(NAME_ALIASES)

    return gdf[gdf[name_column].isin(names)][[name_column, "geometry"]].reset_index(drop=True)

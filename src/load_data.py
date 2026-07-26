"""Load monthly street-level crime CSVs from data.police.uk into one DataFrame."""

from pathlib import Path

import pandas as pd

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


def load_borough_population() -> pd.DataFrame:
    """Load ONS mid-2024 population estimates for the 33 London boroughs.

    Source: ONS "Population estimates for England and Wales: mid-2024" —
    sheet "MYE2 - Persons" holds population by single year of age for every
    UK local authority; we only need the "All ages" total, and only the
    rows tagged Geography == "London Borough" (which includes the City of
    London, despite the name).
    """
    path = RAW_DATA_DIR / "population" / "mye24tablesuk.xlsx"

    # header=7 tells pandas the real column headers are on the 8th row
    # (0-indexed row 7) of the sheet — the rows above it are ONS cover
    # notes, not data.
    df = pd.read_excel(path, sheet_name="MYE2 - Persons", header=7)

    boroughs = df[df["Geography"] == "London Borough"][["Name", "All ages"]]
    return boroughs.rename(columns={"Name": "Borough", "All ages": "Population"})

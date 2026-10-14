import pandas as pd


REQUIRED_COLUMNS = ["Product Name", "Reviewer", "Review Text"]


def validate_reviews(df: pd.DataFrame) -> pd.DataFrame:
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df = df.dropna(subset=["Review Text"])
    df = df[df["Review Text"].astype(str).str.strip() != ""]
    df = df.drop_duplicates(subset=["Reviewer", "Review Text"])
    return df.reset_index(drop=True)
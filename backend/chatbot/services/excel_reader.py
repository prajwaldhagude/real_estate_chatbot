import pandas as pd

# Basic caching to avoid re-reading file on each request (simple module-level cache)
_cached_df = None

def read_dataset(path: str) -> pd.DataFrame:
    global _cached_df
    if _cached_df is not None:
        return _cached_df.copy()

    # Try CSV then Excel
    if path.lower().endswith('.csv'):
        df = pd.read_csv(path)
    else:
        df = pd.read_excel(path, engine='openpyxl')

    # normalize column names (strip & lowercase)
    df.columns = [str(c).strip().lower() for c in df.columns]

    # common column aliases
    # ensure expected columns exist (locality, year, price, demand)
    # we won't rename automatically but we will try to handle some common names:
    if 'area' in df.columns and 'locality' not in df.columns:
        df.rename(columns={'area':'locality'}, inplace=True)
    if 'location' in df.columns and 'locality' not in df.columns:
        df.rename(columns={'location':'locality'}, inplace=True)
    if 'rate' in df.columns and 'price' not in df.columns:
        df.rename(columns={'rate':'price'}, inplace=True)

    # ensure year numeric if present
    if 'year' in df.columns:
        try:
            df['year'] = pd.to_numeric(df['year'], errors='coerce').astype('Int64')
        except Exception:
            pass

    _cached_df = df
    return df.copy()

def filter_by_locality(df, locality: str):
    if 'locality' in df.columns:
        return df[df['locality'].astype(str).str.contains(locality, case=False, na=False)].copy()
    # try matching against other columns if locality missing
    for col in ['area', 'location', 'place', 'name']:
        if col in df.columns:
            return df[df[col].astype(str).str.contains(locality, case=False, na=False)].copy()
    # fallback: try any string column
    string_cols = df.select_dtypes(include='object').columns
    if len(string_cols):
        mask = False
        for c in string_cols:
            mask = mask | df[c].astype(str).str.contains(locality, case=False, na=False)
        return df[mask].copy()
    return df.iloc[0:0]  # empty

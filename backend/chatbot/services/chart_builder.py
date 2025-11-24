import pandas as pd

def build_price_trend(df):
    """
    Expects df with 'year' and 'price' columns.
    Returns list of dicts: [{"year": 2021, "avg_price": 5400}, ...]
    """
    if 'year' not in df.columns or 'price' not in df.columns:
        return []
    grp = df.dropna(subset=['year', 'price']).groupby('year')['price'].mean().reset_index()
    grp = grp.sort_values('year')
    return grp.rename(columns={'price':'avg_price'}).to_dict(orient='records')

def build_demand_trend(df):
    if 'year' not in df.columns:
        return []
    # demand column may be named differently
    demand_col = None
    for c in ['demand', 'requests', 'interest']:
        if c in df.columns:
            demand_col = c
            break
    if demand_col is None:
        return []
    grp = df.dropna(subset=['year', demand_col]).groupby('year')[demand_col].mean().reset_index()
    grp = grp.sort_values('year')
    return grp.rename(columns={demand_col:'avg_demand'}).to_dict(orient='records')

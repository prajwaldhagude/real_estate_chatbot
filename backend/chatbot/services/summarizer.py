def generate_summary(df, locality):
    """
    Simple rule-based summary. You can replace this with an LLM call for bonus points.
    """
    rows = len(df)
    summary = f"Found {rows} records for {locality}."

    # price growth if possible
    if 'year' in df.columns and 'price' in df.columns:
        try:
            grp = df.dropna(subset=['year','price']).groupby('year')['price'].mean().sort_index()
            if len(grp) >= 2:
                first, last = grp.iloc[0], grp.iloc[-1]
                pct = ((last - first) / first) * 100 if first != 0 else 0
                summary += f" Average price changed from {first:.2f} to {last:.2f} ({pct:.1f}% change)."
        except Exception:
            pass

    # demand observation
    for c in ['demand','requests','interest']:
        if c in df.columns:
            try:
                avg = df[c].dropna().mean()
                summary += f" Average {c} is {avg:.2f}."
                break
            except Exception:
                pass

    return summary

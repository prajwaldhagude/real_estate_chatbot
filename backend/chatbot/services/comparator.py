# backend/chatbot/services/comparator.py
import pandas as pd
from .excel_reader import filter_by_locality
from .chart_builder import build_price_trend, build_demand_trend
from .summarizer import generate_summary

def compare_localities_data(df: pd.DataFrame, localities: list):
    results = {}
    for loc in localities:
        filtered = filter_by_locality(df, loc)
        if filtered.empty:
            results[loc] = {"error": "no data"}
            continue
        summary = generate_summary(filtered, loc)
        price_trend = build_price_trend(filtered)
        demand_trend = build_demand_trend(filtered)
        avg_price = None
        if 'price' in filtered.columns:
            try:
                avg_price = float(filtered['price'].astype(float).mean())
            except Exception:
                avg_price = None
        results[loc] = {
            "summary": summary,
            "price_trend": price_trend,
            "demand_trend": demand_trend,
            "avg_price": avg_price,
            "count": len(filtered)
        }
    # also compute simple ranking by avg_price (higher price -> higher rank)
    ranking = sorted([(loc, v.get('avg_price')) for loc,v in results.items() if v.get('avg_price') is not None],
                     key=lambda x: (x[1] is None, -x[1]))  # highest first
    results['_ranking'] = ranking
    return results

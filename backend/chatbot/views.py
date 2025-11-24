from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .services.excel_reader import read_dataset, filter_by_locality
from .services.chart_builder import build_price_trend, build_demand_trend
from .services.summarizer import generate_summary
from .utils.query_parser import extract_locality


DATA_FILE = r"C:\Users\asus\Desktop\assignments\sigmavalue\real_estate_chatbot\dataset\sampledata.csv"



@api_view(['GET'])
def health_check(request):
    return Response({"status": "ok"})

@api_view(['POST'])
def analyze_locality(request):
    """
    POST JSON:
    { "query": "Analyze Wakad" }
    """
    body = request.data
    query = body.get('query', '') if isinstance(body, dict) else ''
    if not query:
        return Response({"error": "Missing 'query' in request body"}, status=status.HTTP_400_BAD_REQUEST)

    # extract locality from user text
    locality = extract_locality(query)
    if not locality:
        return Response({"error": "Could not determine locality from query"}, status=status.HTTP_400_BAD_REQUEST)

    # load dataset (cached inside read_dataset if you want)
    df = read_dataset(DATA_FILE)

    # filter rows that match locality (case-insensitive substring)
    filtered = filter_by_locality(df, locality)

    if filtered.empty:
        return Response({"error": f"No data found for locality '{locality}'"}, status=status.HTTP_404_NOT_FOUND)

    # summary (mock or simple analysis)
    summary_text = generate_summary(filtered, locality)

    # chart data
    price_chart = build_price_trend(filtered)   # list of {year, avg_price}
    demand_chart = build_demand_trend(filtered) # list of {year, avg_demand} (if demand column exists)

    # table sample (limit to 200 rows to avoid huge payloads)
    table_records = filtered.to_dict(orient='records')[:200]

    return Response({
        "locality": locality,
        "summary": summary_text,
        "chart": {
            "price_trend": price_chart,
            "demand_trend": demand_chart
        },
        "table": table_records,
        "count": len(filtered)
    })

# backend/chatbot/views.py
import os
import io
import pandas as pd
import matplotlib.pyplot as plt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse, FileResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet

from .services.excel_reader import read_dataset, filter_by_locality
from .services.chart_builder import build_price_trend, build_demand_trend
from .services.summarizer import generate_summary
from .services.comparator import compare_localities_data
from django.conf import settings
# ✔ Use YOUR Windows file path
DATA_FILE = os.path.join(settings.BASE_DIR, "dataset", "sampledata.csv")


@api_view(['GET'])
def health_check(request):
    return Response({"status": "ok"})


@api_view(['POST'])
def analyze_locality(request):
    body = request.data
    query = body.get('query', '') if isinstance(body, dict) else ''
    if not query:
        return Response({"error": "Missing 'query' in request body"}, status=status.HTTP_400_BAD_REQUEST)

    df = read_dataset(DATA_FILE)
    filtered = filter_by_locality(df, query)
    if filtered.empty:
        return Response({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)

    summary_text = generate_summary(filtered, query)
    price_chart = build_price_trend(filtered)
    demand_chart = build_demand_trend(filtered)

    table_records = filtered.to_dict(orient='records')[:200]
    return Response({
        "locality": query,
        "summary": summary_text,
        "chart": {
            "price_trend": price_chart,
            "demand_trend": demand_chart
        },
        "table": table_records,
        "count": len(filtered)
    })


@api_view(['POST'])
def compare_localities(request):
    body = request.data
    localities = body.get('localities') if isinstance(body, dict) else None
    if not localities or not isinstance(localities, (list, tuple)) or len(localities) < 1:
        return Response({"error": "Provide 'localities' as a non-empty list"}, status=status.HTTP_400_BAD_REQUEST)

    df = read_dataset(DATA_FILE)
    result = compare_localities_data(df, localities)

    return Response(result)


@api_view(['POST'])
def download_csv(request):
    body = request.data
    locality = body.get('locality')
    if not locality:
        return Response({"error": "Missing 'locality' in request body"}, status=status.HTTP_400_BAD_REQUEST)

    df = read_dataset(DATA_FILE)
    filtered = filter_by_locality(df, locality)
    if filtered.empty:
        return Response({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)

    csv_buffer = io.StringIO()
    filtered.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)

    response = HttpResponse(csv_buffer.getvalue(), content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{locality}_data.csv"'
    return response


@api_view(['POST'])
def download_pdf(request):
    body = request.data
    locality = body.get('locality')
    if not locality:
        return Response({"error": "Missing 'locality' in request body"}, status=status.HTTP_400_BAD_REQUEST)

    df = read_dataset(DATA_FILE)
    filtered = filter_by_locality(df, locality)
    if filtered.empty:
        return Response({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)

    summary_text = generate_summary(filtered, locality)

    price_trend = build_price_trend(filtered)
    years = [p['year'] for p in price_trend]
    prices = [p['avg_price'] for p in price_trend]

    plt.figure()
    plt.plot(years, prices, marker='o')
    plt.title(f'Price Trend - {locality}')
    plt.xlabel('Year')
    plt.ylabel('Avg Price')
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    buf.seek(0)

    pdf_buf = io.BytesIO()
    doc = SimpleDocTemplate(pdf_buf)
    styles = getSampleStyleSheet()
    story = []
    story.append(Paragraph(f"Real Estate Report - {locality}", styles['Title']))
    story.append(Spacer(1, 12))
    story.append(Paragraph(summary_text, styles['BodyText']))
    story.append(Spacer(1, 12))

    img_buf = io.BytesIO(buf.getvalue())
    story.append(Image(img_buf, width=400, height=250))
    story.append(Spacer(1, 12))

    doc.build(story)
    pdf_buf.seek(0)

    return FileResponse(pdf_buf, as_attachment=True, filename=f"{locality}_report.pdf")

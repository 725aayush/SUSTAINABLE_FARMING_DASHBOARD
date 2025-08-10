# app/utils/visualization.py
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import io
import base64

def create_profitability_chart(market_data):
    if not market_data:
        return None

    products = [item["product"] for item in market_data]
    prices = [item["price"] for item in market_data]

    fig, ax = plt.subplots(figsize=(8, 4))
    fig.patch.set_facecolor('#f8f9fa')
    ax.set_facecolor('#f8f9fa')

    bars = ax.bar(products, prices, color=['#4CAF50', '#8BC34A', '#CDDC39', '#FFC107', '#FF9800'])
    ax.set_ylabel('Price (₹/ton)')
    ax.set_title('Top 5 Most Profitable Crops')
    plt.xticks(rotation=45, ha='right')

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2., height, f'₹{height:.2f}', ha='center', va='bottom')

    plt.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)

    return base64.b64encode(buf.read()).decode('utf-8')


def create_sustainability_chart(recommendations):
    if not recommendations:
        return None

    crops = []
    scores = []

    for rec in recommendations:
        crop = rec["suggestion"].split(",")[0].split(":")[-1].strip()
        if not crop or len(crop) > 20:
            crop = "Multiple crops"
        crops.append(crop)
        scores.append(rec["score"])

    fig, ax = plt.subplots(figsize=(6, 4))
    fig.patch.set_facecolor('#f8f9fa')
    ax.set_facecolor('#f8f9fa')

    ax.barh(crops, scores, color='#2E7D32')
    ax.set_xlabel('Sustainability Score')
    ax.set_title('Crop Sustainability Ratings')
    plt.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)

    return base64.b64encode(buf.read()).decode('utf-8')

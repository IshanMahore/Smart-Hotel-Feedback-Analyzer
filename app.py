import os
import csv
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from nlp_analyzer import analyze_feedback, get_suggestion

app = Flask(__name__)

DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'hotel_reviews.csv')


def load_reviews():
    """Loads reviews from the CSV file."""
    reviews = []
    if not os.path.exists(DATA_FILE):
        return reviews
    
    with open(DATA_FILE, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            reviews.append({
                "id": int(row.get("id", 0)),
                "review": row.get("review", "").strip(),
                "sentiment": row.get("sentiment", "Neutral").strip(),
                "aspect": row.get("aspect", "General").strip(),
                "date": row.get("date", "").strip()
            })
    return reviews


def save_review(review_text, sentiment, aspect):
    """Appends a newly analyzed review to the CSV dataset."""
    reviews = load_reviews()
    next_id = max([r["id"] for r in reviews], default=0) + 1
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    new_entry = {
        "id": next_id,
        "review": review_text,
        "sentiment": sentiment,
        "aspect": aspect,
        "date": today_str
    }
    
    file_exists = os.path.exists(DATA_FILE)
    with open(DATA_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["id", "review", "sentiment", "aspect", "date"])
        if not file_exists:
            writer.writeheader()
        writer.writerow(new_entry)
        
    return new_entry


def compute_metrics(reviews):
    """Calculates summary KPIs, distributions, and insights from reviews."""
    total = len(reviews)
    if total == 0:
        return {
            "total": 0, "positive": 0, "negative": 0, "neutral": 0,
            "most_common_complaint": "None", "most_liked_service": "None",
            "aspect_distribution": {}, "sentiment_distribution": {"Positive": 0, "Negative": 0, "Neutral": 0},
            "insights": []
        }

    positive_count = sum(1 for r in reviews if r["sentiment"] == "Positive")
    negative_count = sum(1 for r in reviews if r["sentiment"] == "Negative")
    neutral_count = sum(1 for r in reviews if r["sentiment"] == "Neutral")

    # Aspect counts for complaints (Negative reviews)
    complaint_aspects = {}
    for r in reviews:
        if r["sentiment"] == "Negative":
            asp = r["aspect"]
            complaint_aspects[asp] = complaint_aspects.get(asp, 0) + 1

    # Aspect counts for praises (Positive reviews)
    praised_aspects = {}
    for r in reviews:
        if r["sentiment"] == "Positive":
            asp = r["aspect"]
            praised_aspects[asp] = praised_aspects.get(asp, 0) + 1

    # Total aspect breakdown
    aspect_counts = {}
    for r in reviews:
        asp = r["aspect"]
        aspect_counts[asp] = aspect_counts.get(asp, 0) + 1

    most_common_complaint = max(complaint_aspects, key=complaint_aspects.get) if complaint_aspects else "None"
    most_liked_service = max(praised_aspects, key=praised_aspects.get) if praised_aspects else "None"

    # Actionable Insights Generation
    insights = []
    
    # Cleanliness insight
    clean_pos = sum(1 for r in reviews if r["aspect"] == "Cleanliness" and r["sentiment"] == "Positive")
    clean_total = sum(1 for r in reviews if r["aspect"] == "Cleanliness")
    if clean_total > 0 and (clean_pos / clean_total) >= 0.5:
        insights.append({
            "type": "positive",
            "icon": "fa-sparkles",
            "text": "Guests are generally satisfied with cleanliness and hygiene standards across rooms and lobby."
        })
    else:
        insights.append({
            "type": "warning",
            "icon": "fa-broom",
            "text": "Cleanliness audits are recommended to maintain high guest satisfaction."
        })

    # Complaint insight
    if most_common_complaint != "None":
        count = complaint_aspects[most_common_complaint]
        insights.append({
            "type": "danger",
            "icon": "fa-triangle-exclamation",
            "text": f"{most_common_complaint}-related complaints ({count} reviews) require urgent management attention."
        })

    # Service / staff insight
    staff_pos = sum(1 for r in reviews if r["aspect"] == "Staff" and r["sentiment"] == "Positive")
    staff_total = sum(1 for r in reviews if r["aspect"] == "Staff")
    if staff_total > 0 and (staff_pos / staff_total) >= 0.6:
        insights.append({
            "type": "positive",
            "icon": "fa-users-gear",
            "text": f"Hotel staff & hospitality are strongly commended by guests ({staff_pos} positive mentions)."
        })

    # General trend insight
    pos_pct = round((positive_count / total) * 100, 1)
    insights.append({
        "type": "info",
        "icon": "fa-chart-line",
        "text": f"Overall guest sentiment stands at {pos_pct}% positive feedback across 50 recorded stays."
    })

    return {
        "total": total,
        "positive": positive_count,
        "negative": negative_count,
        "neutral": neutral_count,
        "positive_pct": pos_pct,
        "negative_pct": round((negative_count / total) * 100, 1),
        "neutral_pct": round((neutral_count / total) * 100, 1),
        "most_common_complaint": most_common_complaint,
        "most_liked_service": most_liked_service,
        "sentiment_distribution": {
            "Positive": positive_count,
            "Negative": negative_count,
            "Neutral": neutral_count
        },
        "aspect_distribution": aspect_counts,
        "complaint_distribution": complaint_aspects,
        "praised_distribution": praised_aspects,
        "insights": insights
    }


@app.route("/")
def index():
    """Renders the main single-page application dashboard."""
    return render_template("index.html")


@app.route("/api/dashboard", methods=["GET"])
def get_dashboard_data():
    """Returns analytics data for dashboard charts and metric cards."""
    reviews = load_reviews()
    metrics = compute_metrics(reviews)
    return jsonify(metrics)


@app.route("/api/reviews", methods=["GET"])
def get_reviews():
    """Returns reviews list with optional sentiment filter."""
    sentiment_filter = request.args.get("sentiment", "all").strip().lower()
    reviews = load_reviews()
    
    if sentiment_filter in ["positive", "negative", "neutral"]:
        filtered = [r for r in reviews if r["sentiment"].lower() == sentiment_filter]
    else:
        filtered = reviews
        
    # Return reverse chronological order (newest first)
    return jsonify(list(reversed(filtered)))


@app.route("/api/analyze", methods=["POST"])
def analyze():
    """Analyzes guest feedback text using the NLP pipeline and optionally saves it."""
    data = request.get_json() or {}
    text = data.get("text", "").strip()
    save_to_dataset = data.get("save", False)
    
    if not text:
        return jsonify({"error": "Please enter feedback text to analyze."}), 400
        
    result = analyze_feedback(text)
    
    if save_to_dataset:
        saved_entry = save_review(text, result["sentiment"], result["aspect"])
        result["saved_id"] = saved_entry["id"]
        
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, port=5000)

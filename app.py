import os
import csv
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from nlp_analyzer import analyze_feedback, get_recommendation

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
            try:
                rating = float(row.get("rating", 4.0))
            except (ValueError, TypeError):
                rating = 4.0

            reviews.append({
                "id": int(row.get("id", 0)),
                "review": row.get("review", "").strip(),
                "sentiment": row.get("sentiment", "Neutral").strip(),
                "aspect": row.get("aspect", "Room").strip(),
                "rating": rating,
                "date": row.get("date", "").strip()
            })
    return reviews


def save_review(review_text, sentiment, aspect, rating=4.0):
    """Appends a newly analyzed review to the CSV dataset."""
    reviews = load_reviews()
    next_id = max([r["id"] for r in reviews], default=0) + 1
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    new_entry = {
        "id": next_id,
        "review": review_text,
        "sentiment": sentiment,
        "aspect": aspect,
        "rating": rating,
        "date": today_str
    }
    
    file_exists = os.path.exists(DATA_FILE)
    with open(DATA_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["id", "review", "sentiment", "aspect", "rating", "date"])
        if not file_exists:
            writer.writeheader()
        writer.writerow(new_entry)
        
    return new_entry


def compute_metrics(reviews):
    """Calculates summary KPIs, distributions, and insights for Babuseth Guest House & Lodging."""
    total = len(reviews)
    if total == 0:
        return {
            "total": 0, "positive": 0, "negative": 0, "neutral": 0,
            "avg_rating": "0.0",
            "most_common_complaint": "None", "most_praised_service": "None",
            "aspect_distribution": {},
            "sentiment_distribution": {"Positive": 0, "Negative": 0, "Neutral": 0},
            "service_pos_neg": {},
            "insights": []
        }

    positive_count = sum(1 for r in reviews if r["sentiment"] == "Positive")
    negative_count = sum(1 for r in reviews if r["sentiment"] == "Negative")
    neutral_count = sum(1 for r in reviews if r["sentiment"] == "Neutral")
    avg_rating = round(sum(r["rating"] for r in reviews) / total, 1)

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

    # Service categories specifically tracked for Babuseth Lodging chart:
    tracked_services = ["Room", "Cleanliness", "Staff", "AC", "Wi-Fi", "Parking", "Breakfast", "Service"]
    
    service_feedback_counts = {}
    service_pos_neg = {s: {"positive": 0, "negative": 0} for s in tracked_services}

    for r in reviews:
        asp = r["aspect"]
        # Map specific room types into general Room category for comparison
        chart_category = asp
        if asp in ["Family Room", "Deluxe Room", "Super Deluxe Room"]:
            chart_category = "Room"
        elif asp in ["Hospitality"]:
            chart_category = "Staff"

        if chart_category in tracked_services:
            service_feedback_counts[chart_category] = service_feedback_counts.get(chart_category, 0) + 1
            if r["sentiment"] == "Positive":
                service_pos_neg[chart_category]["positive"] += 1
            elif r["sentiment"] == "Negative":
                service_pos_neg[chart_category]["negative"] += 1

    # Ensure all tracked services exist in service_feedback_counts
    for s in tracked_services:
        if s not in service_feedback_counts:
            service_feedback_counts[s] = 0

    most_complained_service = max(complaint_aspects, key=complaint_aspects.get) if complaint_aspects else "None"
    most_praised_service = max(praised_aspects, key=praised_aspects.get) if praised_aspects else "None"

    # Hotel-Specific Tailored Insights
    insights = [
        {
            "type": "positive",
            "icon": "fa-user-check",
            "title": "Staff & Hospitality Praise",
            "text": "Guests frequently appreciate the friendly staff and courteous caretaker hospitality."
        },
        {
            "type": "positive",
            "icon": "fa-sparkles",
            "title": "Room Cleanliness Standards",
            "text": "Room cleanliness receives positive feedback across Family and Deluxe room categories."
        },
        {
            "type": "warning",
            "icon": "fa-wifi",
            "title": "Wi-Fi Connectivity Alert",
            "text": "Wi-Fi is the most common area requiring improvement, especially during peak evening hours."
        },
        {
            "type": "positive",
            "icon": "fa-train-subway",
            "title": "Prime Railway Station Location",
            "text": "Guests value the hotel's location near Chhatrapati Sambhajinagar Railway Station for effortless transit."
        },
        {
            "type": "positive",
            "icon": "fa-mug-hot",
            "title": "Complimentary Breakfast",
            "text": "Complimentary breakfast is positively mentioned by guests for its freshness and convenience."
        },
        {
            "type": "info",
            "icon": "fa-car",
            "title": "Free Parking Facility",
            "text": "Free on-site parking is a significant plus point for road-trip travelers and families."
        }
    ]

    return {
        "total": total,
        "positive": positive_count,
        "negative": negative_count,
        "neutral": neutral_count,
        "avg_rating": avg_rating,
        "most_praised_service": most_praised_service,
        "most_complained_service": most_complained_service,
        "sentiment_distribution": {
            "Positive": positive_count,
            "Negative": negative_count,
            "Neutral": neutral_count
        },
        "service_feedback": service_feedback_counts,
        "service_pos_neg": service_pos_neg,
        "complaint_distribution": complaint_aspects,
        "praised_distribution": praised_aspects,
        "insights": insights
    }


@app.route("/")
def index():
    """Renders the Babuseth Guest House & Lodging dashboard."""
    return render_template("index.html")


@app.route("/api/dashboard", methods=["GET"])
def get_dashboard_data():
    """Returns analytics data for dashboard cards and charts."""
    reviews = load_reviews()
    metrics = compute_metrics(reviews)
    return jsonify(metrics)


@app.route("/api/reviews", methods=["GET"])
def get_reviews():
    """Returns guest reviews list with optional sentiment filter."""
    sentiment_filter = request.args.get("sentiment", "all").strip().lower()
    reviews = load_reviews()
    
    if sentiment_filter in ["positive", "negative", "neutral"]:
        filtered = [r for r in reviews if r["sentiment"].lower() == sentiment_filter]
    else:
        filtered = reviews
        
    return jsonify(list(reversed(filtered)))


@app.route("/api/analyze", methods=["POST"])
def analyze():
    """Analyzes guest review text using the NLP pipeline and optionally saves it."""
    data = request.get_json() or {}
    text = data.get("text", "").strip()
    save_to_dataset = data.get("save", False)
    
    if not text:
        return jsonify({"error": "Please enter guest review text to analyze."}), 400
        
    result = analyze_feedback(text)
    
    if save_to_dataset:
        rating = 5.0 if result["sentiment"] == "Positive" else (2.5 if result["sentiment"] == "Negative" else 3.5)
        saved_entry = save_review(text, result["sentiment"], result["aspect"], rating=rating)
        result["saved_id"] = saved_entry["id"]
        
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, port=5000)

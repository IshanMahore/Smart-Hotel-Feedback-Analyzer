import re
from textblob import TextBlob

# Aspect Definitions and Keyword Mappings
ASPECT_KEYWORDS = {
    "AC": [
        "ac", "air conditioner", "air conditioning", "aircon", "cooling", "thermostat", "heater", "ventilation"
    ],
    "WiFi": [
        "wifi", "wi-fi", "internet", "connection", "network", "signal", "broadband", "web access"
    ],
    "Cleanliness": [
        "clean", "dirty", "dusty", "stain", "stains", "smell", "odor", "hygiene", "tidy", "messy", "filthy", "spotless", "sanitary"
    ],
    "Staff": [
        "staff", "receptionist", "reception", "manager", "concierge", "bellboy", "waiter", "crew", "employee", "polite", "rude", "hospitality", "attentive"
    ],
    "Food": [
        "food", "breakfast", "dinner", "lunch", "meal", "restaurant", "buffet", "coffee", "tasty", "delicious", "menu", "dining"
    ],
    "Room": [
        "room", "bed", "mattress", "pillow", "bathroom", "shower", "towel", "toilet", "curtain", "spacious", "cramped", "view", "balcony"
    ],
    "Service": [
        "service", "room service", "housekeeping", "check-in", "check-out", "check in", "check out", "delayed", "quick", "prompt", "turnaround"
    ],
    "Price": [
        "price", "cost", "value", "expensive", "cheap", "affordable", "overpriced", "rates", "charge", "worth"
    ],
    "Location": [
        "location", "beach", "city center", "downtown", "airport", "metro", "surroundings", "neighborhood", "convenient", "walkable", "far"
    ],
    "Facilities": [
        "pool", "swimming pool", "gym", "fitness", "parking", "elevator", "lift", "spa", "garden", "lobby", "amenities"
    ]
}

# Recommendations based on aspect and sentiment
SUGGESTIONS = {
    "AC": {
        "Negative": "Check and maintain the room AC and HVAC units regularly to ensure proper cooling and heating.",
        "Positive": "Keep up the consistent HVAC servicing and climate control standards.",
        "Neutral": "Inspect room temperature controls and ensure instructions for AC units are clear for guests."
    },
    "WiFi": {
        "Negative": "Upgrade internet bandwidth, replace aging routers, and enhance Wi-Fi coverage across all guest floors.",
        "Positive": "Maintain high-speed wireless connectivity and robust network security.",
        "Neutral": "Provide easy-to-find Wi-Fi login guides and monitor peak-hour connection speeds."
    },
    "Cleanliness": {
        "Negative": "Reinforce thorough housekeeping quality audits and sanitize rooms and bathrooms meticulously before check-in.",
        "Positive": "Recognize and reward the housekeeping team for outstanding cleanliness standards.",
        "Neutral": "Ensure daily housekeeping routines and linen replacements stay consistent."
    },
    "Staff": {
        "Negative": "Conduct hospitality and customer service refresher training emphasizing empathy, politeness, and problem resolution.",
        "Positive": "Commend the front-desk and support staff for their welcoming and courteous hospitality.",
        "Neutral": "Ensure adequate front-desk staffing during peak check-in and check-out windows."
    },
    "Food": {
        "Negative": "Review culinary recipes, food temperatures, freshness of breakfast items, and dining options with the kitchen team.",
        "Positive": "Continue offering high-quality, varied, and fresh breakfast and dining menus.",
        "Neutral": "Consider expanding the menu variety and offering more dietary-friendly options."
    },
    "Room": {
        "Negative": "Inspect room furnishings, bedding quality, plumbing fixtures, and soundproofing for necessary upgrades.",
        "Positive": "Maintain high room comfort, aesthetic appeal, and quality furnishings across all room tiers.",
        "Neutral": "Ensure all room amenities, lighting, and toiletries are stocked and functioning properly."
    },
    "Service": {
        "Negative": "Streamline front desk and room service response workflows to minimize guest wait times.",
        "Positive": "Sustain prompt turnaround times and proactive guest service.",
        "Neutral": "Monitor service response times and offer direct digital guest assistance channels."
    },
    "Price": {
        "Negative": "Evaluate value-for-money propositions, transparent pricing, and consider bundled amenities or special packages.",
        "Positive": "Maintain competitive pricing and strong guest value propositions.",
        "Neutral": "Clearly communicate included amenities to ensure guests perceive full value for their stay."
    },
    "Location": {
        "Negative": "Provide complimentary shuttle services, transit assistance, and clear navigation guides for guests.",
        "Positive": "Highlight convenient proximity to local landmarks and transit hubs in marketing materials.",
        "Neutral": "Offer detailed local area guides, maps, and nearby transport tips at the front desk."
    },
    "Facilities": {
        "Negative": "Schedule immediate maintenance for on-site amenities such as elevators, gym equipment, or swimming pool areas.",
        "Positive": "Maintain clean, well-managed leisure facilities and fitness centers.",
        "Neutral": "Ensure operating hours and safety guidelines for facilities like the pool and gym are clearly posted."
    },
    "General": {
        "Negative": "Review overall hotel operations and reach out to the guest directly to address their concerns.",
        "Positive": "Thank the guest for their positive remarks and encourage future visits.",
        "Neutral": "Follow up with the guest to understand how their stay experience could be improved."
    }
}

NEGATIVE_PHRASES = [
    "not working", "didn't work", "did not work", "wasn't working", "was not working",
    "never worked", "poor", "terrible", "awful", "horrible", "bad", "slow", "broken",
    "noisy", "rude", "unfriendly", "unhelpful", "disappointed", "disappointing",
    "dirty", "smelly", "leaking", "stain", "stains", "overpriced", "cramped",
    "waste of money", "too small", "cold food", "delayed", "unacceptable", "worst"
]

POSITIVE_PHRASES = [
    "great", "excellent", "amazing", "wonderful", "fantastic", "loved", "friendly",
    "helpful", "spotless", "delicious", "comfortable", "spacious", "perfect",
    "highly recommend", "superb", "exceptional", "peaceful", "pleasant", "best"
]

CONTRAST_CONJUNCTIONS = ["but", "however", "although", "though", "yet", "except"]


def detect_aspect(text: str) -> str:
    """
    Identifies the primary hotel aspect mentioned in the text.
    If multiple aspects exist, gives priority to the clause carrying the sentiment focus
    (e.g., in contrast sentences like 'The room was clean but the AC was not working', AC is prioritized).
    """
    text_lower = text.lower()
    
    # Check for contrast conjunctions (e.g., 'but', 'however') to identify the emphasis clause
    clauses = [text_lower]
    for conj in CONTRAST_CONJUNCTIONS:
        if f" {conj} " in text_lower:
            parts = text_lower.split(f" {conj} ", 1)
            clauses = [parts[1], parts[0]]  # inspect the second clause first
            break

    # Search in priority clause first, then full text
    for clause in clauses:
        for aspect, keywords in ASPECT_KEYWORDS.items():
            for kw in keywords:
                # word boundary match
                pattern = r'\b' + re.escape(kw) + r'\b'
                if re.search(pattern, clause):
                    return aspect

    # Fallback search across all keywords in full text
    for aspect, keywords in ASPECT_KEYWORDS.items():
        for kw in keywords:
            pattern = r'\b' + re.escape(kw) + r'\b'
            if re.search(pattern, text_lower):
                return aspect

    return "General"


def analyze_sentiment(text: str) -> dict:
    """
    Performs sentiment analysis using TextBlob polarity combined with rule-based heuristics
    for contrast phrases and negation cues.
    Returns: { 'sentiment': 'Positive'|'Negative'|'Neutral', 'polarity': float, 'confidence': float }
    """
    text_lower = text.lower()
    blob = TextBlob(text)
    raw_polarity = blob.sentiment.polarity
    
    # Check if contrast sentence exists (e.g., "The room was clean but the AC was not working")
    # In hotel reviews, clauses after 'but' typically represent the overriding guest takeaway.
    effective_text = text_lower
    for conj in CONTRAST_CONJUNCTIONS:
        if f" {conj} " in text_lower:
            parts = text_lower.split(f" {conj} ", 1)
            effective_text = parts[1]
            # Calculate polarity of the second clause
            raw_polarity = TextBlob(effective_text).sentiment.polarity
            break

    # Count negative indicators in effective text
    neg_hits = sum(1 for phrase in NEGATIVE_PHRASES if phrase in effective_text)
    pos_hits = sum(1 for phrase in POSITIVE_PHRASES if phrase in effective_text)

    # Decision logic
    if neg_hits > 0 and neg_hits >= pos_hits:
        sentiment = "Negative"
        adjusted_polarity = -0.5 if raw_polarity >= 0 else raw_polarity
    elif pos_hits > 0 and pos_hits > neg_hits and raw_polarity >= 0:
        sentiment = "Positive"
        adjusted_polarity = 0.5 if raw_polarity <= 0 else raw_polarity
    else:
        if raw_polarity > 0.12:
            sentiment = "Positive"
            adjusted_polarity = raw_polarity
        elif raw_polarity < -0.12:
            sentiment = "Negative"
            adjusted_polarity = raw_polarity
        else:
            sentiment = "Neutral"
            adjusted_polarity = raw_polarity

    return {
        "sentiment": sentiment,
        "polarity": round(adjusted_polarity, 2)
    }


def get_suggestion(aspect: str, sentiment: str) -> str:
    """Returns an actionable recommendation for hotel management."""
    aspect_suggestions = SUGGESTIONS.get(aspect, SUGGESTIONS["General"])
    return aspect_suggestions.get(sentiment, SUGGESTIONS["General"][sentiment])


def analyze_feedback(text: str) -> dict:
    """
    Cognitive computing pipeline:
    1. Input human language
    2. Understand text & detect aspect
    3. Detect sentiment
    4. Generate recommendation
    """
    sentiment_result = analyze_sentiment(text)
    aspect = detect_aspect(text)
    suggestion = get_suggestion(aspect, sentiment_result["sentiment"])
    
    return {
        "text": text,
        "sentiment": sentiment_result["sentiment"],
        "polarity": sentiment_result["polarity"],
        "aspect": aspect,
        "suggestion": suggestion,
        "pipeline_steps": [
            {"step": "1. Human Language Input", "desc": "Captured raw guest feedback text"},
            {"step": "2. Text Understanding", "desc": "Parsed syntactic clauses, negation cues, and domain entities"},
            {"step": "3. Sentiment Detection", "desc": f"Classified as {sentiment_result['sentiment']} (Polarity: {sentiment_result['polarity']})"},
            {"step": "4. Service Identification", "desc": f"Matched hotel department: {aspect}"},
            {"step": "5. Cognitive Recommendation", "desc": suggestion}
        ]
    }

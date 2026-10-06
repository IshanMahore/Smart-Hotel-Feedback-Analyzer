import re
from textblob import TextBlob

# Hotel-specific Aspect Definitions for Babuseth Guest House & Lodging
# NOTE: No dedicated restaurant is present. Dining/Food mapped to 'Breakfast' (Complimentary Breakfast).
ASPECT_KEYWORDS = {
    "Super Deluxe Room": [
        "super deluxe room", "super deluxe", "premium room", "luxury room"
    ],
    "Deluxe Room": [
        "deluxe room", "deluxe"
    ],
    "Family Room": [
        "family room", "family stay", "family suite", "quad room", "triple room"
    ],
    "AC": [
        "ac", "air conditioner", "air conditioning", "aircon", "cooling", "thermostat", "cooling unit", "ac unit"
    ],
    "Wi-Fi": [
        "wi-fi", "wifi", "internet", "network", "signal", "broadband", "connectivity", "connection", "hotspot"
    ],
    "Cleanliness": [
        "clean", "cleanliness", "dirty", "dusty", "stain", "stains", "smell", "odor", "hygiene", "tidy", "messy", "filthy", "spotless", "sanitary", "unhygienic"
    ],
    "Staff": [
        "staff", "receptionist", "reception", "manager", "front desk", "caretaker", "bellboy", "polite", "rude", "attentive", "supportive", "helpful", "friendly staff", "behaviour", "behavior"
    ],
    "Hospitality": [
        "hospitality", "welcome", "warmth", "guest service", "courtesy", "kindness"
    ],
    "Parking": [
        "parking", "car parking", "vehicle parking", "park", "parking space", "bike parking", "parking facility"
    ],
    "Breakfast": [
        "breakfast", "complimentary breakfast", "morning tea", "tea", "coffee", "morning meal", "nashta"
    ],
    "Railway Station": [
        "railway station", "train station", "station", "railway", "train"
    ],
    "Location": [
        "location", "surroundings", "neighborhood", "area", "accessibility", "convenient", "walkable", "far", "near station", "sambhajinagar"
    ],
    "Comfort": [
        "comfort", "comfortable", "uncomfortable", "peaceful", "quiet", "noisy", "soundproof", "sleep"
    ],
    "Maintenance": [
        "maintenance", "broken", "leak", "leaking", "repair", "switch", "tap", "geyser", "hot water", "plumbing", "drain", "water supply"
    ],
    "Room": [
        "room", "bed", "mattress", "pillow", "blanket", "bathroom", "washroom", "toilet", "towel", "spacious", "cramped", "ventilation"
    ],
    "Service": [
        "service", "24 hours service", "24 hour service", "24/7 service", "check-in", "check-out", "check in", "check out", "turnaround", "room service", "assistance"
    ]
}

# Hotel-Specific Tailored Recommendations for Babuseth Guest House & Lodging
ASPECT_RECOMMENDATIONS = {
    "AC": {
        "Negative": "Inspect the AC unit and ensure comfortable room temperature.",
        "Positive": "Keep up regular servicing and efficient cooling standards for all AC rooms.",
        "Neutral": "Verify thermostat controls and supply easy-to-use remote operation guides."
    },
    "Wi-Fi": {
        "Negative": "Check Wi-Fi coverage and improve connection stability.",
        "Positive": "Maintain high-speed wireless coverage across all guest rooms and reception.",
        "Neutral": "Ensure Wi-Fi credentials are clearly visible at reception and signal is tested periodically."
    },
    "Cleanliness": {
        "Negative": "Review room cleaning procedures and inspection frequency.",
        "Positive": "Maintain the current room-cleaning standards.",
        "Neutral": "Ensure routine daily housekeeping checks and timely linen replacement."
    },
    "Staff": {
        "Negative": "Review guest-service processes and staff response time.",
        "Positive": "Continue maintaining the friendly and responsive service.",
        "Neutral": "Brief the front-desk team on proactive guest greetings and prompt assistance."
    },
    "Hospitality": {
        "Negative": "Review guest-service processes and staff response time.",
        "Positive": "Continue maintaining the friendly and responsive service.",
        "Neutral": "Provide standard guest welcome protocols to elevate stay satisfaction."
    },
    "Breakfast": {
        "Negative": "Review complimentary breakfast quality and guest preferences.",
        "Positive": "Maintain timely serving and fresh preparation of the complimentary breakfast.",
        "Neutral": "Monitor breakfast serving schedule and guest intake preferences."
    },
    "Parking": {
        "Negative": "Improve parking availability and clearly communicate parking arrangements.",
        "Positive": "Continue providing secure, well-managed free parking for guest vehicles.",
        "Neutral": "Ensure parking spaces are clearly marked and staff assists guests during arrival."
    },
    "Family Room": {
        "Negative": "Inspect Family Room amenities, bedding arrangement, and ensure ample space.",
        "Positive": "Maintain spacious comfort and family-friendly amenities for group travelers.",
        "Neutral": "Review extra mattress availability and family accommodation setups."
    },
    "Deluxe Room": {
        "Negative": "Address specific Deluxe Room fixtures, linen freshness, and ventilation.",
        "Positive": "Uphold high Deluxe room comfort standards for budget and business travelers.",
        "Neutral": "Ensure all standard amenities in Deluxe rooms are verified prior to check-in."
    },
    "Super Deluxe Room": {
        "Negative": "Inspect Super Deluxe premium fixtures, climate control, and luxury bedding immediately.",
        "Positive": "Sustain the premium experience and superior comfort for Super Deluxe guests.",
        "Neutral": "Maintain top-tier readiness for premium lodging guests."
    },
    "Railway Station": {
        "Negative": "Provide clear station directions and assist guests with soundproofing from rail transit.",
        "Positive": "Promote prime walking convenience from Chhatrapati Sambhajinagar Railway Station.",
        "Neutral": "Provide walking maps and taxi/auto tips from the railway terminal."
    },
    "Location": {
        "Negative": "Assist guests with localized transit tips and landmark directions.",
        "Positive": "Highlight prime proximity to railway station and central hubs in guest guides.",
        "Neutral": "Keep city attraction information and railway schedules handy at reception."
    },
    "Maintenance": {
        "Negative": "Schedule immediate plumbing/electrical repair and log routine facility audits.",
        "Positive": "Maintain prompt preventative maintenance across all guest amenities.",
        "Neutral": "Conduct preventative fixture inspections before assigning rooms."
    },
    "Comfort": {
        "Negative": "Check mattress quality, pillows, and acoustic quietness in the guest wing.",
        "Positive": "Ensure consistent restful ambiance and comfortable bedding.",
        "Neutral": "Offer extra pillows and blankets upon guest request."
    },
    "Service": {
        "Negative": "Streamline 24-hour service response workflows to minimize guest wait times.",
        "Positive": "Commend staff for round-the-clock responsiveness and prompt support.",
        "Neutral": "Ensure active reception coverage and quick desk assistance throughout the night."
    },
    "Room": {
        "Negative": "Check room ventilation, lighting, and bathroom fixtures for required improvements.",
        "Positive": "Maintain tidy, well-appointed guest rooms.",
        "Neutral": "Ensure standard room amenities are pre-checked before guest arrival."
    },
    "General": {
        "Negative": "Review guest feedback directly with the on-duty manager to rectify concerns.",
        "Positive": "Thank the guest for staying with Babuseth Guest House & Lodging.",
        "Neutral": "Follow up with the guest to ensure a seamless lodging experience."
    }
}

NEGATIVE_PHRASES = [
    "not working", "didn't work", "did not work", "wasn't working", "was not working",
    "never worked", "poor", "terrible", "awful", "horrible", "bad", "slow", "broken",
    "noisy", "rude", "unfriendly", "unhelpful", "disappointed", "disappointing",
    "dirty", "smelly", "leaking", "stain", "stains", "uncomfortable", "cramped",
    "delayed", "unacceptable", "worst", "no hot water", "weak", "congested",
    "lack of", "insufficient", "not good", "cold", "hard bed", "difficult"
]

POSITIVE_PHRASES = [
    "great", "excellent", "amazing", "wonderful", "fantastic", "loved", "friendly",
    "helpful", "spotless", "delicious", "comfortable", "spacious", "perfect",
    "highly recommend", "superb", "exceptional", "peaceful", "pleasant", "best",
    "neat", "clean", "fresh", "polite", "smooth", "prompt", "convenient", "cozy",
    "value", "welcoming", "supportive", "tasty", "fast"
]

CONTRAST_CONJUNCTIONS = ["but", "however", "although", "though", "yet", "except", "while"]


def extract_aspect_sentiments(text: str) -> list:
    """
    Analyzes clauses and extracts fine-grained aspect-level sentiments.
    e.g. 'The room was very clean and the staff was friendly, but the Wi-Fi was slow.'
    -> Cleanliness: Positive, Staff: Positive, Wi-Fi: Negative
    """
    text_lower = text.lower()
    detected_aspects = []

    # Break review into clauses via commas, conjunctions, periods, semicolons
    delimiters = r'[,.;]|\bbut\b|\bhowever\b|\band\b|\bwhile\b|\balthough\b'
    raw_clauses = re.split(delimiters, text_lower)
    clauses = [c.strip() for c in raw_clauses if len(c.strip()) > 2]

    found_aspects = {}

    for clause in clauses:
        # Check polarity of this specific clause
        clause_blob = TextBlob(clause)
        c_pol = clause_blob.sentiment.polarity

        has_neg = any(p in clause for p in NEGATIVE_PHRASES)
        has_pos = any(p in clause for p in POSITIVE_PHRASES)

        if has_neg and not has_pos:
            c_sentiment = "Negative"
        elif has_pos and not has_neg:
            c_sentiment = "Positive"
        elif c_pol > 0.1:
            c_sentiment = "Positive"
        elif c_pol < -0.1:
            c_sentiment = "Negative"
        else:
            c_sentiment = "Neutral"

        # Check which aspects are mentioned in this clause
        for aspect, keywords in ASPECT_KEYWORDS.items():
            for kw in keywords:
                pattern = r'\b' + re.escape(kw) + r'\b'
                if re.search(pattern, clause):
                    if aspect not in found_aspects:
                        found_aspects[aspect] = c_sentiment
                    break

    # If nothing matched clause-by-clause, run full text aspect search
    if not found_aspects:
        overall_pol = TextBlob(text).sentiment.polarity
        overall_s = "Positive" if overall_pol > 0.1 else ("Negative" if overall_pol < -0.1 else "Neutral")
        for aspect, keywords in ASPECT_KEYWORDS.items():
            for kw in keywords:
                pattern = r'\b' + re.escape(kw) + r'\b'
                if re.search(pattern, text_lower):
                    found_aspects[aspect] = overall_s
                    break

    if not found_aspects:
        found_aspects["Room"] = "Neutral"

    return [{"aspect": asp, "sentiment": s} for asp, s in found_aspects.items()]


def detect_aspect(text: str) -> str:
    """
    Detects the primary focus aspect.
    Prioritizes issues/complaints if present (e.g. contrast clause after 'but').
    """
    text_lower = text.lower()

    # If contrast conjunction exists, prioritize the second clause (the key complaint/praise)
    clauses = [text_lower]
    for conj in CONTRAST_CONJUNCTIONS:
        if f" {conj} " in text_lower:
            parts = text_lower.split(f" {conj} ", 1)
            clauses = [parts[1], parts[0]]
            break

    for clause in clauses:
        for aspect, keywords in ASPECT_KEYWORDS.items():
            for kw in keywords:
                pattern = r'\b' + re.escape(kw) + r'\b'
                if re.search(pattern, clause):
                    return aspect

    # Fallback to general scan
    for aspect, keywords in ASPECT_KEYWORDS.items():
        for kw in keywords:
            pattern = r'\b' + re.escape(kw) + r'\b'
            if re.search(pattern, text_lower):
                return aspect

    return "Room"


def analyze_sentiment(text: str) -> dict:
    """
    Performs sentiment analysis using TextBlob polarity combined with heuristics.
    In contrast sentences with both strong praise and specific flaw,
    computes an overall sentiment while preserving the isolated issues.
    """
    text_lower = text.lower()
    blob = TextBlob(text)
    raw_polarity = blob.sentiment.polarity

    # Count positive and negative cues in the overall review
    neg_count = sum(1 for phrase in NEGATIVE_PHRASES if phrase in text_lower)
    pos_count = sum(1 for phrase in POSITIVE_PHRASES if phrase in text_lower)

    # Check for contrast like: "The room was very clean and staff was friendly, but the Wi-Fi was slow."
    # Here 2 positive traits vs 1 negative flaw -> overall experience leans Positive with an isolated issue.
    if pos_count > neg_count and neg_count > 0:
        sentiment = "Positive"
        adjusted_polarity = 0.35
    elif neg_count > pos_count:
        sentiment = "Negative"
        adjusted_polarity = -0.5 if raw_polarity >= 0 else raw_polarity
    elif pos_count > 0 and neg_count == 0:
        sentiment = "Positive"
        adjusted_polarity = max(0.4, raw_polarity)
    elif neg_count > 0 and pos_count == 0:
        sentiment = "Negative"
        adjusted_polarity = min(-0.4, raw_polarity)
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


def get_recommendation(aspect: str, sentiment: str) -> str:
    """Returns official hotel-specific management recommendations."""
    aspect_dict = ASPECT_RECOMMENDATIONS.get(aspect, ASPECT_RECOMMENDATIONS["General"])
    return aspect_dict.get(sentiment, ASPECT_RECOMMENDATIONS["General"][sentiment])


def analyze_feedback(text: str) -> dict:
    """
    Cognitive Computing Pipeline for Babuseth Guest House & Lodging:
    1. Input Human Language
    2. Understand Text & Syntactic Clauses
    3. Sentiment Detection (Overall & Aspect-Level)
    4. Service/Aspect Detection (Hotel-Specific Categories)
    5. Issue Identification & Priority Assessment
    6. Recommendation Formulation
    7. Hotel Management Insight
    """
    overall_sentiment = analyze_sentiment(text)
    aspect_sentiments = extract_aspect_sentiments(text)
    primary_aspect = detect_aspect(text)

    # Identify any negative aspects / main issue
    negative_aspects = [item for item in aspect_sentiments if item["sentiment"] == "Negative"]
    positive_aspects = [item for item in aspect_sentiments if item["sentiment"] == "Positive"]

    if negative_aspects:
        main_issue_aspect = negative_aspects[0]["aspect"]
        main_issue = f"{main_issue_aspect} performance / condition"
        priority = "High" if len(negative_aspects) > 1 or overall_sentiment["sentiment"] == "Negative" else "Medium"
        recommendation = get_recommendation(main_issue_aspect, "Negative")
    elif overall_sentiment["sentiment"] == "Neutral":
        main_issue_aspect = primary_aspect
        main_issue = "Routine service maintenance"
        priority = "Low"
        recommendation = get_recommendation(primary_aspect, "Neutral")
    else:
        main_issue_aspect = primary_aspect
        main_issue = "None (Positive Feedback)"
        priority = "Low"
        recommendation = get_recommendation(primary_aspect, "Positive")

    aspect_summary = ', '.join([a['aspect'] + ' (' + a['sentiment'] + ')' for a in aspect_sentiments])

    return {
        "text": text,
        "sentiment": overall_sentiment["sentiment"],
        "polarity": overall_sentiment["polarity"],
        "aspect": primary_aspect,
        "aspect_sentiments": aspect_sentiments,
        "priority": priority,
        "main_issue": main_issue,
        "recommendation": recommendation,
        "pipeline_steps": [
            {"step": "1. Human Language Input", "desc": f"Received review text ({len(text)} chars)"},
            {"step": "2. Natural Language Processing", "desc": "Parsed grammatical clauses, negation qualifiers & entity phrases"},
            {"step": "3. Sentiment Detection", "desc": f"Classified overall as {overall_sentiment['sentiment']} (Polarity: {overall_sentiment['polarity']})"},
            {"step": "4. Service / Aspect Detection", "desc": f"Identified aspects: {aspect_summary}"},
            {"step": "5. Issue Identification", "desc": f"Identified core focus: {main_issue} [Priority: {priority}]"},
            {"step": "6. Recommendation Generation", "desc": recommendation},
            {"step": "7. Hotel Management Insight", "desc": "Dispatched action item to Babuseth Lodging operations team"}
        ]
    }

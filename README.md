# Smart Hotel Feedback Analyzer 🏨

A cognitive computing web application built with Python Flask, NLTK/TextBlob, and modern frontend technologies to analyze hotel guest feedback, classify sentiments, identify service aspects, and automatically generate managerial recommendations.

---

## 🌟 Features

1. **Dashboard & Analytics:**
   - Real-time KPI summary cards: Total Reviews, Positive, Negative, Neutral counts.
   - Identifies **Most Common Complaint** and **Most Liked Service**.
   - Interactive charts via **Chart.js** (Doughnut chart for Sentiment Distribution, Bar chart for Feedback by Aspect).
   
2. **Cognitive Feedback Analyzer:**
   - Real-time guest review text input box with one-click test presets.
   - Implements rule-assisted NLP handling complex contrast sentences (e.g. *"The room was clean but the AC was not working properly"* correctly recognizes **Negative** sentiment and prioritizes the **AC** aspect).
   - Generates actionable operational recommendations for hotel managers.
   - Option to automatically log and persist the newly analyzed feedback into the CSV dataset.

3. **Aspect Categorization (10 Hotel Operational Areas):**
   - **AC:** Air conditioning, cooling, heating, thermostats
   - **WiFi:** Connectivity, speed, wireless coverage
   - **Cleanliness:** Hygiene, housekeeping, bathrooms, linens
   - **Staff:** Front desk courtesy, hospitality, concierge
   - **Food:** Breakfast buffet, restaurant dining, taste
   - **Room:** Space, bed comfort, amenities, views
   - **Service:** Room service turnaround, check-in, check-out
   - **Price:** Value-for-money, affordability, billing transparency
   - **Location:** Proximity to city center, transportation, surroundings
   - **Facilities:** Elevators, swimming pools, fitness gyms, parking

4. **Sentiment Classification:**
   - Classifies text into **Positive**, **Negative**, or **Neutral** using transparent TextBlob polarity and contextual heuristics without external paid APIs.

5. **Reviews Database & Filters:**
   - Responsive reviews data table.
   - Quick filters: **All**, **Positive**, **Negative**, **Neutral**.
   - Live search filter by keyword or service category.

6. **Operational Insights:**
   - Automated insights highlighting operational health (e.g., cleanliness satisfaction, recurring complaint bottlenecks, and sentiment trends).

7. **Clean Hotel Dashboard UI:**
   - Designed with clean white background, ocean blue / teal accents, cards, responsive sidebar, and clear visual hierarchy.

---

## 🧠 Cognitive Computing Pipeline

The system directly implements the 5 core stages of cognitive computing:

```
[1. Input Human Language]
         │ (Guest review text)
         ▼
[2. Understand Text]
         │ (Parse syntax, negation clauses & conjunctions)
         ▼
[3. Detect Sentiment]
         │ (Positive / Negative / Neutral)
         ▼
[4. Identify Hotel Service]
         │ (AC, WiFi, Cleanliness, Staff, Food, etc.)
         ▼
[5. Generate Recommendation]
           (Contextual managerial action plan)
```

---

## 🛠️ Technology Stack

- **Frontend:** HTML5, CSS3 (Modern Flexbox & Grid), JavaScript (Vanilla ES6), Font Awesome icons
- **Data Visualizations:** Chart.js
- **Backend:** Python 3 (Flask framework)
- **Natural Language Processing (NLP):** TextBlob + NLTK
- **Storage / Dataset:** CSV (`data/hotel_reviews.csv` with 50 realistic guest reviews)

---

## 📁 Project Structure

```
smart-hotel-feedback-analyzer/
├── app.py                     # Flask application server & REST APIs
├── nlp_analyzer.py            # Cognitive NLP engine (aspect detection, sentiment, suggestions)
├── test_analyzer.py           # Automated unit test suite
├── requirements.txt           # Python package dependencies
├── README.md                  # Project documentation & execution guide
├── data/
│   └── hotel_reviews.csv      # 50 sample hotel reviews
├── templates/
│   └── index.html             # Single-Page Application (SPA) dashboard
└── static/
    ├── css/
    │   └── style.css          # Professional hotel UI stylesheet
    └── js/
        └── app.js             # Interactive client-side logic & Chart.js rendering
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+ installed on your computer.

### Step 1: Open Terminal and Navigate to Project Directory
```bash
cd "C:\Users\Ishan\.gemini\antigravity\scratch\smart-hotel-feedback-analyzer"
```

### Step 2: Install Required Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the Application
```bash
python app.py
```

### Step 4: Access the Web App
Open your web browser and go to:
```
http://127.0.0.1:5000/
```

---

## 🧪 Verification & Example Runs

The test suite can be run at any time:
```bash
python test_analyzer.py
```

### Example Test Inputs & Outputs:

1. **Input:** `"The room was clean but the AC was not working properly."`
   - **Sentiment:** `Negative`
   - **Aspect:** `AC`
   - **Suggestion:** *"Check and maintain the room AC and HVAC units regularly to ensure proper cooling and heating."*

2. **Input:** `"Exceptional hospitality! The front desk staff welcomed us warmly and helped with our luggage."`
   - **Sentiment:** `Positive`
   - **Aspect:** `Staff`
   - **Suggestion:** *"Commend the front-desk and support staff for their welcoming and courteous hospitality."*

3. **Input:** `"The complimentary breakfast buffet had delicious fresh fruit, pastries, and great coffee."`
   - **Sentiment:** `Positive`
   - **Aspect:** `Food`
   - **Suggestion:** *"Continue offering high-quality, varied, and fresh breakfast and dining menus."*

4. **Input:** `"Wi-Fi kept disconnecting during my remote work meetings, very frustrating."`
   - **Sentiment:** `Negative`
   - **Aspect:** `WiFi`
   - **Suggestion:** *"Upgrade internet bandwidth, replace aging routers, and enhance Wi-Fi coverage across all guest floors."*

5. **Input:** `"The room was fairly standard with basic furnishings and adequate lighting."`
   - **Sentiment:** `Neutral`
   - **Aspect:** `Room`
   - **Suggestion:** *"Ensure all room amenities, lighting, and toiletries are stocked and functioning properly."*

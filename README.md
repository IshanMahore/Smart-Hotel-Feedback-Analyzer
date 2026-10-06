# Babuseth Guest House & Lodging 🏨
### Guest Feedback & Service Quality Analyzer

A Cognitive Computing web application customized specifically for **Babuseth Guest House & Lodging**, located at **Railway Station, Chhatrapati Sambhajinagar, Maharashtra**. The system analyzes guest feedback using Natural Language Processing (NLP) to detect multi-aspect sentiments, identify service issues, and automatically generate managerial recommendations.

---

## 🏢 Hotel Profile & Contact Details

- **Property Name:** Babuseth Guest House & Lodging
- **Location:** Railway Station, Chhatrapati Sambhajinagar, Maharashtra
- **Phone:** 7821077435
- **Email:** babusethguesthouse@gmail.com
- **Official Branding:** Navy Blue (`#0b1b3d`), Orange (`#ea580c`), White, and Light Gray (`#f8fafc`).
- **Official Logo:** Included in SVG format at `static/images/babuseth_logo.svg` (rendered seamlessly in sidebar, header, and about section).

---

## 🛏️ Hotel Services & Accommodations

### Room Types:
1. **Family Room:** Comfortable accommodation for families with spacious bedding.
2. **Deluxe Room:** Comfortable room suitable for a relaxing stay.
3. **Super Deluxe Room:** Premium room option for guests seeking additional comfort and quietness.

### Hotel Amenities & Offerings:
- **AC Rooms:** Air-conditioned rooms for optimal climate control.
- **Free Wi-Fi:** High-speed internet access for guests.
- **Free Parking:** Dedicated, secure on-premises parking.
- **Complimentary Breakfast:** Fresh morning breakfast and hot tea.
- **24 Hours Service:** Round-the-clock check-in and room assistance.
- **Friendly Staff:** Courteous and helpful caretaker hospitality.
- *(Note: No dedicated restaurant is present).*

---

## 🧠 Cognitive Computing Architecture

The system demonstrates the cognitive intelligence workflow transforming human language into managerial decisions:

```
           [ Guest Feedback ]
                   ↓
     [ Natural Language Processing ]
                   ↓
          [ Sentiment Detection ]
                   ↓
      [ Service/Aspect Detection ]
                   ↓
        [ Issue Identification ]
                   ↓
            [ Recommendation ]
                   ↓
      [ Hotel Management Insight ]
```

### Cognitive Processing Principles:
1. **Perception & Natural Language Understanding:** Decomposes complex feedback containing multiple clauses, negation qualifiers, and contrast conjunctions (`but`, `however`, `although`).
2. **Fine-Grained Aspect Sentiment Mapping:** Simultaneously captures positive traits and isolated grievances.
   * *Example:* `"The room was very clean and the staff was friendly, but the Wi-Fi was slow."*
   * **Overall Sentiment:** `Positive`
   * **Detected Aspects:** Cleanliness → Positive, Staff → Positive, Wi-Fi → Negative
   * **Priority:** `Medium`
   * **Main Issue:** `Wi-Fi performance`
   * **Recommendation:** *"Improve Wi-Fi coverage and connection speed for guests."*
3. **Action-Oriented Decision Support:** Prescribes targeted operational adjustments rather than static statistics.

---

## 📊 Dashboard & System Features

1. **Dashboard KPI Summary Cards:**
   - Total Reviews (30 verified stays)
   - Positive Reviews
   - Negative Reviews
   - Neutral Reviews
   - Average Rating (e.g. 4.0 ★)
   - Most Praised Service
   - Most Complained Service

2. **3 Chart.js Visualizations:**
   - **Guest Sentiment Distribution:** Doughnut chart (Positive, Neutral, Negative).
   - **Service Feedback Breakdown:** Bar chart (Room, Cleanliness, Staff, AC, Wi-Fi, Parking, Breakfast, Service).
   - **Positive vs. Negative Feedback:** Grouped bar chart comparing satisfaction by department.

3. **Interactive Feedback Analyzer:**
   - One-click testing chips for real hotel scenarios.
   - Live extraction of aspects, sentiments, priority levels, and recommendations.
   - Option to persist analyzed reviews directly into the guest database.

4. **Dedicated Hotel Services Page:**
   - Clean, professional cards showcasing Family Rooms, Deluxe Rooms, Super Deluxe Rooms, AC Rooms, Free Wi-Fi, Free Parking, Complimentary Breakfast, 24 Hours Service, and Friendly Staff.

5. **Guest Reviews Database:**
   - Filter by All, Positive, Negative, or Neutral.
   - Real-time search across guest reviews and service tags.

6. **Actionable Insights:**
   - Highlights staff courtesy, room cleanliness standards, Wi-Fi optimization alerts, and the strategic railway station location advantage.

---

## 🛠️ Technology Stack

- **Backend:** Python 3 + Flask framework
- **NLP Engine:** TextBlob + rule-assisted syntax heuristics
- **Data Persistence:** CSV (`data/hotel_reviews.csv` with 30 realistic guest feedback entries)
- **Frontend:** Responsive HTML5, CSS3 (Navy Blue & Orange hotel palette), Vanilla JavaScript ES6
- **Visualizations:** Chart.js
- **Icons:** Font Awesome 6

---

## 🚀 How to Run the Application

### 1. Open Terminal and Navigate to the Directory:
```powershell
cd "C:\Users\Ishan\.gemini\antigravity\scratch\smart-hotel-feedback-analyzer"
```

### 2. Install Dependencies (if not already installed):
```powershell
pip install -r requirements.txt
```

### 3. Start the Flask Server:
```powershell
python app.py
```

### 4. Access the Website:
Open your browser and navigate to:
```
http://127.0.0.1:5000/
```

---

## 🧪 Automated Testing

Run the automated test suite verifying all hotel aspects, sentiment detection, and recommendation rules:
```powershell
python test_analyzer.py
```
*(All 9 unit tests pass in < 0.3s).*

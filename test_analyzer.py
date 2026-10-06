import unittest
from nlp_analyzer import analyze_feedback, detect_aspect, analyze_sentiment, extract_aspect_sentiments

class TestBabusethHotelAnalyzer(unittest.TestCase):

    def test_example_prompt_clean_staff_wifi(self):
        # Specific user requirement:
        # "The room was very clean and the staff was friendly, but the Wi-Fi was slow."
        # Overall Sentiment: Positive
        # Detected Aspects: Cleanliness -> Positive, Staff -> Positive, Wi-Fi -> Negative
        # Priority: Medium
        # Main Issue: Wi-Fi performance
        # Recommendation: "Improve Wi-Fi coverage and connection speed for guests."
        text = "The room was very clean and the staff was friendly, but the Wi-Fi was slow."
        res = analyze_feedback(text)
        self.assertEqual(res["sentiment"], "Positive")
        
        aspect_dict = {a["aspect"]: a["sentiment"] for a in res["aspect_sentiments"]}
        self.assertEqual(aspect_dict.get("Cleanliness"), "Positive")
        self.assertEqual(aspect_dict.get("Staff"), "Positive")
        self.assertEqual(aspect_dict.get("Wi-Fi"), "Negative")
        
        self.assertEqual(res["priority"], "Medium")
        self.assertIn("Wi-Fi", res["main_issue"])
        self.assertIn("Wi-Fi", res["recommendation"])

    def test_negative_ac_feedback(self):
        # Negative AC feedback -> Inspect the AC unit and ensure comfortable room temperature.
        text = "AC in our room was not working properly and it was hot."
        res = analyze_feedback(text)
        self.assertEqual(res["sentiment"], "Negative")
        self.assertEqual(res["aspect"], "AC")
        self.assertIn("AC unit", res["recommendation"])

    def test_negative_cleanliness_feedback(self):
        # Negative cleanliness -> Review room cleaning procedures and inspection frequency.
        text = "The bathroom was dirty and towels were not clean."
        res = analyze_feedback(text)
        self.assertEqual(res["sentiment"], "Negative")
        self.assertIn("cleaning procedures", res["recommendation"])

    def test_negative_staff_feedback(self):
        # Negative staff -> Review guest-service processes and staff response time.
        text = "Staff was rude and delayed our check-in by 40 minutes."
        res = analyze_feedback(text)
        self.assertEqual(res["sentiment"], "Negative")
        self.assertIn("guest-service processes", res["recommendation"])

    def test_negative_breakfast_feedback(self):
        # Negative breakfast -> Review complimentary breakfast quality and guest preferences.
        text = "Breakfast was cold, delayed, and tasteless."
        res = analyze_feedback(text)
        self.assertEqual(res["sentiment"], "Negative")
        self.assertIn("breakfast", res["recommendation"].lower())

    def test_negative_parking_feedback(self):
        # Negative parking -> Improve parking availability and clearly communicate parking arrangements.
        text = "Parking was full, congested and difficult to find space."
        res = analyze_feedback(text)
        self.assertEqual(res["sentiment"], "Negative")
        self.assertIn("parking", res["recommendation"].lower())

    def test_positive_staff_feedback(self):
        # Positive staff -> Continue maintaining the friendly and responsive service.
        text = "Staff was very friendly, helpful, and courteous."
        res = analyze_feedback(text)
        self.assertEqual(res["sentiment"], "Positive")
        self.assertIn("friendly and responsive", res["recommendation"])

    def test_positive_cleanliness_feedback(self):
        # Positive cleanliness -> Maintain the current room-cleaning standards.
        text = "The room cleanliness was spotless and very neat."
        res = analyze_feedback(text)
        self.assertEqual(res["sentiment"], "Positive")
        self.assertIn("cleaning standards", res["recommendation"])

    def test_hotel_room_aspects_detection(self):
        # Family Room, Deluxe Room, Super Deluxe Room
        res_family = analyze_feedback("Our Family Room was spacious and comfortable for all 4 of us.")
        self.assertIn("Family Room", [a["aspect"] for a in res_family["aspect_sentiments"]])

        res_deluxe = analyze_feedback("The Deluxe Room was cozy with comfortable mattress.")
        self.assertIn("Deluxe Room", [a["aspect"] for a in res_deluxe["aspect_sentiments"]])

        res_super = analyze_feedback("Super Deluxe Room offered luxury bedding and peace.")
        self.assertIn("Super Deluxe Room", [a["aspect"] for a in res_super["aspect_sentiments"]])

        res_station = analyze_feedback("The hotel is right next to the Railway Station in Sambhajinagar.")
        self.assertIn("Railway Station", [a["aspect"] for a in res_station["aspect_sentiments"]])


if __name__ == '__main__':
    unittest.main()

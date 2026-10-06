import unittest
from nlp_analyzer import analyze_feedback, detect_aspect, analyze_sentiment

class TestSmartHotelFeedbackAnalyzer(unittest.TestCase):

    def test_sample_1_user_request_ac_negative(self):
        # Specific user requirement:
        # "The room was clean but the AC was not working properly." -> Negative, AC, "Check and maintain..."
        res = analyze_feedback("The room was clean but the AC was not working properly.")
        self.assertEqual(res["sentiment"], "Negative")
        self.assertEqual(res["aspect"], "AC")
        self.assertIn("AC", res["suggestion"])

    def test_sample_2_staff_positive(self):
        res = analyze_feedback("Exceptional hospitality! The front desk staff welcomed us warmly and helped with luggage.")
        self.assertEqual(res["sentiment"], "Positive")
        self.assertEqual(res["aspect"], "Staff")
        self.assertIn("staff", res["suggestion"].lower())

    def test_sample_3_food_positive(self):
        res = analyze_feedback("The complimentary breakfast buffet had delicious fresh fruit, pastries, and great coffee.")
        self.assertEqual(res["sentiment"], "Positive")
        self.assertEqual(res["aspect"], "Food")

    def test_sample_4_wifi_negative(self):
        res = analyze_feedback("Wi-Fi kept disconnecting during my remote work meetings, very frustrating.")
        self.assertEqual(res["sentiment"], "Negative")
        self.assertEqual(res["aspect"], "WiFi")
        self.assertIn("Wi-Fi", res["suggestion"])

    def test_sample_5_room_neutral(self):
        res = analyze_feedback("The room was fairly standard with basic furnishings and adequate lighting.")
        self.assertEqual(res["sentiment"], "Neutral")
        self.assertEqual(res["aspect"], "Room")

    def test_sample_6_cleanliness_negative(self):
        res = analyze_feedback("The bathroom floor was dirty and the shower drain was clogged when we checked in.")
        self.assertEqual(res["sentiment"], "Negative")
        self.assertEqual(res["aspect"], "Cleanliness")
        self.assertIn("housekeeping", res["suggestion"].lower())

    def test_sample_7_facilities_price_aspects(self):
        res_fac = analyze_feedback("The rooftop swimming pool was pristine and our kids thoroughly enjoyed the pool.")
        self.assertEqual(res_fac["aspect"], "Facilities")
        self.assertEqual(res_fac["sentiment"], "Positive")

        res_price = analyze_feedback("Way overpriced for the subpar amenities provided. Not good value for money.")
        self.assertEqual(res_price["aspect"], "Price")
        self.assertEqual(res_price["sentiment"], "Negative")


if __name__ == '__main__':
    unittest.main()

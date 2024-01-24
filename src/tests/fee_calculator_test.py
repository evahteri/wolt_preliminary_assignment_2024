import unittest
from fastapi.testclient import TestClient
from main import app

class TestFeeCalculator(unittest.TestCase):
    def setUp(self):
        self.delivery = {"cart_value": 790, "delivery_distance": 2235, "number_of_items": 4, "time": "2024-01-15T13:00:00Z"}
        self.client = TestClient(app)

    def test_example_delivery(self):
        example_delivery = {"cart_value": 790, "delivery_distance": 2235, "number_of_items": 4, "time": "2024-01-15T13:00:00Z"}
        response = self.client.post("/", json=example_delivery)
        self.assertEqual (response.status_code, 200)
        self.assertEqual (response.json(), {"delivery_fee": 710})
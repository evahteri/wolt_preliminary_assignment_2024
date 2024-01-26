import unittest
from fastapi.testclient import TestClient
from main import app


class TestFeeCalculator(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_example_delivery(self):
        """Example delivery from the assignment, delivery fee should be 7.10€
        """
        example_delivery = {"cart_value": 790, "delivery_distance": 2235,
                            "number_of_items": 4, "time": "2024-01-15T13:00:00Z"}
        response = self.client.post("/", json=example_delivery)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"delivery_fee": 710})

    def test_friday_rush(self):
        """Friday rush fee should be applied when order is placed during it
        """
        example_delivery = {"cart_value": 790, "delivery_distance": 2235,
                            "number_of_items": 4, "time": "2024-01-26T15:30:00Z"}
        response = self.client.post("/", json=example_delivery)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"delivery_fee": 852})

    def test_no_friday_rush_after_end(self):
        """No rush fee after the rush time ends
        """
        example_delivery = {"cart_value": 790, "delivery_distance": 2235,
                            "number_of_items": 4, "time": "2024-01-26T19:00:01Z"}
        response = self.client.post("/", json=example_delivery)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"delivery_fee": 710})

    def test_get_request(self):
        """GET request should not be allowed
        """
        response = self.client.get("/")
        self.assertEqual(response.status_code, 405)

    def test_put_request(self):
        """PUT request should not be allowed
        """
        response = self.client.put("/")
        self.assertEqual(response.status_code, 405)

    def test_free_delivery(self):
        """If cart value is 200€ or over, delivery is free
        """
        example_delivery = {"cart_value": 20000, "delivery_distance": 2235,
                            "number_of_items": 4, "time": "2024-01-26T15:30:00Z"}
        response = self.client.post("/", json=example_delivery)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"delivery_fee": 0})

    def test_max_delivery_fee(self):
        """Delivery fee should not pass 15€
        """
        example_delivery = {"cart_value": 790, "delivery_distance": 50000,
                            "number_of_items": 9, "time": "2024-01-26T15:30:00Z"}
        response = self.client.post("/", json=example_delivery)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"delivery_fee": 1500})

    def test_minimum_fee(self):
        """Delivery fee should never be under 1€
        """
        example_delivery = {"cart_value": 1000, "delivery_distance": 3,
                            "number_of_items": 4, "time": "2024-01-15T15:30:00Z"}
        response = self.client.post("/", json=example_delivery)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"delivery_fee": 100})

    def test_additional_delivery_distance_fee_1499_meters(self):
        """If delivery fee is 1499, delivery fee is 3€
        """
        example_delivery = {"cart_value": 1000, "delivery_distance": 1499,
                            "number_of_items": 4, "time": "2024-01-15T15:30:00Z"}
        response = self.client.post("/", json=example_delivery)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"delivery_fee": 300})

    def test_additional_delivery_distance_fee_1500_meters(self):
        """If delivery distance is 1500, delivery fee is 3€
        """
        example_delivery = {"cart_value": 1000, "delivery_distance": 1500,
                            "number_of_items": 4, "time": "2024-01-15T15:30:00Z"}
        response = self.client.post("/", json=example_delivery)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"delivery_fee": 300})

    def test_additional_delivery_distance_fee_1501_meters(self):
        """If delivery distance is 1501 meters, delivery fee is 4€
        """
        example_delivery = {"cart_value": 1000, "delivery_distance": 1501,
                            "number_of_items": 4, "time": "2024-01-15T15:30:00Z"}
        response = self.client.post("/", json=example_delivery)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"delivery_fee": 400})

    def test_additional_item_fee_4_items(self):
        """If there are only 4 items, no extra fee
        """
        example_delivery = {"cart_value": 1000, "delivery_distance": 200,
                            "number_of_items": 4, "time": "2024-01-15T15:30:00Z"}
        response = self.client.post("/", json=example_delivery)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"delivery_fee": 100})

    def test_additional_item_fee_5_items(self):
        """If there are 5 items, 50cent extra fee
        """
        example_delivery = {"cart_value": 1000, "delivery_distance": 200,
                            "number_of_items": 5, "time": "2024-01-15T15:30:00Z"}
        response = self.client.post("/", json=example_delivery)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"delivery_fee": 150})

    def test_additional_item_fee_13_items(self):
        """If there are 13 items, 5.70€ extra fee
        """
        example_delivery = {"cart_value": 1000, "delivery_distance": 200,
                            "number_of_items": 13, "time": "2024-01-15T15:30:00Z"}
        response = self.client.post("/", json=example_delivery)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"delivery_fee": 670})

    def test_additional_item_fee_14_items(self):
        """If there are 13 items, 6.20€ extra fee
        """
        example_delivery = {"cart_value": 1000, "delivery_distance": 200,
                            "number_of_items": 14, "time": "2024-01-15T15:30:00Z"}
        response = self.client.post("/", json=example_delivery)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"delivery_fee": 720})

    def test_non_valid_data(self):
        """Even when the JSON values are not the right type, the API works
        """
        example_delivery = {"cart_value": "790", "delivery_distance": "2235",
                            "number_of_items": "4", "time": "2024-01-15T13:00:00Z"}
        response = self.client.post("/", json=example_delivery)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"delivery_fee": 710})

    def test_non_valid_data(self):
        """When non-valid data is entered and it cannot be processed, API should return 422 error
        """
        example_delivery = {"cart_value": "value", "delivery_distance": 2235,
                            "number_of_items": 4, "time": "2024-01-15T13:00:00Z"}
        response = self.client.post("/", json=example_delivery)
        self.assertEqual(response.status_code, 422)

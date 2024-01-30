import unittest
from settings import settings
from fastapi.testclient import TestClient
from main import app


class TestApi(unittest.TestCase):
    def setUp(self):
        settings.ENVIRONMENT = 'test'
        self.client = TestClient(app)

    def test_example_delivery(self):
        """Example delivery from the assignment, delivery fee should be 7.10€.
        """
        example_delivery = {"cart_value": 790, "delivery_distance": 2235,
                            "number_of_items": 4, "time": "2024-01-15T13:00:00Z"}
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

    def test_non_valid_data(self):
        """Even when the JSON values are not the right type, the API works
        """
        example_delivery = {"cart_value": "790", "delivery_distance": "2235",
                            "number_of_items": "4", "time": "2024-01-15T13:00:00Z"}
        response = self.client.post("/", json=example_delivery)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"delivery_fee": 710})

    def test_non_valid_data_error(self):
        """When non-valid data is entered and it cannot be processed, API should return 422 error
        """
        example_delivery = {"cart_value": "value", "delivery_distance": 2235,
                            "number_of_items": 4, "time": "2024-01-15T13:00:00Z"}
        response = self.client.post("/", json=example_delivery)
        self.assertEqual(response.status_code, 422)

import unittest
from settings import settings
from fastapi.testclient import TestClient
from main import app


class TestApi(unittest.TestCase):
    def setUp(self):
        settings.ENVIRONMENT = 'test'
        self.client = TestClient(app)

    def test_example_delivery(self):
        """Example delivery from the assignment, response should be in json format 
        including a delivery fee of 7.10€,
        and the status code should be 200.
        """
        example_delivery = {"cart_value": 790, "delivery_distance": 2235,
                            "number_of_items": 4, "time": "2024-01-15T13:00:00Z"}
        response = self.client.post("/", json=example_delivery)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"delivery_fee": 710})

class TestApiRequests(unittest.TestCase):
    def setUp(self):
        settings.ENVIRONMENT = 'test'
        self.client = TestClient(app)

    def test_get_request(self):
        """GET request should not be allowed and the response status code should be 405.
        """
        response = self.client.get("/")
        self.assertEqual(response.status_code, 405)

    def test_put_request(self):
        """PUT request should not be allowed and the response status code should be 405.
        """
        response = self.client.put("/")
        self.assertEqual(response.status_code, 405)
    
    def test_head_request(self):
        """HEAD request should not be allowed and the response status code should be 405.
        """
        response = self.client.head("/")
        self.assertEqual(response.status_code, 405)

    def test_delete_request(self):
        """DELETE request should not be allowed and the response status code should be 405.
        """
        response = self.client.delete("/")
        self.assertEqual(response.status_code, 405)

    def test_options_request(self):
        """OPTIONS request should not be allowed and the response status code should be 405.
        """
        response = self.client.options("/")
        self.assertEqual(response.status_code, 405)

    def test_patch_request(self):
        """PATCH request should not be allowed and the response status code should be 405.
        """
        response = self.client.patch("/")
        self.assertEqual(response.status_code, 405)

class TestApiCartValueValidation(unittest.TestCase):
    def setUp(self):
        settings.ENVIRONMENT = 'test'
        self.client = TestClient(app)

    def test_non_valid_data_error_cart_value_str(self):
        """When non-valid data is entered and it cannot be processed, 
        API should return 400 error with a relevant error message.
        """
        example_delivery = {"cart_value": "value", "delivery_distance": 2235,
                            "number_of_items": 4, "time": "2024-01-15T13:00:00Z"}
        response = self.client.post("/", json=example_delivery)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), "Cart value must be a positive integer.")

class TestApiNumberOfItemsValidation(unittest.TestCase):
    def setUp(self):
        settings.ENVIRONMENT = 'test'
        self.client = TestClient(app)

    def test_non_valid_data_error_number_of_items_str(self):
        """When non-valid data is entered and it cannot be processed, 
        API should return 400 error with a relevant error message.
        """
        example_delivery = {"cart_value": 500, "delivery_distance": 2235,
                            "number_of_items": "4", "time": "2024-01-15T13:00:00Z"}
        response = self.client.post("/", json=example_delivery)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), "Number of items must be an integer with a value over 1.")

    def test_non_valid_data_error_number_of_items_zero(self):
        """When non-valid data is entered and it cannot be processed, 
        API should return 400 error with a relevant error message.
        """
        example_delivery = {"cart_value": 500, "delivery_distance": 2235,
                            "number_of_items": 0, "time": "2024-01-15T13:00:00Z"}
        response = self.client.post("/", json=example_delivery)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), "Number of items must be an integer with a value over 1.")

    def test_non_valid_data_error_number_of_items_negative(self):
        """When non-valid data is entered and it cannot be processed, 
        API should return 400 error with a relevant error message.
        """
        example_delivery = {"cart_value": 500, "delivery_distance": 2235,
                            "number_of_items": -20, "time": "2024-01-15T13:00:00Z"}
        response = self.client.post("/", json=example_delivery)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), "Number of items must be an integer with a value over 1.")

class TestApiTimeValidation(unittest.TestCase):
    def setUp(self):
        settings.ENVIRONMENT = 'test'
        self.client = TestClient(app)

    def test_non_valid_data_error_time_not_string(self):
        """When non-valid data is entered and it cannot be processed, 
        API should return 400 error with a relevant error message.
        """
        example_delivery = {"cart_value": 500, "delivery_distance": 2235,
                            "number_of_items": 10, "time": 20240115130000}
        response = self.client.post("/", json=example_delivery)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), "Time must be string type in UTC, ISO 8601 format.")

    def test_non_valid_data_error_time_month_does_not_exist(self):
        """When non-valid data is entered and it cannot be processed, 
        API should return 400 error with a relevant error message.
        """
        example_delivery = {"cart_value": 500, "delivery_distance": 2235,
                            "number_of_items": 10, "time": "2024-13-15T13:00:00Z"}
        response = self.client.post("/", json=example_delivery)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), "Time must be string type in UTC, ISO 8601 format.")

    def test_non_valid_data_error_time_date_does_not_exist(self):
        """When non-valid data is entered and it cannot be processed, 
        API should return 400 error with a relevant error message.
        """
        example_delivery = {"cart_value": 500, "delivery_distance": 2235,
                            "number_of_items": 10, "time": "2024-02-30T13:00:00Z"}
        response = self.client.post("/", json=example_delivery)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), "Time must be string type in UTC, ISO 8601 format.")

    def test_non_valid_data_error_time_hour_does_not_exist(self):
        """When non-valid data is entered and it cannot be processed, 
        API should return 400 error with a relevant error message.
        """
        example_delivery = {"cart_value": 500, "delivery_distance": 2235,
                            "number_of_items": 10, "time": "2024-02-30T25:00:00Z"}
        response = self.client.post("/", json=example_delivery)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), "Time must be string type in UTC, ISO 8601 format.")

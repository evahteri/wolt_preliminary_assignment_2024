import unittest
from services.request_validator import DeliveryRequestValidator


class TestDeliveryRquestValidator(unittest.TestCase):

    def setUp(self):
        """Testing all the methods in the DeliveryRequestValidator class.
        """
        self.delivery_request_validator = DeliveryRequestValidator()

    def test_valid_cart_value_not_int(self):
        self.assertEqual(self.delivery_request_validator.valid_cart_value(cart_value="13"), False)

    def test_valid_cart_value_negative(self):
        self.assertEqual(self.delivery_request_validator.valid_cart_value(cart_value=-1), False)

    def test_valid_cart_value_positive(self):
        self.assertEqual(self.delivery_request_validator.valid_cart_value(cart_value=1), True)

    def test_valid_cart_value_zero(self):
        self.assertEqual(self.delivery_request_validator.valid_cart_value(cart_value=0), True)

    def test_valid_delivery_distance_not_int(self):
        self.assertEqual(self.delivery_request_validator.valid_delivery_distance(delivery_distance="long"), False)

    def test_valid_delivery_distance_negative(self):
        self.assertEqual(self.delivery_request_validator.valid_delivery_distance(delivery_distance=-1), False)

    def test_valid_delivery_distance_positive(self):
        self.assertEqual(self.delivery_request_validator.valid_delivery_distance(delivery_distance=1), True)

    def test_valid_delivery_distance_zero(self):
        self.assertEqual(self.delivery_request_validator.valid_delivery_distance(delivery_distance=0), True)

    def test_valid_number_of_items_not_int(self):
        self.assertEqual(self.delivery_request_validator.valid_number_of_items(number_of_items="a lot"), False)

    def test_valid_number_of_items_negative(self):
        self.assertEqual(self.delivery_request_validator.valid_number_of_items(number_of_items=-1), False)

    def test_valid_number_of_items_positive(self):
        self.assertEqual(self.delivery_request_validator.valid_number_of_items(number_of_items=1), True)

    def test_valid_number_of_items_zero(self):
        self.assertEqual(self.delivery_request_validator.valid_number_of_items(number_of_items=0), False)

    def test_valid_time_not_str(self):
        self.assertEqual(self.delivery_request_validator.valid_time(time=1), False)

    def test_valid_time_not_iso_format(self):
        self.assertEqual(self.delivery_request_validator.valid_time(time="2024-01-01 12:00:00"), False)

    def test_valid_time_iso_format_not_valid_time(self):
        self.assertEqual(self.delivery_request_validator.valid_time(time="2024-01-01T25:00:00Z"), False)

    def test_valid_delivery_request_valid(self):
        self.assertEqual(self.delivery_request_validator.valid_delivery_request(
            delivery_request={"cart_value": 1, "delivery_distance": 1, "number_of_items": 1, "time": "2024-01-01T12:00:00Z"}),
            "valid")

    def test_valid_delivery_request_neg_cart_value(self):
        self.assertEqual(self.delivery_request_validator.valid_delivery_request(
            delivery_request={"cart_value": -1, "delivery_distance": 1, "number_of_items": 1, "time": "2024-01-01T12:00:00Z"}),
            "Cart value must be a positive integer.")

    def test_valid_delivery_request_neg_delivery_distance(self):
        self.assertEqual(self.delivery_request_validator.valid_delivery_request(
            delivery_request={"cart_value": 1, "delivery_distance": -1, "number_of_items": 1, "time": "2024-01-01T12:00:00Z"}),
            "Delivery distance must be a positive integer.")

    def test_valid_delivery_request_zero_number_of_items(self):
        self.assertEqual(self.delivery_request_validator.valid_delivery_request(
            delivery_request={"cart_value": 1, "delivery_distance": 1, "number_of_items": 0, "time": "2024-01-01T12:00:00Z"}),
            "Number of items must be an integer with a value over 1.")

    def test_valid_delivery_request_time_not_iso_format(self):
        self.assertEqual(self.delivery_request_validator.valid_delivery_request(
            delivery_request={"cart_value": 1, "delivery_distance": 1, "number_of_items": 1, "time": "2024-01-01 12:00:00"}),
            "Time must be string type in UTC, ISO 8601 format.")

import unittest
from datetime import datetime
from models.delivery import Delivery
from services.fee_calculator import FeeCalculator

class TestFeeCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = FeeCalculator()

    def test_calculate_fee(self):
        """Test the function with example delivery from the assignment. Fee should be 7.10€
        """
        delivery = Delivery(cart_value=790, delivery_distance=2235, number_of_items=4, time="2024-01-15T13:00:00Z")
        fee = self.calculator.calculate_fee(delivery)
        self.assertEqual(fee, 710)

    def test_minimum_cart_value(self):
        # TODO
        pass


    def test_delivery_distance_fee(self):
        # TODO
        pass


    def test_number_of_items_fee(self):
        # TODO
        pass


    def test_rush_hour_fee(self):
        # TODO
        pass



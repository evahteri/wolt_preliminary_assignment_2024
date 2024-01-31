import unittest
from datetime import time
from settings import settings
from models.delivery import Delivery
from services.fee_calculator import FeeCalculator
from config import RushHours


class TestFeeCalculatorTotalDeliveryFee(unittest.TestCase):

    def setUp(self):
        """The tests use test_config.py configuration,
        so that changing the prod/dev config does not break the tests.
        """
        settings.ENVIRONMENT = 'test'
        self.calculator = FeeCalculator()

    def test_calculate_fee_valid_order(self):
        """Test the function with a valid delivery. Fee should be 7.10€
        """
        delivery = Delivery(cart_value=790, delivery_distance=2235, number_of_items=4, time="2024-01-15T13:00:00Z")
        fee = self.calculator.calculate_total_delivery_fee(delivery)
        self.assertEqual(fee, 710)

    def test_calculate_total_delivery_fee_minimum_total_fee(self):
        """Test the total fee function with a delivery that is under the minimum total fee,
        to test that it is never under that.
        """
        delivery = Delivery(cart_value=1000, delivery_distance=50, number_of_items=1, time="2024-01-15T13:00:00Z")
        total_fee = self.calculator.calculate_total_delivery_fee(delivery)
        self.assertEqual(total_fee, 100)

    def test_calculate_total_fee_max_total_fee(self):
        """Test the total fee function with a delivery that is over the maximum total fee,
        to test that it is never over that.
        """
        delivery = Delivery(cart_value=1000, delivery_distance=50000, number_of_items=100, time="2024-01-15T13:00:00Z")
        total_fee = self.calculator.calculate_total_delivery_fee(delivery)
        self.assertEqual(total_fee, 1500)

    def test_calculate_total_fee_free_delivery_edge_over(self):
        """Test the total fee function with a delivery that is over the minimum cart value for free delivery,
        to test that the fee is 0.
        """
        delivery = Delivery(cart_value=20001, delivery_distance=1490, number_of_items=25, time="2024-01-15T13:00:00Z")
        total_fee = self.calculator.calculate_total_delivery_fee(delivery)
        self.assertEqual(total_fee, 0)

    def test_calculate_total_fee_free_delivery_edge_equal(self):
        """Test the total fee function with a delivery that is equal to the minimum cart value for free delivery,
        to test that the fee is 0.
        """
        delivery = Delivery(cart_value=20000, delivery_distance=1490, number_of_items=25, time="2024-01-15T13:00:00Z")
        total_fee = self.calculator.calculate_total_delivery_fee(delivery)
        self.assertEqual(total_fee, 0)

    def test_calculate_total_fee_free_delivery_edge_under(self):
        """Test the total fee function with a delivery that is equal to the minimum cart value for free delivery,
        to test that the fee is 0.
        """
        delivery = Delivery(cart_value=19999, delivery_distance=3200, number_of_items=25, time="2024-01-15T13:00:00Z")
        total_fee = self.calculator.calculate_total_delivery_fee(delivery)
        self.assertEqual(total_fee, 1500)


class TestFeeCalculatorCartValueSurcharge(unittest.TestCase):

    def setUp(self):
        settings.ENVIRONMENT = 'test'
        self.calculator = FeeCalculator()

    def test_minimum_cart_value_surcharge_is_right(self):
        """Test minimum cart value function. If the cart value is 8.90€,
        the surcharge should be 1.10€.
        """
        cart_value = 890
        surcharge = self.calculator.calculate_minimum_cart_value_surcharge(cart_value=cart_value, min_cart_value=1000)
        self.assertEqual(surcharge, 110)

    def test_minimum_cart_value_no_surcharge(self):
        """If the cart value is over the minimum cart value, surcharge should be 0€.
        12€ cart value is over the min value of 11€.
        """
        cart_value = 1200
        surcharge = self.calculator.calculate_minimum_cart_value_surcharge(cart_value=cart_value, min_cart_value=1100)
        self.assertEqual(surcharge, 0)

    def test_minimum_cart_value_no_surcharge_edge_equal(self):
        """If the cart value is equal to the minimum cart value, surcharge should be 0€
        """
        cart_value = 1100
        surcharge = self.calculator.calculate_minimum_cart_value_surcharge(cart_value=cart_value, min_cart_value=1100)
        self.assertEqual(surcharge, 0)

    def test_minimum_cart_value_no_surcharge_edge_under(self):
        """If the cart value is one cent under minimum cart value, surcharge should be one cent.
        """
        cart_value = 1099
        surcharge = self.calculator.calculate_minimum_cart_value_surcharge(cart_value=cart_value, min_cart_value=1100)
        self.assertEqual(surcharge, 1)

    def test_minimum_cart_value_no_surcharge_edge_over(self):
        """If the cart value is one cent over the minimum cart value, surcharge should 0€.
        """
        cart_value = 1201
        surcharge = self.calculator.calculate_minimum_cart_value_surcharge(cart_value=cart_value, min_cart_value=1100)
        self.assertEqual(surcharge, 0)


class TestFeeCalculatorDistanceSurcharge(unittest.TestCase):

    def setUp(self):
        settings.ENVIRONMENT = 'test'
        self.calculator = FeeCalculator()

    def test_delivery_distance_surcharge_min_fee(self):
        """Test the delivery distance fee function. The minimum fee should be 1€,
        if the distance is shorter than the minimum delivery distance.
        """
        surcharge = self.calculator.calculate_delivery_distance_surcharge(delivery_distance=100,
                                                                          minimum_delivery_fee=100,
                                                                          minimum_delivery_distance=500,
                                                                          delivery_fee_for_additional_distance=100,
                                                                          delivery_fee_for_the_first_km=200,
                                                                          additional_distance_after_first_km=500)
        self.assertEqual(surcharge, 100)

    def test_delivery_distance_surcharge_base_fee_edge_equal(self):
        """Test the delivery distance fee function. The surcharge should be 2€,
        if the distance is 1km.
        """
        surcharge = self.calculator.calculate_delivery_distance_surcharge(delivery_distance=1000,
                                                                          minimum_delivery_fee=100,
                                                                          minimum_delivery_distance=500,
                                                                          delivery_fee_for_additional_distance=100,
                                                                          delivery_fee_for_the_first_km=200,
                                                                          additional_distance_after_first_km=500)
        self.assertEqual(surcharge, 200)

    def test_delivery_distance_surcharge_base_fee_edge_under(self):
        """Test the delivery distance fee function. The surcharge should be 2€,
        if the distance is 1 meter under 1km.
        """
        surcharge = self.calculator.calculate_delivery_distance_surcharge(delivery_distance=999,
                                                                          minimum_delivery_fee=100,
                                                                          minimum_delivery_distance=500,
                                                                          delivery_fee_for_additional_distance=100,
                                                                          delivery_fee_for_the_first_km=200,
                                                                          additional_distance_after_first_km=500)
        self.assertEqual(surcharge, 200)

    def test_delivery_distance_surcharge_base_fee_edge_over(self):
        """Test the delivery distance fee function. The surcharge should be 3€,
        if the distance is 1 meter over 1km.
        """
        surcharge = self.calculator.calculate_delivery_distance_surcharge(delivery_distance=1001,
                                                                          minimum_delivery_fee=100,
                                                                          minimum_delivery_distance=500,
                                                                          delivery_fee_for_additional_distance=100,
                                                                          delivery_fee_for_the_first_km=200,
                                                                          additional_distance_after_first_km=500)
        self.assertEqual(surcharge, 300)

    def test_delivery_distance_surcharge_additional_distance_surcharge(self):
        """Test the delivery distance fee function. The surcharge should be 3€,
        if the distance is over 1km but under 1km + additional distance after first km.
        """
        surcharge = self.calculator.calculate_delivery_distance_surcharge(delivery_distance=1200,
                                                                          minimum_delivery_fee=100,
                                                                          minimum_delivery_distance=500,
                                                                          delivery_fee_for_additional_distance=100,
                                                                          delivery_fee_for_the_first_km=200,
                                                                          additional_distance_after_first_km=500)
        self.assertEqual(surcharge, 300)

    def test_delivery_distance_surcharge_additional_distance_surcharge_edge_case_lower(self):
        """Test the delivery distance fee function. The surcharge should be 3€,
        if the distance is over 1km but just under 1km + additional distance after first km.
        """
        surcharge = self.calculator.calculate_delivery_distance_surcharge(delivery_distance=1499,
                                                                          minimum_delivery_fee=100,
                                                                          minimum_delivery_distance=500,
                                                                          delivery_fee_for_additional_distance=100,
                                                                          delivery_fee_for_the_first_km=200,
                                                                          additional_distance_after_first_km=500)
        self.assertEqual(surcharge, 300)

    def test_delivery_distance_surcharge_additional_distance_surcharge_edge_case_equal(self):
        """Test the delivery distance fee function. The surcharge should be 3€,
        if the distance is equal to 1km + additional distance after first km.
        """
        surcharge = self.calculator.calculate_delivery_distance_surcharge(delivery_distance=1500,
                                                                          minimum_delivery_fee=100,
                                                                          minimum_delivery_distance=500,
                                                                          delivery_fee_for_additional_distance=100,
                                                                          delivery_fee_for_the_first_km=200,
                                                                          additional_distance_after_first_km=500)
        self.assertEqual(surcharge, 300)

    def test_delivery_distance_surcharge_additional_distance_surcharge_edge_case_higher(self):
        """Test the delivery distance fee function. The surcharge should be 4€,
        if the distance is just over 1km + additional distance after first km.
        """
        surcharge = self.calculator.calculate_delivery_distance_surcharge(delivery_distance=1501,
                                                                          minimum_delivery_fee=100,
                                                                          minimum_delivery_distance=500,
                                                                          delivery_fee_for_additional_distance=100,
                                                                          delivery_fee_for_the_first_km=200,
                                                                          additional_distance_after_first_km=500)
        self.assertEqual(surcharge, 400)


class TestFeeCalculatorNumberOfItems(unittest.TestCase):

    def setUp(self):
        settings.ENVIRONMENT = 'test'
        self.calculator = FeeCalculator()

    def test_number_of_items_fee_no_surcharge_lower(self):
        """If the number of items is under "the product amount for surcharge"
        no surcharge should be added.
        """
        surcharge = self.calculator.calculate_number_of_items_surcharge(items_amount=3,
                                                                        product_amount_for_surcharge=4,
                                                                        surcharge_fee=50,
                                                                        bulk_amount=12,
                                                                        bulk_charge_fee=120)
        self.assertEqual(surcharge, 0)

    def test_number_of_items_fee_no_surcharge_equal(self):
        """If the number of items is equal to "the product amount for surcharge"
        no surcharge should be added.
        """
        surcharge = self.calculator.calculate_number_of_items_surcharge(items_amount=4,
                                                                        product_amount_for_surcharge=4,
                                                                        surcharge_fee=50,
                                                                        bulk_amount=12,
                                                                        bulk_charge_fee=120)
        self.assertEqual(surcharge, 0)

    def test_number_of_items_fee_no_surcharge_one_surcharge(self):
        """If the number of items is one bigger than "the product amount for surcharge"
        one surcharge should be added.
        """
        surcharge = self.calculator.calculate_number_of_items_surcharge(items_amount=5,
                                                                        product_amount_for_surcharge=4,
                                                                        surcharge_fee=50,
                                                                        bulk_amount=12,
                                                                        bulk_charge_fee=120)
        self.assertEqual(surcharge, 50)

    def test_number_of_items_fee_no_bulk_multiple_surcharge(self):
        """If the number of items is under the bulk amount, but still has more products
        than the product amount for surcharge, the surcharge should be added for every product
        over the product amount for surcharge.
        """
        surcharge = self.calculator.calculate_number_of_items_surcharge(items_amount=11,
                                                                        product_amount_for_surcharge=4,
                                                                        surcharge_fee=50,
                                                                        bulk_amount=12,
                                                                        bulk_charge_fee=120)
        self.assertEqual(surcharge, 350)

    def test_number_of_items_fee_no_bulk_fee_when_equal(self):
        """If the number of items is equal to the bulk amount,
        no bulk fee should be added yet.
        """
        surcharge = self.calculator.calculate_number_of_items_surcharge(items_amount=12,
                                                                        product_amount_for_surcharge=4,
                                                                        surcharge_fee=50,
                                                                        bulk_amount=12,
                                                                        bulk_charge_fee=120)
        self.assertEqual(surcharge, 400)

    def test_number_of_items_fee_bulk_fee_when_over(self):
        """If the number of items is bigger than the bulk amount,
        bulk fee should be added.
        """
        surcharge = self.calculator.calculate_number_of_items_surcharge(items_amount=13,
                                                                        product_amount_for_surcharge=4,
                                                                        surcharge_fee=50,
                                                                        bulk_amount=12,
                                                                        bulk_charge_fee=120)
        self.assertEqual(surcharge, 570)


class TestFeeCalculatorRushHour(unittest.TestCase):

    def setUp(self):
        settings.ENVIRONMENT = 'test'
        self.test_rush_hours = [
            RushHours(
                day=4, start=time(15, 00, 00), end=time(19, 00, 00), fee=1.2  # friday 15-19, fee multiplier 1.2
            ),
            RushHours(
                # monday 9-12, fee multiplier 0.5 (50% discount)
                day=0, start=time(9, 00, 00), end=time(12, 00, 00), fee=0.5
            ),
            RushHours(
                day=4, start=time(18, 00, 00), end=time(21, 00, 00), fee=1.5  # friday 19-22, fee multiplier 1.5
            )
        ]

        self.calculator = FeeCalculator()

    def test_rush_hour_fee_rush_hour(self):
        """Rush hour fee returns the multiplier, that is added after all surcharges.
        When a single rush hour is active, the multiplier should be the fee from that rush hour.
        """
        rush_hour_multiplier = self.calculator.calculate_rush_hour_surcharge_multiplier(time="2024-01-19T15:00:20Z",
                                                                                        rush_hours=self.test_rush_hours)
        self.assertEqual(rush_hour_multiplier, 1.2)

    def test_rush_hour_fee_no_rush_hour(self):
        """Rush hour fee returns the multiplier, that is added after all surcharges.
        When a no rush hour is active, the multiplier should be the 1.
        """
        rush_hour_multiplier = self.calculator.calculate_rush_hour_surcharge_multiplier(time="2024-01-19T10:00:20Z",
                                                                                        rush_hours=self.test_rush_hours)
        self.assertEqual(rush_hour_multiplier, 1)

    def test_rush_hour_fee_rush_hour_edge_case_below(self):
        """Rush hour fee returns the multiplier, that is added after all surcharges.
        When ordering just before rush hour, multiplier should be 1.
        """
        rush_hour_multiplier = self.calculator.calculate_rush_hour_surcharge_multiplier(time="2024-01-19T14:59:59Z",
                                                                                        rush_hours=self.test_rush_hours)
        self.assertEqual(rush_hour_multiplier, 1)

    def test_rush_hour_fee_rush_hour_edge_case_equal(self):
        """Rush hour fee returns the multiplier, that is added after all surcharges.
        When ordering just when rush hour starts, multiplier should be the fee multiplier from that rush hour.
        """
        rush_hour_multiplier = self.calculator.calculate_rush_hour_surcharge_multiplier(time="2024-01-19T15:00:00Z",
                                                                                        rush_hours=self.test_rush_hours)
        self.assertEqual(rush_hour_multiplier, 1.2)

    def test_rush_hour_fee_rush_hour_edge_case_over(self):
        """Rush hour fee returns the multiplier, that is added after all surcharges.
        When ordering one second after rush hour starts, multiplier should be the fee multiplier from that rush hour.
        """
        rush_hour_multiplier = self.calculator.calculate_rush_hour_surcharge_multiplier(time="2024-01-19T15:00:01Z",
                                                                                        rush_hours=self.test_rush_hours)
        self.assertEqual(rush_hour_multiplier, 1.2)

    def test_rush_hour_fee_discount(self):
        """Rush hour fee returns the multiplier, that is added after all surcharges.
        When ordering while discount "rush hour" multiplier should be the fee multiplier from that rush hour.
        """
        rush_hour_multiplier = self.calculator.calculate_rush_hour_surcharge_multiplier(time="2024-01-29T11:00:00Z",
                                                                                        rush_hours=self.test_rush_hours)
        self.assertEqual(rush_hour_multiplier, 0.5)

    def test_rush_hour_fee_multiple_fees(self):
        """If there are multiple rush hours active, the multiplier should be the product of all the fees.
        In this case, 1.2*1.5=1.8
        """
        rush_hour_multiplier = self.calculator.calculate_rush_hour_surcharge_multiplier(time="2024-01-19T18:30:00Z",
                                                                                        rush_hours=self.test_rush_hours)
        self.assertEqual(rush_hour_multiplier, 1.8)


class TestFeeCalculatorMaxFee(unittest.TestCase):

    def setUp(self):
        settings.ENVIRONMENT = 'test'
        self.calculator = FeeCalculator()

    def test_max_total_delivery_fee_under_max(self):
        """If the total fee is under the max fee, the total fee should be returned.
        """
        total_fee = self.calculator.check_max_total_delivery_fee(total_delivery_fee=1000, max_total_delivery_fee=1500)
        self.assertEqual(total_fee, 1000)

    def test_max_total_delivery_fee_edge_under_max(self):
        """If the total fee is under the max fee, the total fee should be returned.
        """
        total_fee = self.calculator.check_max_total_delivery_fee(total_delivery_fee=1499, max_total_delivery_fee=1500)
        self.assertEqual(total_fee, 1499)

    def test_max_total_delivery_fee_edge_over_max(self):
        """If the total fee is under the max fee, the total fee should be returned.
        """
        total_fee = self.calculator.check_max_total_delivery_fee(total_delivery_fee=1501, max_total_delivery_fee=1500)
        self.assertEqual(total_fee, 1500)


class TestFeeCalculatorFreeDelivery(unittest.TestCase):

    def setUp(self):
        settings.ENVIRONMENT = 'test'
        self.calculator = FeeCalculator()

    def test_free_delivery_edge_over(self):
        """Delivery is free if the cart value is just over the threshold.
        """
        isfree = self.calculator.check_free_total_delivery_fee(cart_value=20001, min_cart_value_for_free_delivery=20000)
        self.assertEqual(isfree, True)

    def test_free_delivery_edge_equal(self):
        """Delivery is free if the cart value is equal to the threshold.
        """
        isfree = self.calculator.check_free_total_delivery_fee(cart_value=20000, min_cart_value_for_free_delivery=20000)
        self.assertEqual(isfree, True)

    def test_free_delivery_edge_under(self):
        """Delivery is free if the cart value is equal to the threshold.
        """
        isfree = self.calculator.check_free_total_delivery_fee(cart_value=19999, min_cart_value_for_free_delivery=20000)
        self.assertEqual(isfree, False)

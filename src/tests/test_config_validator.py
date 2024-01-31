import unittest
from datetime import time
from settings import settings
from services.config_validator import ConfigValidator
import test_config
from config import RushHours

class TestConfigValidatorMinCartValue(unittest.TestCase):

    def setUp(self):
        """The tests use test_config.py configuration, 
        so that changing the prod/dev config does not break the tests.
        """
        settings.ENVIRONMENT = 'test'
        self.config_validator = ConfigValidator()
        self.test_config = test_config
        self.original_min_cart_value = self.test_config.MINIMUM_CART_VALUE
    
    def test_minimum_cart_value_not_int(self):
        self.test_config.MINIMUM_CART_VALUE = "not int"
        self.assertEqual(self.config_validator.valid_config(config=self.test_config), 
                         "Error in config.py: MINIMUM_CART_VALUE must be a positive integer.")
    
    def test_minimum_cart_value_not_positive(self):
        self.test_config.MINIMUM_CART_VALUE = 1
        self.assertEqual(self.config_validator.valid_config(config=self.test_config), 
                         "valid")
    
    def test_minimum_cart_value_negative(self):
        self.test_config.MINIMUM_CART_VALUE = -1
        self.assertEqual(self.config_validator.valid_config(config=self.test_config), 
                         "Error in config.py: MINIMUM_CART_VALUE must be a positive integer.")
    
    def tearDown(self):
        """Restore the original values after each test.
        """
        self.test_config.MINIMUM_CART_VALUE = self.original_min_cart_value

class TestConfigValidatorMinDeliveryDistance(unittest.TestCase):

    def setUp(self):
        settings.ENVIRONMENT = 'test'
        self.config_validator = ConfigValidator()
        self.test_config = test_config
        self.original_min_delivery_distance = self.test_config.MINIMUM_DELIVERY_DISTANCE
    
    def test_minimum_delivery_distance_not_int(self):
        self.test_config.MINIMUM_DELIVERY_DISTANCE = "not int"
        self.assertEqual(self.config_validator.valid_config(config=self.test_config), 
                         "Error in config.py: MINIMUM_DELIVERY_DISTANCE must be a positive integer.")
    
    def test_minimum_delivery_distance_not_positive(self):
        self.test_config.MINIMUM_DELIVERY_DISTANCE = 1
        self.assertEqual(self.config_validator.valid_config(config=self.test_config), 
                         "valid")
    
    def test_minimum_delivery_distance_negative(self):
        self.test_config.MINIMUM_DELIVERY_DISTANCE = -1
        self.assertEqual(self.config_validator.valid_config(config=self.test_config), 
                         "Error in config.py: MINIMUM_DELIVERY_DISTANCE must be a positive integer.")
    
    def tearDown(self):
        self.test_config.MINIMUM_DELIVERY_DISTANCE = self.original_min_delivery_distance

class TestConfigValidatorRushHours(unittest.TestCase):

    def setUp(self):
        settings.ENVIRONMENT = 'test'
        self.config_validator = ConfigValidator()
        self.test_config = test_config
        self.original_rush_hours = self.test_config.RUSH_HOURS
    
    def test_rush_hours_not_list(self):
        self.test_config.RUSH_HOURS = "not list"
        self.assertEqual(self.config_validator.valid_config(config=self.test_config), 
                         "Error in config.py: Rush hours are not valid.")

    def test_rush_hours_weekday_not_weekday(self):
        self.test_config.RUSH_HOURS = [
        RushHours(day=7, start=time(15, 00, 00), end=time(19, 00, 00), fee=1.2)
        ]
        self.assertEqual(self.config_validator.valid_config(config=self.test_config), 
                         "Error in config.py: Rush hours are not valid.")
    
    def test_rush_hours_end_time_before_start_time(self):
        self.test_config.RUSH_HOURS = [
        RushHours(day=4, start=time(19, 00, 00), end=time(15, 00, 00), fee=1.2)
        ]
        self.assertEqual(self.config_validator.valid_config(config=self.test_config), 
                         "Error in config.py: Rush hours are not valid.")

    def test_rush_hours_end_time_start_time_equal(self):
        self.test_config.RUSH_HOURS = [
        RushHours(day=4, start=time(15, 00, 00), end=time(15, 00, 00), fee=1.2)
        ]
        self.assertEqual(self.config_validator.valid_config(config=self.test_config), 
                         "Error in config.py: Rush hours are not valid.")

    def tearDown(self):
        self.test_config.RUSH_HOURS = self.original_rush_hours
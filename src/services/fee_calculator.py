import math
from dateutil.parser import parse
import config
from models.delivery import Delivery


class FeeCalculator:
    """This class makes all the calculations related to the fee.
"""

    def __init__(self):
        self._fee = 0

    def calculate_fee(self, response_object: Delivery) -> int:
        """Main function to calculate the fee for the delivery.

        Returns:
            integer: The fee in cents
        """

        self._minimum_cart_value(response_object)
        self._delivery_distance_fee(response_object)
        self._number_of_items(response_object)
        self._rush_hour_fee(response_object)
        # Making sure the max delivery fee is not crossed.
        if self._fee > config.MAX_DELIVERY_FEE:
            self._fee = config.MAX_DELIVERY_FEE
        # Free delivery if certain threshold is passed.
        if response_object.cart_value >= config.MIN_CART_VALUE_FOR_FREE_DELIVERY:
            self._fee = 0

        return int(self._fee)

    def _minimum_cart_value(self, response_object: Delivery):
        """This functions adds surcharge to the fee, if cart value is under
            the minimum cart value.
        """
        min_cart_value = config.MINIMUM_CART_VALUE
        if response_object.cart_value < min_cart_value:
            surcharge = min_cart_value - response_object.cart_value
            self._fee += surcharge

    def _delivery_distance_fee(self, response_object: Delivery):
        """This function counts the extra fee from distance and adds it to the total fee.
        """

        if response_object.delivery_distance < config.MINIMUM_DELIVERY_DISTANCE:
            self._fee += config.MINIMUM_DELIVERY_FEE  # Adding the minimum fee.

        if response_object.delivery_distance >= config.MINIMUM_DELIVERY_DISTANCE:
            # Adding the first km fee.
            self._fee += config.DELIVERY_FEE_FOR_THE_FIRST_KM

        if response_object.delivery_distance > 1000:  # Extra charge after first km.
            extra_charge_multiplier = math.ceil(
                (response_object.delivery_distance - 1000) / config.ADDITIONAL_DISTANCE_AFTER_FIRST_KM)
            # Extra charge amount is counted by deducting the first 1000 metres from the distance, then dividing it with the additional distance and rounding it upwards.
            # Total extra charge is multiplier times the fee.
            self._fee += extra_charge_multiplier * \
                config.DELIVERY_FEE_FOR_ADDITIONAL_DISTANCE

    def _number_of_items(self, response_object: Delivery):
        """This function counts the fee for larger orders. No charge is added 
        if there are only PRODUCT_AMOUNT_FOR_SURCHARGE items or less.
        """
        if response_object.number_of_items > config.PRODUCT_AMOUNT_FOR_SURCHARGE:
            # Count how many extra items there are.
            extra_items = response_object.number_of_items - \
                config.PRODUCT_AMOUNT_FOR_SURCHARGE
            # Multiply the amount by the surcharge fee and add it to the total fee.
            self._fee += extra_items * config.SURCHARGE_FEE
        # If the order is considered bulk, add the bulk fee.
        if response_object.number_of_items > config.BULK_AMOUNT:
            self._fee += config.BULK_CHARGE_FEE

    def _rush_hour_fee(self, response_object: Delivery):
        # Get the time as datetime object from string
        parsed = parse(response_object.time)
        time_of_day = parsed.time()
        for rush_time in config.RUSH_HOURS:
            if parsed.weekday() == rush_time.day:
                if time_of_day >= rush_time.start and time_of_day <= rush_time.end:
                    # Multiply the fee with the chosen rush time fee
                    self._fee = self._fee * rush_time.fee

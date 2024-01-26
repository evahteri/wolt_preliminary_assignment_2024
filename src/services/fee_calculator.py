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

        self._fee += self.minimum_cart_value(cart_value=response_object.cart_value, min_cart_value=config.MINIMUM_CART_VALUE)
        self._fee += self.delivery_distance_fee(delivery_distance=response_object.delivery_distance,
                                                minimum_delivery_fee=config.MINIMUM_DELIVERY_FEE, 
                                                minimum_delivery_distance=config.MINIMUM_DELIVERY_DISTANCE, 
                                                delivery_fee_for_additional_distance=config.DELIVERY_FEE_FOR_ADDITIONAL_DISTANCE,
                                                delivery_fee_for_the_first_km=config.DELIVERY_FEE_FOR_THE_FIRST_KM,
                                                additional_distance_after_first_km=config.ADDITIONAL_DISTANCE_AFTER_FIRST_KM)
        self._fee += self.number_of_items_fee(items_amount=response_object.number_of_items,
                                          product_amount_for_surcharge=config.PRODUCT_AMOUNT_FOR_SURCHARGE,
                                          surcharge_fee=config.SURCHARGE_FEE,
                                          bulk_amount=config.BULK_AMOUNT,
                                          bulk_charge_fee=config.BULK_CHARGE_FEE
                                          )
        self._fee = self._fee * self.rush_hour_fee(time=response_object.time, rush_hours=config.RUSH_HOURS)
        # Making sure the max delivery fee is not crossed.
        if self._fee > config.MAX_DELIVERY_FEE:
            self._fee = config.MAX_DELIVERY_FEE
        # Free delivery if certain threshold is passed.
        if response_object.cart_value >= config.MIN_CART_VALUE_FOR_FREE_DELIVERY:
            self._fee = 0

        return int(self._fee)

    def minimum_cart_value(self, cart_value: int, min_cart_value: int) -> int:
        """This functions adds surcharge to the fee, if cart value is under
            the minimum cart value.
        """
        surcharge = 0
        min_cart_value = config.MINIMUM_CART_VALUE
        if cart_value < min_cart_value:
            surcharge = min_cart_value - cart_value
        return int(surcharge)
            
            

    def delivery_distance_fee(self, delivery_distance: int, 
                              minimum_delivery_distance: int,
                              minimum_delivery_fee: int,
                              delivery_fee_for_the_first_km: int,
                              additional_distance_after_first_km: int,
                              delivery_fee_for_additional_distance: int) -> int:
        """This function counts the extra fee from distance and adds it to the total fee.
        """
        fee = 0
        if delivery_distance < minimum_delivery_distance:
            fee += minimum_delivery_fee  # Adding the minimum fee.

        if delivery_distance >= minimum_delivery_distance:
            # Adding the first km fee.
            fee += delivery_fee_for_the_first_km

        if delivery_distance > 1000:  # Extra charge after first km.
            extra_charge_multiplier = math.ceil(
                (delivery_distance - 1000) / additional_distance_after_first_km)
            # Extra charge amount is counted by deducting the first 1000 metres from the distance, then dividing it with the additional distance and rounding it upwards.
            # Total extra charge is multiplier times the fee.
            fee += extra_charge_multiplier * \
                delivery_fee_for_additional_distance
        return int(fee)

    def number_of_items_fee(self, items_amount: int, 
                        product_amount_for_surcharge: int,
                        surcharge_fee: int,
                        bulk_amount: int,
                        bulk_charge_fee: int)-> int:
        """This function counts the fee for larger orders. No charge is added 
        if there are only PRODUCT_AMOUNT_FOR_SURCHARGE items or less.
        """
        fee = 0
        if items_amount > product_amount_for_surcharge:
            # Count how many extra items there are.
            extra_items = items_amount - \
                product_amount_for_surcharge
            # Multiply the amount by the surcharge fee and add it to the total fee.
            fee += extra_items * surcharge_fee
        # If the order is considered bulk, add the bulk fee.
        if items_amount > bulk_amount:
            fee += bulk_charge_fee
        return int(fee)

    def rush_hour_fee(self, time: str, rush_hours: config.RushHours) -> float:
        multiplier = 0
        # Get the time as datetime object from string
        parsed = parse(time)
        time_of_day = parsed.time()
        for rush_time in rush_hours:
            if parsed.weekday() == rush_time.day:
                if time_of_day >= rush_time.start and time_of_day <= rush_time.end:
                    # Multiply the fee with the chosen rush time fee
                    multiplier += rush_time.fee
        if multiplier == 0:
            multiplier = 1
        return float(multiplier)

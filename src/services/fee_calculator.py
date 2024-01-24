import math
from datetime import datetime
from dateutil.parser import parse

class FeeCalculator:
        """This class makes all the calculations related to the fee.
    """

        def __init__(self, configuration):
            self._configuration = configuration
            self._fee = 0

        def calculate_fee(self, response_object):
            """Main function to calculate the fee for the delivery.

            Returns:
                integer: The fee in cents
            """
            
            self._minimum_cart_value(response_object)
            self._delivery_distance_fee(response_object)
            self._number_of_items(response_object)
            self._rush_hour_fee(response_object)
            if self._fee > self._configuration["max_delivery_fee"]: # Making sure the max delivery fee is not crossed.
                self._fee = self._configuration["max_delivery_fee"]
            if response_object.cart_value >= self._configuration["max_cart_value_for_free_delivery"]: # Free delivery if certain threshold is passed.
                self._fee = 0
    
            return self._fee

        def _minimum_cart_value(self, response_object):
            """This functions adds surcharge to the fee, if cart value is under
                the minimum cart value.
            """
            min_cart_value = self._configuration["minimum_cart_value"]
            if response_object.cart_value < min_cart_value:
                surcharge = min_cart_value - response_object.cart_value
                self._fee += surcharge

        def _delivery_distance_fee(self, response_object):
            """This function counts the extra fee from distance and adds it to the total fee.
            """

            if response_object.delivery_distance < self._configuration["minimum_delivery_distance"]:
                self._fee += self._configuration["minimum_delivery_fee"] # Adding the minimum fee.
            
            if response_object.delivery_distance >= self._configuration["minimum_delivery_distance"]:
                self._fee += self._configuration["delivery_fee_for_the_first_km"] # Adding the first km fee.
            
            if response_object.delivery_distance > 1000: # Extra charge after first km.
                extra_charge_multiplier = math.ceil((response_object.delivery_distance - 1000 )/ self._configuration["additional_distance_after_first_km"])
                # Extra charge amount is counted by deducting the first 1000 metres from the distance, then dividing it with the additional distance and rounding it upwards.
                self._fee += extra_charge_multiplier * self._configuration["delivery_fee_for_additional_distance"] # Total extra charge is multiplier times the fee.
            

        def _number_of_items(self, response_object):
            """This function counts the fee for larger orders. No charge is added if there are only "product_amount_for_surcharge" items or less.
            """
            if response_object.number_of_items > self._configuration["product_amount_for_surcharge"]:
                # Count how many extra items there are.
                extra_items = response_object.number_of_items - self._configuration["product_amount_for_surcharge"]
                # Multiply the amount by the surcharge fee and add it to the total fee.
                self._fee += extra_items * self._configuration["surcharge_fee"]
            # If the order is considered bulk, add the bulk fee.
            if response_object.number_of_items > self._configuration["bulk_amount"]:
                self._fee += self._configuration["bulk_charge_fee"]

        def _rush_hour_fee(self, response_object):
            parsed = parse(response_object.time) # Get the time as datetime object from string
            time_of_day = parsed.time()
            for rush_time in self._configuration["rush_hours"]:
                if parsed.weekday() == rush_time["day"]:
                    time_object_start = datetime.strptime(rush_time["start"], "%H:%M:%S") # Convert string into datetime objects
                    time_object_end = datetime.strptime(rush_time["end"], "%H:%M:%S")
                    if time_of_day >= time_object_start.time() and time_of_day <= time_object_end.time():
                        self._fee = self._fee * rush_time["fee"] # Multiply the fee with the chosen rush time fee
                
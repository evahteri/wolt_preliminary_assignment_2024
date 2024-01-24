import json
import math

class FeeCalculator:
        """This class makes all the calculations related to the fee.
    """

        def __init__(self, conf_filename):
            self._conf_filename = conf_filename
            self._configuration = self.__config_parser__()
            self._fee = 0

        def __config_parser__(self):
            with open(f"../{self._conf_filename}", "r") as file:
                data = json.load(file)
            return data

        def calculate_fee(self, response_object):
            """Main function to calculate the fee for the delivery.

            Returns:
                integer: The fee in cents
            """
            
            self._minimum_cart_value(response_object)
            self._delivery_distance_fee(response_object)
            self._number_of_items()
            self._rush_hour_fee()
    
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
            

        def _number_of_items(self):
            #TODO
            pass

        def _rush_hour_fee(self):
            #TODO
            pass
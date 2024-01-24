import json

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
            self._delivery_distance_fee()
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

        def _delivery_distance_fee(self):
            #TODO
            pass

        def _number_of_items(self):
            #TODO
            pass

        def _rush_hour_fee(self):
            #TODO
            pass
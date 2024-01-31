import datetime


class DeliveryRequestValidator:
    def __init__(self):
        self._error = "valid"

    def valid_delivery_request(self, delivery_request: dict) -> str:
        """Checks if the delivery request is valid.
        """
        if self.valid_cart_value(delivery_request["cart_value"]) is False:
            self._error = "Cart value must be a positive integer."
        if self.valid_delivery_distance(delivery_request["delivery_distance"]) is False:
            self._error = "Delivery distance must be a positive integer."
        if self.valid_number_of_items(delivery_request["number_of_items"]) is False:
            self._error = "Number of items must be an integer with a value over 1."
        if self.valid_time(delivery_request["time"]) is False:
            self._error = "Time must be string type in UTC, ISO 8601 format."
        return self._error

    def valid_cart_value(self, cart_value) -> bool:
        """Checks if the cart value is a positive integer.
        """
        if not isinstance(cart_value, int):
            return False
        if cart_value < 0:
            return False
        return True

    def valid_delivery_distance(self, delivery_distance) -> bool:
        """Checks if the delivery distance is a positive integer.
        """
        if not isinstance(delivery_distance, int):
            return False
        if delivery_distance < 0:
            return False
        return True

    def valid_number_of_items(self, number_of_items) -> bool:
        """Checks if the number of items is a positive integer.
        """
        if not isinstance(number_of_items, int):
            return False
        if number_of_items < 1:
            return False
        return True

    def valid_time(self, time) -> bool:
        """Checks if the time is in right format (UTC, ISO 8601)
        """
        if not isinstance(time, str):
            return False
        try:
            datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")
            return True
        except ValueError:
            return False

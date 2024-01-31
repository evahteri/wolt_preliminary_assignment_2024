class ConfigValidator:
    def __init__(self):
        self._error = "valid"

    def valid_config(self, config) -> str:
        """Checks if the configuration file is valid.
        """
        config_variables_pos_int = [
            "MINIMUM_CART_VALUE",
            "MINIMUM_DELIVERY_DISTANCE",
            "DELIVERY_FEE_FOR_THE_FIRST_KM",
            "ADDITIONAL_DISTANCE_AFTER_FIRST_KM",
            "DELIVERY_FEE_FOR_ADDITIONAL_DISTANCE",
            "MINIMUM_DELIVERY_FEE",
            "PRODUCT_AMOUNT_FOR_SURCHARGE",
            "SURCHARGE_FEE",
            "MAX_DELIVERY_FEE",
            "MIN_CART_VALUE_FOR_FREE_DELIVERY",
        ]

        for variable in config_variables_pos_int:
            value = getattr(config, variable)
            if not self.is_positive_integer(value):
                self._error = f"Error in config.py: {variable} must be a positive integer."
                break
        if not self.validate_rush_hours(config.RUSH_HOURS):
            self._error = "Error in config.py: Rush hours are not valid."

        return self._error

    def is_positive_integer(self, value) -> bool:
        """Checks if the cart value is a positive integer.
        """
        if not isinstance(value, int):
            return False
        if value < 0:
            return False
        return True

    def validate_rush_hours(self, rush_hours: list) -> bool:
        """Checks if the rush hours are valid. The rush hour cannot end before
        it starts and week cannot be negative or over 6.
        """
        if not isinstance(rush_hours, list):
            return False
        for rush_hour in rush_hours:
            if rush_hour.day < 0 or rush_hour.day > 6:
                return False
            if rush_hour.start >= rush_hour.end:
                return False
        return True

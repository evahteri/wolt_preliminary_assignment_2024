import math
from dateutil.parser import parse
import config
import test_config
from models.order_model import OrderModel
from settings import settings


class FeeCalculator:
    """This class makes all the calculations related to the fee.
    """

    def __init__(self):
        """_summary_
        """
        self._total_delivery_fee = 0
        if settings.ENVIRONMENT == 'test':
            self.config = test_config
        else:
            self.config = config

    def calculate_total_delivery_fee(self, response_object: OrderModel) -> int:
        """Main function to calculate the fee for the delivery.
        First, the minimum cart value surcharge is added.
        Second, the delivery distance surcharge is added.
        Third, the number of items surcharge is added.
        Fourth, the rush hour surcharge is added.
        Fifth, the maximum fee is checked.
        Sixth, the free delivery is checked.
        Finally, the total fee is returned.

        Returns:
            int: The total delivery fee in cents.
        """

        self._total_delivery_fee += self.calculate_minimum_cart_value_surcharge(
            cart_value=response_object.cart_value,
            min_cart_value=self.config.MINIMUM_CART_VALUE
        )
        self._total_delivery_fee += self.calculate_delivery_distance_surcharge(
            delivery_distance=response_object.delivery_distance,
            minimum_delivery_fee=self.config.MINIMUM_DELIVERY_FEE,
            minimum_delivery_distance=self.config.MINIMUM_DELIVERY_DISTANCE,
            delivery_fee_for_additional_distance=self.config.DELIVERY_FEE_FOR_ADDITIONAL_DISTANCE,
            delivery_fee_for_the_first_km=self.config.DELIVERY_FEE_FOR_THE_FIRST_KM,
            additional_distance_after_first_km=self.config.ADDITIONAL_DISTANCE_AFTER_FIRST_KM
        )
        self._total_delivery_fee += self.calculate_number_of_items_surcharge(
            items_amount=response_object.number_of_items,
            product_amount_for_surcharge=self.config.PRODUCT_AMOUNT_FOR_SURCHARGE,
            surcharge_fee=self.config.SURCHARGE_FEE,
            bulk_amount=self.config.BULK_AMOUNT,
            bulk_charge_fee=self.config.BULK_CHARGE_FEE
        )
        self._total_delivery_fee *= self.calculate_rush_hour_surcharge_multiplier(
            time=response_object.time,
            rush_hours=self.config.RUSH_HOURS
        )
        self._total_delivery_fee = self.check_max_total_delivery_fee(
            total_delivery_fee=self._total_delivery_fee,
            max_total_delivery_fee=self.config.MAX_DELIVERY_FEE
        )
        if self.check_free_total_delivery_fee(
            cart_value=response_object.cart_value,
            min_cart_value_for_free_delivery=self.config.MIN_CART_VALUE_FOR_FREE_DELIVERY
        ):
            self._total_delivery_fee = 0
        return int(self._total_delivery_fee)

    def check_max_total_delivery_fee(self, total_delivery_fee: int, max_total_delivery_fee: int) -> int:
        """Makes sure the max fee is not crossed.
        """
        return int(min(total_delivery_fee, max_total_delivery_fee))

    def check_free_total_delivery_fee(self, cart_value: int, min_cart_value_for_free_delivery: int) -> bool:
        """Checks if the cart value is over the minimum for free delivery.
        """
        if cart_value >= min_cart_value_for_free_delivery:
            return True
        return False

    def calculate_minimum_cart_value_surcharge(self, cart_value: int, min_cart_value: int) -> int:
        """This functions adds surcharge to the fee, if cart value is under
            the minimum cart value.
        """
        min_cart_value_surcharge = 0
        if cart_value < min_cart_value:
            min_cart_value_surcharge = min_cart_value - cart_value
        return int(min_cart_value_surcharge)

    def calculate_delivery_distance_surcharge(self, delivery_distance: int,
                                              minimum_delivery_distance: int,
                                              minimum_delivery_fee: int,
                                              delivery_fee_for_the_first_km: int,
                                              additional_distance_after_first_km: int,
                                              delivery_fee_for_additional_distance: int) -> int:
        """This function counts the extra fee from distance.
        """
        delivery_distance_surcharge = 0
        if delivery_distance < minimum_delivery_distance:
            delivery_distance_surcharge += minimum_delivery_fee

        if delivery_distance >= minimum_delivery_distance:
            delivery_distance_surcharge += delivery_fee_for_the_first_km

        if delivery_distance > 1000:
            extra_charge_multiplier = math.ceil(
                (delivery_distance - 1000) / additional_distance_after_first_km)
            # Extra charge amount is counted by deducting the first 1000 metres from the distance,
            # then dividing it with the additional distance and rounding it upwards.
            delivery_distance_surcharge += extra_charge_multiplier * \
                delivery_fee_for_additional_distance
        return int(delivery_distance_surcharge)

    def calculate_number_of_items_surcharge(self, items_amount: int,
                                            product_amount_for_surcharge: int,
                                            surcharge_fee: int,
                                            bulk_amount: int,
                                            bulk_charge_fee: int) -> int:
        """This function counts the fee for larger orders. No charge is added
        if there are only PRODUCT_AMOUNT_FOR_SURCHARGE items or less.
        """
        number_of_items_surcharge = 0
        if items_amount > product_amount_for_surcharge:
            extra_items = items_amount - \
                product_amount_for_surcharge
            number_of_items_surcharge += extra_items * surcharge_fee
        if items_amount > bulk_amount:
            number_of_items_surcharge += bulk_charge_fee
        return int(number_of_items_surcharge)

    def calculate_rush_hour_surcharge_multiplier(self, time: str, rush_hours: list) -> float:
        """Calculating the rush hour surcharge multiplier. Config might include multiple rush hours,
        so the function loops through them.
        """
        surcharge_multiplier = 1
        parsed = parse(time)
        time_of_day = parsed.time()
        for rush_time in rush_hours:
            if parsed.weekday() == rush_time.day:
                if time_of_day >= rush_time.start and time_of_day <= rush_time.end:
                    surcharge_multiplier *= rush_time.fee
        return round(float(surcharge_multiplier), 1)

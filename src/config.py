from pydantic import BaseModel
from datetime import time


class RushHours(BaseModel):
    day: int  # 0 = Monday,..., 6 = Sunday
    # e.g. datetime.time object as time(hours, minutes, seconds), e.g. time(15,00,00)
    start: time
    end: time  # e.g. time(19,00,00)
    fee: float  # Multiplier, e.g. 1.2


MINIMUM_CART_VALUE: int = 1000  # If the cart value is less than this, a small order surcharge is added to the delivery price (10€ = 1000).
MINIMUM_DELIVERY_DISTANCE: int = 500  # The minimum delivery distance as meters.
DELIVERY_FEE_FOR_THE_FIRST_KM: int = 200  # The delivery fee for the first km.
ADDITIONAL_DISTANCE_AFTER_FIRST_KM: int = 500  # The distance the courier has to travel after the first km, delivery_fee_for_additional_distance value is added for every additional distance.
DELIVERY_FEE_FOR_ADDITIONAL_DISTANCE: int = 100  # This is added to the delivery fee for every configured additional distance.
MINIMUM_DELIVERY_FEE: int = 100  # The minimum delivery fee.
BULK_AMOUNT: int = 12  # Amount of products that is considered bulk.
BULK_CHARGE_FEE: int = 120  # This is added if the order is considered bulk.
PRODUCT_AMOUNT_FOR_SURCHARGE: int = 4  # Every product after this number has a surcharge fee.
SURCHARGE_FEE: int = 50  # This is added for every product after PRODUCT_AMOUNT_FOR_SURCHARGE.
MAX_DELIVERY_FEE: int = 1500  # The maximum delivery fee that is never exceeded.
MIN_CART_VALUE_FOR_FREE_DELIVERY: int = 20000  # The minimum cart value for free delivery.
RUSH_HOURS: list = [
    RushHours(day=4, start=time(15, 00, 00), end=time(19, 00, 00), fee=1.2)
]  # The rush hours for the additional fee(s), created as RushHours objects in a list.

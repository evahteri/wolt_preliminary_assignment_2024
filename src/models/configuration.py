from pydantic import BaseModel

class Configuration(BaseModel):  
    minimum_cart_value: int
    minimum_delivery_distance: int
    delivery_fee_for_the_first_km: int
    additional_distance_after_first_km: int
    delivery_fee_for_additional_distance: int
    minimum_delivery_fee: int
    bulk_amount: int
    bulk_charge_fee: int
    product_amount_for_surcharge: int
    surcharge_fee: int
    max_delivery_fee: int
    max_cart_value_for_free_delivery: int
    rush_hours: list
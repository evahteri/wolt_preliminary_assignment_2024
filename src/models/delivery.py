from pydantic import BaseModel


class Delivery(BaseModel):
    cart_value: int
    delivery_distance: int
    number_of_items: int
    time: str

from pydantic import BaseModel


class Delivery(BaseModel):
    """This class is used validate the request body.
    """
    cart_value: int
    delivery_distance: int
    number_of_items: int
    time: str

from pydantic import BaseModel


class DeliveryFeeModel(BaseModel):
    delivery_fee: int

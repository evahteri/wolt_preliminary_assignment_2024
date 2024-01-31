from pydantic import BaseModel


class Fee(BaseModel):
    delivery_fee: int

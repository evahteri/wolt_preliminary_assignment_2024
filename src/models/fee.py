from pydantic import BaseModel

class Fee(BaseModel):
    """This class is used validate the response body for the delivery fee.
    """
    delivery_fee: int
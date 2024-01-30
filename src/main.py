from fastapi import FastAPI
from models.delivery import Delivery
from services.fee_calculator import FeeCalculator
from models.fee import Fee

app = FastAPI()

@app.post("/", response_model=Fee)
def index(delivery: Delivery) -> Fee:
    """Endpoint to get the delivery fee

    Returns:
        JSON: JSON object with the delivery fee
    """
    delivery_fee = FeeCalculator().calculate_total_delivery_fee(response_object=delivery)

    return Fee(delivery_fee=delivery_fee)

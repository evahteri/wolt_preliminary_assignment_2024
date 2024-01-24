from fastapi import FastAPI
from models.delivery import Delivery
from services.fee_calculator import FeeCalculator

app = FastAPI()
conf_filename = "config.json" # Adjust this if you want to use different configuration file.

@app.post("/")
def index(delivery: Delivery):
    """Endpoint to get the delivery fee

    Returns:
        JSON: JSON object with the delivery fee
    """
    delivery_fee = FeeCalculator(conf_filename).calculate_fee(response_object=delivery)
    return {"delivery_fee": delivery_fee}
import json
from fastapi import FastAPI
from models.delivery import Delivery
from services.fee_calculator import FeeCalculator
from models.configuration import Configuration

app = FastAPI()
conf_filename = "config.json" # Adjust this if you want to use different configuration file.

def config_parser(configuration: Configuration):
    """Data validation for te configuration file
    """
    return configuration

@app.post("/")
def index(delivery: Delivery):
    """Endpoint to get the delivery fee

    Returns:
        JSON: JSON object with the delivery fee
    """
    with open(f"../{conf_filename}", "r") as file:
        data = json.load(file)
    configuration = config_parser(data)

    delivery_fee = FeeCalculator(configuration=configuration).calculate_fee(response_object=delivery)
    return {"delivery_fee": delivery_fee}
import json
from typing import Any
from fastapi import FastAPI
from models.delivery import Delivery
from services.fee_calculator import FeeCalculator
from models.configuration import Configuration
from models.fee import Fee

app = FastAPI()
conf_filename = "config.json" # Adjust this if you want to use a different configuration file.

def config_validator(configuration: Configuration):
    """Data validation for the configuration file
    """
    return configuration

@app.post("/", response_model=Fee)
def index(delivery: Delivery) -> Fee:
    """Endpoint to get the delivery fee

    Returns:
        JSON: JSON object with the delivery fee
    """
    with open(f"../{conf_filename}", "r") as file:
        data = json.load(file)
    configuration = config_validator(data)

    delivery_fee = FeeCalculator(configuration=configuration).calculate_fee(response_object=delivery)
    
    return Fee(delivery_fee=delivery_fee)
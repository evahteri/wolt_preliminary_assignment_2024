from fastapi import FastAPI, Request
import uvicorn
from fastapi.responses import JSONResponse
from models.delivery import Delivery
from services.fee_calculator import FeeCalculator
from services.request_validator import DeliveryRequestValidator
from services.config_validator import ConfigValidator
from models.fee import Fee
import config

class DeliveryValidatorException(Exception):
    def __init__(self, name: str):
        self.name = name

app = FastAPI()

@app.exception_handler(DeliveryValidatorException)
def delivery_exception_handler(request: Request, exc: DeliveryValidatorException):
    return JSONResponse(
        status_code = 400,
        content = exc.name,
    )

@app.post("/", response_model=Fee)
def index(delivery: dict) -> Fee:
    """Endpoint to get the delivery fee. Valid JSON request body follows the format:
    {
        "cart_value": int,
        "delivery_distance": int,
        "number_of_items": int,
        "time": str in ISO 8601 format (UTC)
    }

    Returns:
        JSON: JSON object with the delivery fee. e.g. {"delivery_fee": 500}
    """
    request_validity = DeliveryRequestValidator().valid_delivery_request(delivery_request=delivery)
    if request_validity != "valid":
        raise DeliveryValidatorException(name=request_validity)
    delivery = Delivery(**delivery)

    delivery_fee = FeeCalculator().calculate_total_delivery_fee(response_object=delivery)

    return Fee(delivery_fee=delivery_fee)

if __name__ == "__main__":
    config_validity = ConfigValidator().valid_config(config=config)
    if config_validity != "valid":
        print("Could not start the server, due to the following error:")
        print(config_validity)
    else:
        uvicorn.run(app, host="0.0.0.0", port=8000)
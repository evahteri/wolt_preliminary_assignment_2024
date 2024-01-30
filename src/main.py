from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from models.delivery import Delivery
from services.fee_calculator import FeeCalculator
from services.request_validator import DeliveryRequestValidator
from models.fee import Fee

class ValidatorException(Exception):
    def __init__(self, name: str):
        self.name = name

app = FastAPI()

@app.exception_handler(ValidatorException)
def delivery_exception_handler(request: Request, exc: ValidatorException):
    return JSONResponse(
        status_code = 400,
        content = exc.name,
    )

@app.post("/", response_model=Fee)
def index(delivery: dict) -> Fee:
    """Endpoint to get the delivery fee

    Returns:
        JSON: JSON object with the delivery fee
    """
    request_validity = DeliveryRequestValidator().valid_delivery_request(delivery_request=delivery)
    if request_validity != "valid":
        raise ValidatorException(name=request_validity)
    delivery = Delivery(**delivery)
    delivery_fee = FeeCalculator().calculate_total_delivery_fee(response_object=delivery)

    return Fee(delivery_fee=delivery_fee)

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def index():
    """Endpoint to get the delivery fee

    Returns:
        JSON: JSON object with the delivery fee
    """
    return {"message": "Hello World"}
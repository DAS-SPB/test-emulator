from pydantic import BaseModel


class UpdateOrderRequestModel(BaseModel):
    order_id: str
    status: str
    amount: int | float

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "order_id": "123456789",
                    "status": "SUCCESS",
                    "amount": 150.20
                }
            ]
        }
    }


class UpdateOrderResponseModel(BaseModel):
    order_id: str
    message: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "order_id": "123456789",
                    "message": "Order updated successfully"
                }
            ]
        }
    }

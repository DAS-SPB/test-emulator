from pydantic import BaseModel, Field
from typing import Optional


class CallbackRequestModel(BaseModel):
    order_id: str = Field(min_length=5, max_length=20)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "order_id": "123456789"
                }
            ]
        }
    }


class CallbackModel(BaseModel):
    reference: Optional[str] = None
    status: str
    amount: int | float


class CallbackQueryModel(BaseModel):
    payment: Optional[CallbackModel] = None
    code: Optional[int] = None
    message: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "payment":
                        {
                            "reference": "generated reference",
                            "status": "SUCCESS",
                            "amount": 150.20
                        },
                    "code": 10,
                    "message": "message text"
                }
            ]
        }
    }


class CallbackResponseModel(BaseModel):
    message: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "message": "Callback successfully executed"
                }
            ]
        }
    }

from pydantic import BaseModel, Field
from typing import Optional, List

REQUEST_CURRENCY = "EUR"
REQUEST_SUBCLASS = "subclass"


class Data(BaseModel):
    amount: float
    currency: str = REQUEST_CURRENCY


class Customer(BaseModel):
    full_name: str = Field(min_length=1, max_length=256)
    email: str = Field(min_length=5, max_length=256)


class PaymentRequest(BaseModel):
    order_id: str = Field(min_length=5, max_length=10)
    data: Data
    customer: List[Customer]
    subclass: str = REQUEST_SUBCLASS

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "order_id": "123456789",
                    "data": {
                        "amount": 100.20,
                        "currency": "EUR"
                    },
                    "customer": [
                        {
                            "full_name": "Full Name",
                            "email": "email@email.com"
                        }
                    ],
                    "subclass": "subclass"
                }
            ]
        }
    }


class Payment(BaseModel):
    reference: str


class PaymentResponse(BaseModel):
    payment: Optional[Payment] = None
    code: int
    message: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "payment":
                        {
                            "reference": "generated uuid"
                        },
                    "code": 10,
                    "message": "message text"
                }
            ]
        }
    }

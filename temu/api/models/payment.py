from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

REQUEST_CURRENCY = "EUR"
REQUEST_SUBCLASS = "subclass"


class CurrencyEnum(str, Enum):
    currency = "EUR"


class SubclassEnum(str, Enum):
    subclass = "subclass"


class DataModel(BaseModel):
    amount: int | float
    currency: CurrencyEnum


class CustomerModel(BaseModel):
    full_name: str = Field(min_length=1, max_length=256)
    email: str = Field(min_length=5, max_length=256)


class PaymentRequestModel(BaseModel):
    order_id: str = Field(min_length=5, max_length=20)
    data: DataModel
    customer: List[CustomerModel]
    subclass: SubclassEnum
    callback_url: str

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
                    "subclass": "subclass",
                    "callback_url": "https://webhook.site/xxx"
                }
            ]
        }
    }


class PaymentModel(BaseModel):
    reference: str


class PaymentResponseModel(BaseModel):
    payment: Optional[PaymentModel] = None
    code: Optional[int] = None
    message: Optional[str] = None

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

from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

REQUEST_SUBCLASS = "subclass"


class SubclassEnum(str, Enum):
    subclass = "subclass"


class CheckStatusRequestModel(BaseModel):
    order_id: str = Field(min_length=5, max_length=20)
    subclass: SubclassEnum

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "order_id": "123456789",
                    "subclass": "subclass"
                }
            ]
        }
    }


class CheckStatusModel(BaseModel):
    reference: Optional[str] = None
    status: str
    amount: int | float


class CheckStatusResponseModel(BaseModel):
    payment: Optional[CheckStatusModel] = None
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

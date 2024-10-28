from pydantic import BaseModel


class UpdateOrderRequestModel(BaseModel):
    order_id: str
    status: str
    amount: int | float


class UpdateOrderResponseModel(BaseModel):
    order_id: str
    message: str

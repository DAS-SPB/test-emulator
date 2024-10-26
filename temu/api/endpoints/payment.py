from fastapi import APIRouter, status
from ..models.payment import PaymentRequestModel, PaymentResponseModel
from ...db.database import insert_order, find_order, update_order
from ...db.connection import collection_orders

import uuid

router = APIRouter()


@router.post("/payment", response_model=PaymentResponseModel, status_code=status.HTTP_200_OK)
async def payment_creation(request: PaymentRequestModel):
    await insert_order(data=request.dict(), collection=collection_orders)

    return PaymentResponseModel(
        payment={"reference": str(uuid.uuid4())},
        code=10,
        message="Created successfully"
    )

from fastapi import APIRouter, status
from ..schemas.paymentDTO import PaymentRequest, PaymentResponse

import uuid

router = APIRouter()


@router.post("/payment", response_model=PaymentResponse, status_code=status.HTTP_200_OK)
async def payment_creation(request: PaymentRequest):
    return PaymentResponse(
        payment={"reference": str(uuid.uuid4())},
        code=10,
        message="Created successfully"
    )

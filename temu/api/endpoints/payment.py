from fastapi import APIRouter, status, Depends, Response
from ..models.payment import PaymentRequestModel, PaymentResponseModel
from ..signature.signature import signature_verification, signature_creation
from ...db.database import insert_order
from ...db.connection import collection_orders

import uuid

router = APIRouter()

# several error cases as an example
RESPONSE_CASES = {
    # HTTP 200, only mandatory fields
    101.00: {
        "status_code": status.HTTP_200_OK,
        "response_body": lambda: PaymentResponseModel(
            payment={"reference": str(uuid.uuid4())}
        )
    },
    # HTTP 400, error response
    102.00: {
        "status_code": status.HTTP_400_BAD_REQUEST,
        "response_body": lambda: PaymentResponseModel(
            code=5,
            message="Test error response"
        )
    },
    # HTTP 200, unsigned response
    103.00: {
        "status_code": status.HTTP_200_OK,
        "response_body": lambda: PaymentResponseModel(
            payment={"reference": str(uuid.uuid4())},
            code=10,
            message="Created successfully"
        ),
        "unsigned": True
    }
}


@router.post("/payment", response_model=PaymentResponseModel)
async def payment_creation(request: PaymentRequestModel, response: Response,
                           signed: None = Depends(signature_verification)):
    await insert_order(data=request.dict(), collection=collection_orders)

    case = RESPONSE_CASES.get(request.data.amount, None)

    if case:
        response.status_code = case.get("status_code")
        response_body = case.get("response_body")()
        unsigned = case.get("unsigned", False)
    else:
        response.status_code = status.HTTP_200_OK
        response_body = PaymentResponseModel(
            payment={"reference": str(uuid.uuid4())},
            code=10,
            message="Created successfully"
        )
        unsigned = False

    if unsigned:
        return response_body

    response_body_bytes = str(response_body.dict()).encode()
    signature = await signature_creation(response_body_bytes)
    response.headers["x-signature"] = signature

    return response_body

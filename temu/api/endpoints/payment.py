import logging
import uuid

from fastapi import APIRouter, status, Depends, Request, Response

from ..models.payment import PaymentRequestModel, PaymentResponseModel
from ..signature.signature import signature_verification, signature_creation
from ...db import database
from ...db.connection import collection_orders

router = APIRouter()
logger = logging.getLogger(__name__)

# several error cases as an example
RESPONSE_CASES = {
    # HTTP 200, only mandatory fields
    101: {
        "status_code": status.HTTP_200_OK,
        "response_body": lambda: PaymentResponseModel(
            payment={"reference": str(uuid.uuid4())}
        )
    },
    # HTTP 400, error response
    102: {
        "status_code": status.HTTP_400_BAD_REQUEST,
        "response_body": lambda: PaymentResponseModel(
            code=5,
            message="Test error response"
        )
    },
    # HTTP 200, unsigned response
    103: {
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
async def payment_creation(request: Request, payload: PaymentRequestModel, response: Response,
                           signed: None = Depends(signature_verification)):
    logger.info(f"Make payment. Incoming request with headers: {request.headers} and payload: {payload.json()}")

    order_data = payload.model_dump()
    reference = str(uuid.uuid4())

    order_data.update(
        {
            "reference": reference,
            "status": "PENDING"
        }
    )

    await database.insert_order(data=order_data, collection=collection_orders)

    case = RESPONSE_CASES.get(payload.data.amount, None)

    if case:
        response.status_code = case.get("status_code")
        response_body = case.get("response_body")()
        unsigned = case.get("unsigned", False)
    else:
        response.status_code = status.HTTP_200_OK
        response_body = PaymentResponseModel(
            payment={"reference": reference},
            code=10,
            message="Created successfully"
        )
        unsigned = False

    if not unsigned:
        signature = await signature_creation(response_body.model_dump())
        response.headers["x-signature"] = signature

    logger.info(
        f"Make payment. Outgoing response with status: {response.status_code}, additional headers: {response.headers}"
        f" and payload: {response_body.json()}")

    return response_body

import logging
from fastapi import APIRouter, status, Depends, Request, Response

from ..models.check_status import CheckStatusRequestModel, CheckStatusResponseModel
from ..signature.signature import signature_verification, signature_creation
from ...db import database
from ...db.connection import collection_orders

router = APIRouter()
logger = logging.getLogger(__name__)

# several error cases as an example
ERROR_CASES = {201, 202, 203}


async def error_case_response(response_data: dict) -> dict:
    response_cases = {
        # HTTP 200, only mandatory fields
        201: {
            "status_code": status.HTTP_200_OK,
            "response_body": lambda: CheckStatusResponseModel(
                payment={
                    "status": response_data.get("status"),
                    "amount": response_data.get("data", {}).get("amount")
                }
            )
        },
        # HTTP 400, error response
        202: {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "response_body": lambda: CheckStatusResponseModel(
                code=5,
                message="Test error response"
            )
        },
        # HTTP 200, unsigned response
        203: {
            "status_code": status.HTTP_200_OK,
            "response_body": lambda: CheckStatusResponseModel(
                payment={
                    "reference": response_data.get("reference"),
                    "status": response_data.get("status"),
                    "amount": response_data.get("data", {}).get("amount")
                },
                code=10,
                message="Success"
            ),
            "unsigned": True
        }
    }

    case = response_cases.get(response_data.get("data", {}).get("amount"))

    return case


@router.post("/check-status", response_model=CheckStatusResponseModel)
async def check_status(request: Request, payload: CheckStatusRequestModel, response: Response,
                       signed: None = Depends(signature_verification)):
    logger.info(f"Check status. Incoming request with headers: {request.headers} and payload: {payload.json()}")

    order_data = await database.find_order(data=payload.model_dump(), collection=collection_orders)
    amount = order_data.get("data", {}).get("amount")

    if amount in ERROR_CASES:
        case = await error_case_response(order_data)

        response.status_code = case.get("status_code")
        response_body = case.get("response_body")()
        unsigned = case.get("unsigned", False)
    else:
        response.status_code = status.HTTP_200_OK
        response_body = CheckStatusResponseModel(
            payment={
                "reference": order_data.get("reference"),
                "status": order_data.get("status"),
                "amount": amount
            },
            code=10,
            message="Success"
        )
        unsigned = False

    if not unsigned:
        signature = await signature_creation(response_body.model_dump())
        response.headers["x-signature"] = signature

    logger.info(
        f"Check status. Outgoing response with status: {response.status_code}, additional headers: {response.headers}"
        f" and payload: {response_body.json()}")

    return response_body

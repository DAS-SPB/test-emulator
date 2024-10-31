import httpx
import json
from fastapi import APIRouter, HTTPException, status

from ..models.callback import CallbackRequestModel, CallbackQueryModel, CallbackResponseModel
from ..signature.signature import signature_creation
from ...db import database
from ...db.connection import collection_orders

router = APIRouter()

# several error cases as an example
ERROR_CASES = {301, 302}


async def error_case_query(order_data: dict) -> dict:
    query_cases = {
        # only mandatory fields
        301: {
            "query_body": lambda: CallbackQueryModel(
                payment={
                    "status": order_data.get("status"),
                    "amount": order_data.get("data", {}).get("amount")
                }
            )
        },
        # HTTP 200, unsigned response
        302: {
            "query_body": lambda: CallbackQueryModel(
                payment={
                    "reference": order_data.get("reference"),
                    "status": order_data.get("status"),
                    "amount": order_data.get("data", {}).get("amount")
                },
                code=10,
                message="Success"
            ),
            "unsigned": True
        }
    }

    case = query_cases.get(order_data.get("data", {}).get("amount"))

    return case


@router.post("/callback-request", response_model=CallbackResponseModel, status_code=status.HTTP_200_OK)
async def callback_request(request: CallbackRequestModel):
    order_data = await database.find_order(data=request.model_dump(), collection=collection_orders)

    callback_url = order_data.get('callback_url')
    amount = order_data.get("data", {}).get("amount")

    if amount in ERROR_CASES:
        case = await error_case_query(order_data)
        query_body = case.get("query_body")()
        unsigned = case.get("unsigned", False)

    else:
        query_body = CallbackQueryModel(
            payment={
                "reference": order_data.get("reference"),
                "status": order_data.get("status"),
                "amount": order_data.get("data", {}).get("amount")
            },
            code=10,
            message="Callback"
        )
        unsigned = False

    query_body_dict = query_body.model_dump()
    query_signature = await signature_creation(query_body_dict)

    async with httpx.AsyncClient() as client:
        try:
            headers = {"x-signature": query_signature} if not unsigned else {}
            callback_response = await client.post(
                url=callback_url,
                json=query_body_dict,
                headers=headers
            )
        except httpx.RequestError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Failed to send callback request: {str(e)}")

    if callback_response.status_code != 200:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Callback request failed with status code {callback_response.status_code}")

    return CallbackResponseModel(message="Callback request successfully sent")

import logging
from fastapi import APIRouter, status

from ..models.update_order import UpdateOrderRequestModel, UpdateOrderResponseModel
from ...db import database
from ...db.connection import collection_orders

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/update-order", response_model=UpdateOrderResponseModel, status_code=status.HTTP_200_OK)
async def order_update(request: UpdateOrderRequestModel):
    logger.info(f"Update order. Incoming request with payload: {request.json()}")

    await database.update_order(data=request.model_dump(), collection=collection_orders)

    logger.info(f"Order was updated")

    return UpdateOrderResponseModel(
        order_id=request.order_id,
        message="Order updated successfully"
    )

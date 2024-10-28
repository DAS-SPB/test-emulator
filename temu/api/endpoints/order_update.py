from fastapi import APIRouter, status
from ..models.update_order import UpdateOrderRequestModel, UpdateOrderResponseModel
from ...db.database import update_order
from ...db.connection import collection_orders

router = APIRouter()


@router.post("/update-order", response_model=UpdateOrderResponseModel, status_code=status.HTTP_200_OK)
async def order_update(request: UpdateOrderRequestModel):
    await update_order(data=request.model_dump(), collection=collection_orders)

    return UpdateOrderResponseModel(
        order_id=request.order_id,
        message="Order updated successfully"
    )

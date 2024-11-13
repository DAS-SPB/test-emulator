import logging
from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo.results import InsertOneResult, UpdateResult
from fastapi import HTTPException, status

logger = logging.getLogger(__name__)


async def insert_order(data: dict, collection: AsyncIOMotorCollection) -> InsertOneResult:
    try:
        inserted_data = await collection.insert_one(data)
    except Exception as e:
        logger.error(f"Failed to insert data to MongoDB: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail={"message": f"Failed to insert data to MongoDB: {str(e)}"})

    return inserted_data


async def find_order(data: dict, collection: AsyncIOMotorCollection):
    query = {
        "order_id": data.get("order_id")
    }
    try:
        fetched_data = await collection.find_one(filter=query)
    except Exception as e:
        logger.error(f"Failed to fetch data from MongoDB: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail={"message": f"Failed to fetch data from MongoDB: {str(e)}"})

    if not fetched_data:
        logger.error("Order not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Order not found"})

    return fetched_data


async def update_order(data: dict, collection: AsyncIOMotorCollection) -> UpdateResult:
    query = {
        "order_id": data.get("order_id")
    }
    data_copy = {
        "data.amount": data.get("amount"),
        "status": data.get("status")
    }
    try:
        updated_record = await collection.update_one(filter=query, update={"$set": data_copy})
    except Exception as e:
        logger.error(f"Failed to update data in MongoDB: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail={"message": f"Failed to update data in MongoDB: {str(e)}"})

    if updated_record.modified_count == 0:
        logger.error("Order not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Order not found"})

    return updated_record

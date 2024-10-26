from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo.results import InsertOneResult, UpdateResult
from fastapi import HTTPException, status
from bson import ObjectId


async def insert_order(data: dict, collection: AsyncIOMotorCollection) -> InsertOneResult:
    try:
        inserted_data = await collection.insert_one(data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Failed to insert data to MongoDB: {str(e)}")

    return inserted_data


async def find_order(data: dict, collection: AsyncIOMotorCollection):
    try:
        fetched_data = await collection.find_one(data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Failed to fetch data from MongoDB: {str(e)}")

    return fetched_data


async def update_order(data: dict, collection: AsyncIOMotorCollection) -> UpdateResult:
    data_copy = data.copy()
    query = {
        "order_id": data.get("order_id"),
        "status": data.get("status"),
        "amount": data.get("amount")
    }
    try:
        updated_record = await collection.update_one(filter=query, update={"$set": data_copy})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Failed to update data in MongoDB: {str(e)}")

    return updated_record

import pytest
import pytest_asyncio
from httpx import AsyncClient
from fastapi import status

from temu.api.signature.signature import signature_creation
from temu.db.connection import client as motor_client

DATABASE_NAME = "test-emulator"
COLLECTION_NAME = "orders"


@pytest_asyncio.fixture
async def test_db():
    db = motor_client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
    await collection.delete_many({})
    return collection


@pytest_asyncio.fixture
async def async_client():
    from main import temu
    async with AsyncClient(app=temu, base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
async def test_create_payment(async_client, test_db, valid_payment_request):
    signature = await signature_creation(valid_payment_request)

    response = await async_client.post(
        "/test-emulator/payment",
        json=valid_payment_request,
        headers={"x-signature": signature}
    )

    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()

    created_order = await test_db.find_one({"reference": response_data["payment"]["reference"]})

    assert created_order is not None
    assert created_order.get("order_id") == "12345"
    assert created_order.get("status") == "PENDING"
    assert created_order.get("subclass") == "subclass"
    assert created_order.get("callback_url") == "https://example.com/callback"
    assert created_order.get("customer")[0].get("full_name") == "John Doe"
    assert created_order.get("customer")[0].get("email") == "johndoe@example.com"
    assert created_order.get("data").get("amount") == 100.22
    assert created_order.get("data").get("currency") == "EUR"

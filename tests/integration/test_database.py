import pytest
import asyncio
import pytest_asyncio
from motor.motor_asyncio import AsyncIOMotorCollection
from httpx import AsyncClient, ASGITransport
from typing import Dict, Any
from fastapi import status

from temu.api.signature.signature import signature_creation
from temu.db.connection import client as motor_client

DATABASE_NAME = "test-emulator"
COLLECTION_NAME = "orders"


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def test_db():
    db = motor_client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
    await collection.delete_many({})
    return collection


@pytest_asyncio.fixture
async def async_client():
    from main import temu
    async with AsyncClient(transport=ASGITransport(app=temu), base_url="http://test.test-emulator") as client:
        yield client


@pytest.mark.asyncio
async def test_create_payment(
        async_client: AsyncClient,
        test_db: AsyncIOMotorCollection,
        valid_payment_request: Dict[str, Any]
):
    signature = await signature_creation(valid_payment_request)

    response = await async_client.post(
        "/test-emulator/payment",
        json=valid_payment_request,
        headers={"x-signature": signature}
    )

    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()

    created_order = await test_db.find_one({"reference": response_data.get("payment").get("reference")})

    assert created_order is not None
    assert created_order.get("order_id") == "12345"
    assert created_order.get("status") == "PENDING"
    assert created_order.get("subclass") == "subclass"
    assert created_order.get("callback_url") == "https://example.com/callback"
    assert created_order.get("customer")[0].get("full_name") == "John Doe"
    assert created_order.get("customer")[0].get("email") == "johndoe@example.com"
    assert created_order.get("data").get("amount") == 100.22
    assert created_order.get("data").get("currency") == "EUR"


@pytest.mark.asyncio
async def test_update_payment(
        async_client: AsyncClient,
        test_db: AsyncIOMotorCollection,
        valid_update_order_request: Dict[str, Any]
):
    response = await async_client.post(
        "/test-emulator/update-order",
        json=valid_update_order_request
    )

    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()

    updated_order = await test_db.find_one({"order_id": response_data.get("order_id")})

    assert updated_order is not None
    assert updated_order.get("order_id") == "12345"
    assert updated_order.get("status") == "SUCCESS"
    assert updated_order.get("subclass") == "subclass"
    assert updated_order.get("callback_url") == "https://example.com/callback"
    assert updated_order.get("customer")[0].get("full_name") == "John Doe"
    assert updated_order.get("customer")[0].get("email") == "johndoe@example.com"
    assert updated_order.get("data").get("amount") == 150.20
    assert updated_order.get("data").get("currency") == "EUR"


@pytest.mark.asyncio
async def test_check_status(
        async_client: AsyncClient,
        test_db: AsyncIOMotorCollection,
        valid_check_status_request: Dict[str, Any]
):
    signature = await signature_creation(valid_check_status_request)

    response = await async_client.post(
        "/test-emulator/check-status",
        json=valid_check_status_request,
        headers={"x-signature": signature}
    )

    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()

    updated_order = await test_db.find_one({"reference": response_data.get("payment").get("reference")})

    assert updated_order is not None
    assert updated_order.get("order_id") == "12345"
    assert updated_order.get("status") == "SUCCESS"
    assert updated_order.get("subclass") == "subclass"
    assert updated_order.get("callback_url") == "https://example.com/callback"
    assert updated_order.get("customer")[0].get("full_name") == "John Doe"
    assert updated_order.get("customer")[0].get("email") == "johndoe@example.com"
    assert updated_order.get("data").get("amount") == 150.20
    assert updated_order.get("data").get("currency") == "EUR"


@pytest.mark.asyncio
async def test_callback(async_client: AsyncClient, test_db: AsyncIOMotorCollection):
    response = await async_client.post(
        "/test-emulator/callback-request",
        json={"order_id": "12345"}
    )

    # commented due to callback url == "https://example.com/callback"
    # assert response.status_code == status.HTTP_200_OK

    updated_order = await test_db.find_one({"order_id": "12345"})

    assert updated_order is not None
    assert updated_order.get("order_id") == "12345"
    assert updated_order.get("status") == "SUCCESS"
    assert updated_order.get("subclass") == "subclass"
    assert updated_order.get("callback_url") == "https://example.com/callback"
    assert updated_order.get("customer")[0].get("full_name") == "John Doe"
    assert updated_order.get("customer")[0].get("email") == "johndoe@example.com"
    assert updated_order.get("data").get("amount") == 150.20
    assert updated_order.get("data").get("currency") == "EUR"

import json
import pytest
from fastapi import status
from unittest.mock import AsyncMock

from temu.api.signature.signature import signature_creation
from temu.api.models.payment import PaymentResponseModel


@pytest.mark.asyncio
async def test_valid_signature(client, valid_payment_request, mocker):
    mock_insert_order = mocker.patch("temu.db.database.insert_order", new_callable=AsyncMock)
    mock_insert_order.return_value = None

    correct_signature = await signature_creation(json.dumps(valid_payment_request.model_dump()).encode('utf-8'))
    response = client.post(
        "/test-emulator/payment",
        json=valid_payment_request.dict(),
        headers={"x-signature": correct_signature}
    )
    assert response.status_code == status.HTTP_200_OK

    response_body = PaymentResponseModel(**response.json())
    assert response_body.code == 10
    assert response_body.message == "Created successfully"


@pytest.mark.asyncio
async def test_empty_signature(client, valid_payment_request):
    response = client.post(
        "/test-emulator/payment",
        json=valid_payment_request.dict(),
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    response_body = PaymentResponseModel(**response.json()['detail'])
    assert response_body.payment is None
    assert response_body.code == 2
    assert response_body.message == "Missing x-signature header"


@pytest.mark.asyncio
async def test_invalid_signature(client, valid_payment_request):
    incorrect_signature = "invalid_signature"

    response = client.post(
        "/test-emulator/payment",
        json=valid_payment_request.dict(),
        headers={"x-signature": incorrect_signature}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    response_body = PaymentResponseModel(**response.json()['detail'])
    assert response_body.payment is None
    assert response_body.code == 2
    assert response_body.message == "Invalid x-signature header"

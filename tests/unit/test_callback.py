import pytest
import httpx
from unittest.mock import patch
from fastapi import HTTPException
from temu.api.models.callback import CallbackRequestModel
from temu.api.signature.signature import signature_creation


@pytest.mark.asyncio
@patch("httpx.AsyncClient.post")
async def test_successful_callback_request(mock_post, mock_find_order, client):
    found_order = mock_find_order(response_amount=188.10, response_status="SUCCESS")

    mock_post.return_value.status_code = 200

    request_data = CallbackRequestModel(order_id="123456789").model_dump()
    temu_response = client.post(
        "/test-emulator/callback-request",
        json=request_data
    )

    assert temu_response.status_code == 200
    assert temu_response.json().get("message") == "Callback request successfully sent"

    callback_data = {
        "payment": {
            "reference": "order reference",
            "status": "SUCCESS",
            "amount": 188.10
        },
        "code": 10,
        "message": "Callback"
    }
    generated_signature = await signature_creation(callback_data)

    found_order.assert_called_once()
    mock_post.assert_called_once_with(
        url="https://example.com/callback",
        json=callback_data,
        headers={"x-signature": generated_signature}
    )


@pytest.mark.asyncio
@patch("httpx.AsyncClient.post")
async def test_callback_request_case_301(mock_post, mock_find_order, client):
    found_order = mock_find_order(response_amount=301, response_status="SUCCESS")

    mock_post.return_value.status_code = 200

    request_data = CallbackRequestModel(order_id="123456789").model_dump()
    temu_response = client.post(
        "/test-emulator/callback-request",
        json=request_data
    )

    assert temu_response.status_code == 200
    assert temu_response.json().get("message") == "Callback request successfully sent"

    callback_data = {
        "payment": {
            "reference": None,
            "status": "SUCCESS",
            "amount": 301
        },
        "code": None,
        "message": None
    }
    generated_signature = await signature_creation(callback_data)

    found_order.assert_called_once()
    mock_post.assert_called_once_with(
        url="https://example.com/callback",
        json=callback_data,
        headers={"x-signature": generated_signature}
    )


@pytest.mark.asyncio
@patch("httpx.AsyncClient.post")
async def test_callback_request_case_302(mock_post, mock_find_order, client):
    found_order = mock_find_order(response_amount=302, response_status="SUCCESS")

    mock_post.return_value.status_code = 200

    request_data = CallbackRequestModel(order_id="123456789").model_dump()
    temu_response = client.post(
        "/test-emulator/callback-request",
        json=request_data
    )

    assert temu_response.status_code == 200
    assert temu_response.json().get("message") == "Callback request successfully sent"

    found_order.assert_called_once()
    mock_post.assert_called_once_with(
        url="https://example.com/callback",
        json={
            "payment": {
                "reference": "order reference",
                "status": "SUCCESS",
                "amount": 302
            },
            "code": 10,
            "message": "Success"
        },
        headers={}
    )


@pytest.mark.asyncio
async def test_callback_request_db_error(mock_find_order, client):
    mock_find_order(side_effect=HTTPException(
        status_code=500,
        detail={"message": f"Failed to fetch data from MongoDB: Test Exception"})
    )

    request_data = CallbackRequestModel(order_id="123456789").model_dump()
    temu_response = client.post(
        "/test-emulator/callback-request",
        json=request_data
    )

    assert temu_response.status_code == 500
    assert temu_response.json().get("detail").get("message") == "Failed to fetch data from MongoDB: Test Exception"


@pytest.mark.asyncio
@patch("httpx.AsyncClient.post")
async def test_callback_request_received_400_status(mock_post, mock_find_order, client):
    found_order = mock_find_order(response_amount=302, response_status="SUCCESS")

    mock_post.return_value.status_code = 400

    request_data = CallbackRequestModel(order_id="123456789").model_dump()
    temu_response = client.post(
        "/test-emulator/callback-request",
        json=request_data
    )

    assert temu_response.status_code == 500
    assert temu_response.json().get("detail") == "Callback request failed with status code 400"

    found_order.assert_called_once()


@pytest.mark.asyncio
@patch("httpx.AsyncClient.post")
async def test_callback_request_connection_failed(mock_post, mock_find_order, client):
    found_order = mock_find_order(response_amount=302, response_status="SUCCESS")

    mock_post.side_effect = httpx.RequestError("Unable to connect",
                                               request=httpx.Request("POST", "https://example.com"))

    request_data = CallbackRequestModel(order_id="123456789").model_dump()
    temu_response = client.post(
        "/test-emulator/callback-request",
        json=request_data
    )

    assert temu_response.status_code == 500
    assert temu_response.json()["detail"] == "Failed to send callback request: Unable to connect"

    found_order.assert_called_once()

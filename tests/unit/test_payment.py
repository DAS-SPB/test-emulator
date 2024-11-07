import pytest
import json
from fastapi import HTTPException

from temu.api.signature.signature import signature_creation
from temu.api.models.payment import PaymentResponseModel


def check_payment_response(response: json, expected_status: int, expected_signature: bool, error_response: bool,
                           reference: bool, expected_code: int | None, expected_message: str | None):
    assert response.status_code == expected_status, \
        f"Expected response code: {expected_status}, but got: {response.status_code}"

    if expected_signature:
        assert "x-signature" in response.headers, "Expected 'x-signature' header in response headers, but it is absent"
    else:
        assert "x-signature" not in response.headers, "Unexpected 'x-signature' header in response headers"

    response_data = response.json()
    if error_response:
        assert "detail" in response_data, "Expected 'detail' in the response body for error response"
        error_detail = response_data.get("detail")

        response_body = PaymentResponseModel(**error_detail)
    else:
        response_body = PaymentResponseModel(**response_data)

    if reference:
        assert hasattr(response_body.payment, "reference"), "Expected 'reference' in response_body.payment"
    else:
        assert response_body.payment is None, "Expected 'payment' to be None"

    if expected_code:
        assert response_body.code == expected_code, \
            f"Expected response code: {expected_status}, but got: {response_body.code}"
    else:
        assert response_body.code is None, "Expected 'code' to be None"

    if expected_message:
        assert response_body.message == expected_message, \
            f"Expected 'message': {expected_message}, but got: {response_body.message}"
    else:
        assert response_body.message is None, "Expected 'message' to be None"


@pytest.mark.asyncio
async def test_successful_payment_creation(client, valid_payment_request, mock_insert_order):
    mock_insert_order(return_value=None)

    temu_response = client.post(
        "/test-emulator/payment",
        json=valid_payment_request,
        headers={"x-signature": await signature_creation(valid_payment_request)}
    )

    check_payment_response(response=temu_response, expected_status=200, expected_signature=True, error_response=False,
                           reference=True, expected_code=10, expected_message="Created successfully")


@pytest.mark.asyncio
async def test_empty_signature(client, valid_payment_request, mock_insert_order):
    mock_insert_order(return_value=None)

    temu_response = client.post(
        "/test-emulator/payment",
        json=valid_payment_request,
    )

    check_payment_response(response=temu_response, expected_status=401, expected_signature=False, error_response=True,
                           reference=False, expected_code=2, expected_message="Missing x-signature header")


@pytest.mark.asyncio
async def test_invalid_signature(client, valid_payment_request, mock_insert_order):
    mock_insert_order(return_value=None)

    temu_response = client.post(
        "/test-emulator/payment",
        json=valid_payment_request,
        headers={"x-signature": "invalid_signature"}
    )

    check_payment_response(response=temu_response, expected_status=401, expected_signature=False, error_response=True,
                           reference=False, expected_code=2, expected_message="Invalid x-signature header")


@pytest.mark.asyncio
async def test_payment_creation_case_101(client, payment_request_case_101, mock_insert_order):
    mock_insert_order(return_value=None)

    temu_response = client.post(
        "/test-emulator/payment",
        json=payment_request_case_101,
        headers={"x-signature": await signature_creation(payment_request_case_101)}

    )

    check_payment_response(response=temu_response, expected_status=200, expected_signature=True, error_response=False,
                           reference=True, expected_code=None, expected_message=None)


@pytest.mark.asyncio
async def test_payment_creation_case_102(client, payment_request_case_102, mock_insert_order):
    mock_insert_order(return_value=None)

    temu_response = client.post(
        "/test-emulator/payment",
        json=payment_request_case_102,
        headers={"x-signature": await signature_creation(payment_request_case_102)}

    )

    check_payment_response(response=temu_response, expected_status=400, expected_signature=True, error_response=False,
                           reference=False, expected_code=5, expected_message="Test error response")


@pytest.mark.asyncio
async def test_payment_creation_case_103(client, payment_request_case_103, mock_insert_order):
    mock_insert_order(return_value=None)

    temu_response = client.post(
        "/test-emulator/payment",
        json=payment_request_case_103,
        headers={"x-signature": await signature_creation(payment_request_case_103)}

    )

    check_payment_response(response=temu_response, expected_status=200, expected_signature=False, error_response=False,
                           reference=True, expected_code=10, expected_message="Created successfully")


@pytest.mark.asyncio
async def test_payment_creation_db_error(client, valid_payment_request, mock_insert_order):
    mock_insert_order(side_effect=HTTPException(
        status_code=500,
        detail={"message": f"Failed to insert data to MongoDB: Test Exception"})
    )

    temu_response = client.post(
        "/test-emulator/payment",
        json=valid_payment_request,
        headers={"x-signature": await signature_creation(valid_payment_request)}

    )

    check_payment_response(response=temu_response, expected_status=500, expected_signature=False, error_response=True,
                           reference=False, expected_code=None,
                           expected_message="Failed to insert data to MongoDB: Test Exception")

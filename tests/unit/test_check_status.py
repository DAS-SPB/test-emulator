import pytest
import json
from fastapi import HTTPException
from typing import Optional

from temu.api.signature.signature import signature_creation
from temu.api.models.check_status import CheckStatusResponseModel


def check_check_status_response(
        response: json,
        expected_status: int,
        expected_signature: bool,
        error_response: bool,
        expected_reference: Optional[str],
        expected_order_status: Optional[str],
        expected_amount: Optional[int | float],
        expected_code: Optional[int],
        expected_message: Optional[str],
):
    assert response.status_code == expected_status, f"Expected response code: {expected_status}, but got: {response.status_code}"

    if expected_signature:
        assert "x-signature" in response.headers, "Expected 'x-signature' header in response headers, but it is absent"
    else:
        assert "x-signature" not in response.headers, "Unexpected 'x-signature' header in response headers"

    response_data = response.json()

    if error_response:
        assert "detail" in response_data, "Expected 'detail' in the response body for error response"
        response_body = CheckStatusResponseModel(**response_data["detail"])
    else:
        response_body = CheckStatusResponseModel(**response_data)

    if expected_reference is not None:
        assert response_body.payment is not None, "Expected 'payment' to be present in response body"
        assert response_body.payment.reference == expected_reference, f"Expected reference: {expected_reference}, but got: {response_body.payment.reference}"
    else:
        if response_body.payment is not None:
            assert response_body.payment.reference is None, "Expected 'reference' to be None"
        else:
            assert response_body.payment is None, "Expected 'payment' to be None"

    if expected_order_status is not None:
        assert response_body.payment is not None, "Expected 'payment' to be present in response body"
        assert response_body.payment.status == expected_order_status, f"Expected response order status: {expected_order_status}, but got: {response_body.payment.status}"
    else:
        if response_body.payment is not None:
            assert response_body.payment.status is None, "Expected 'status' to be None"
        else:
            assert response_body.payment is None, "Expected 'payment' to be None"

    if expected_amount is not None:
        assert response_body.payment is not None, "Expected 'payment' to be present in response body"
        assert response_body.payment.amount == expected_amount, f"Expected response order amount: {expected_amount}, but got: {response_body.payment.amount}"
    else:
        if response_body.payment is not None:
            assert response_body.payment.amount is None, "Expected 'amount' to be None"
        else:
            assert response_body.payment is None, "Expected 'payment' to be None"

    if expected_code is not None:
        assert response_body.code == expected_code, f"Expected response code: {expected_code}, but got: {response_body.code}"
    else:
        assert response_body.code is None, "Expected 'code' to be None"

    if expected_message is not None:
        assert response_body.message == expected_message, f"Expected message: {expected_message}, but got: {response_body.message}"
    else:
        assert response_body.message is None, "Expected 'message' to be None"


@pytest.mark.asyncio
async def test_successful_check_status_request(client, valid_check_status_request, mock_find_order):
    mock_find_order(response_amount=155.22, response_status="PENDING")

    temu_response = client.post(
        "/test-emulator/check-status",
        json=valid_check_status_request,
        headers={"x-signature": await signature_creation(valid_check_status_request)}
    )

    check_check_status_response(
        response=temu_response,
        expected_status=200,
        expected_signature=True,
        error_response=False,
        expected_reference="order reference",
        expected_order_status="PENDING",
        expected_amount=155.22,
        expected_code=10,
        expected_message="Success",
    )


@pytest.mark.asyncio
async def test_empty_signature(client, valid_check_status_request, mock_find_order):
    mock_find_order()

    temu_response = client.post(
        "/test-emulator/check-status",
        json=valid_check_status_request
    )

    check_check_status_response(
        response=temu_response,
        expected_status=401,
        expected_signature=False,
        error_response=True,
        expected_reference=None,
        expected_order_status=None,
        expected_amount=None,
        expected_code=2,
        expected_message="Missing x-signature header",
    )


@pytest.mark.asyncio
async def test_invalid_signature(client, valid_check_status_request, mock_find_order):
    mock_find_order()

    temu_response = client.post(
        "/test-emulator/check-status",
        json=valid_check_status_request,
        headers={"x-signature": "invalid_signature"}
    )

    check_check_status_response(
        response=temu_response,
        expected_status=401,
        expected_signature=False,
        error_response=True,
        expected_reference=None,
        expected_order_status=None,
        expected_amount=None,
        expected_code=2,
        expected_message="Invalid x-signature header",
    )


@pytest.mark.asyncio
async def test_check_status_case_201(client, valid_check_status_request, mock_find_order):
    mock_find_order(response_amount=201, response_status="SUCCESS")

    temu_response = client.post(
        "/test-emulator/check-status",
        json=valid_check_status_request,
        headers={"x-signature": await signature_creation(valid_check_status_request)}
    )

    check_check_status_response(
        response=temu_response,
        expected_status=200,
        expected_signature=True,
        error_response=False,
        expected_reference=None,
        expected_order_status="SUCCESS",
        expected_amount=201,
        expected_code=None,
        expected_message=None,
    )


@pytest.mark.asyncio
async def test_check_status_case_202(client, valid_check_status_request, mock_find_order):
    mock_find_order(response_amount=202, response_status=None)

    temu_response = client.post(
        "/test-emulator/check-status",
        json=valid_check_status_request,
        headers={"x-signature": await signature_creation(valid_check_status_request)}
    )

    check_check_status_response(
        response=temu_response,
        expected_status=400,
        expected_signature=True,
        error_response=False,
        expected_reference=None,
        expected_order_status=None,
        expected_amount=None,
        expected_code=5,
        expected_message="Test error response",
    )


@pytest.mark.asyncio
async def test_check_status_case_203(client, valid_check_status_request, mock_find_order):
    mock_find_order(response_amount=203, response_status="SUCCESS")

    temu_response = client.post(
        "/test-emulator/check-status",
        json=valid_check_status_request,
        headers={"x-signature": await signature_creation(valid_check_status_request)}
    )

    check_check_status_response(
        response=temu_response,
        expected_status=200,
        expected_signature=False,
        error_response=False,
        expected_reference="order reference",
        expected_order_status="SUCCESS",
        expected_amount=203,
        expected_code=10,
        expected_message="Success",
    )


@pytest.mark.asyncio
async def test_check_status_db_error(client, valid_check_status_request, mock_find_order):
    mock_find_order(side_effect=HTTPException(
        status_code=500,
        detail={"message": f"Failed to fetch data from MongoDB: Test Exception"})
    )

    temu_response = client.post(
        "/test-emulator/check-status",
        json=valid_check_status_request,
        headers={"x-signature": await signature_creation(valid_check_status_request)}
    )

    check_check_status_response(
        response=temu_response,
        expected_status=500,
        expected_signature=False,
        error_response=True,
        expected_reference=None,
        expected_order_status=None,
        expected_amount=None,
        expected_code=None,
        expected_message="Failed to fetch data from MongoDB: Test Exception",
    )

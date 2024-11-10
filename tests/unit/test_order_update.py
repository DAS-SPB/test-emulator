import pytest
from fastapi import HTTPException


@pytest.mark.asyncio
async def test_successful_update_order_request(client, valid_update_order_request, mock_update_order):
    update_order = mock_update_order(request_amount=150.20, request_status="SUCCESS")

    temu_response = client.post(
        "/test-emulator/update-order",
        json=valid_update_order_request,
        headers={}
    )

    update_order.assert_called_once()

    assert temu_response.status_code == 200

    response_json = temu_response.json()
    assert response_json.get("order_id") == "12345"
    assert response_json.get("message") == "Order updated successfully"
    assert "x-signature" not in temu_response.headers


@pytest.mark.asyncio
async def test_update_order_db_error_case_1(client, valid_update_order_request, mock_update_order):
    update_order = mock_update_order(side_effect=HTTPException(
        status_code=500,
        detail={"message": f"Failed to update data in MongoDB: Test Exception"})
    )

    temu_response = client.post(
        "/test-emulator/update-order",
        json=valid_update_order_request,
        headers={}
    )

    update_order.assert_called_once()

    assert temu_response.status_code == 500

    response_json = temu_response.json()
    assert response_json.get("detail").get("message") == "Failed to update data in MongoDB: Test Exception"
    assert "x-signature" not in temu_response.headers


@pytest.mark.asyncio
async def test_update_order_db_error_case_2(client, valid_update_order_request, mock_update_order):
    update_order = mock_update_order(side_effect=HTTPException(
        status_code=404, detail={"message": "Order not found"})
    )

    temu_response = client.post(
        "/test-emulator/update-order",
        json=valid_update_order_request,
        headers={}
    )

    update_order.assert_called_once()

    assert temu_response.status_code == 404

    response_json = temu_response.json()
    assert response_json.get("detail").get("message") == "Order not found"
    assert "x-signature" not in temu_response.headers

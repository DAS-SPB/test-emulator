# import pytest
# from unittest.mock import patch
# from temu.api.models.callback import CallbackRequestModel
#
#
# @pytest.mark.asyncio
# @patch("temu.api.signature.signature.signature_creation")
# @patch("httpx.AsyncClient.post")
# async def test_successful_callback_request(mock_post, mock_signature_creation, mock_find_order, client):
#     found_order = mock_find_order(response_amount=188.10, response_status="SUCCESS")
#
#     mock_signature_creation.return_value = "generated_signature"
#     mock_post.return_value.status_code = 200
#
#     request_data = CallbackRequestModel(order_id="123456789").model_dump()
#
#     temu_response = client.post(
#         "/test-emulator/callback-request",
#         json=request_data
#     )
#
#     assert temu_response.status_code == 200
#     assert temu_response.json().get("message") == "Callback request successfully sent"
#
#     found_order.assert_called_once()
#     mock_signature_creation.assert_called_once()
#     mock_post.assert_called_once_with(
#         url="https://webhook.site/94385313-18e0-4617-99dd-db78a2f86081",
#         json={
#             "payment": {
#                 "reference": "order reference",
#                 "status": "SUCCESS",
#                 "amount": 188.10
#             },
#             "code": 10,
#             "message": "Callback"
#         },
#         headers={"x-signature": "generated_signature"}
#     )
#
#
# @pytest.mark.asyncio
# @patch("temu.api.callback.database.find_order")
# @patch("httpx.AsyncClient.post")
# async def test_callback_request_error_case(mock_post, mock_find_order):
#     mock_find_order.return_value = {
#         "reference": "",
#         "status": "FAILED",
#         "callback_url": "https://callback.url",
#         "data": {
#             "amount": 301
#         }
#     }
#
#     mock_post.return_value.status_code = 500
#
#     request_data = CallbackRequestModel(order_id="123456789")
#
#     with pytest.raises(HTTPException) as exc_info:
#         await callback_request(request_data)
#
#     assert exc_info.value.status_code == 500
#     assert "Callback request failed with status code 500" in exc_info.value.detail
#     mock_find_order.assert_called_once()
#     mock_post.assert_called_once()
#
#
# @pytest.mark.asyncio
# @patch("temu.api.callback.database.find_order")
# @patch("temu.api.callback.signature_creation")
# @patch("httpx.AsyncClient.post")
# async def test_callback_request_unsigned(mock_post, mock_signature_creation, mock_find_order):
#     mock_find_order.return_value = {
#         "reference": "order reference",
#         "status": "SUCCESS",
#         "callback_url": "https://callback.url",
#         "data": {
#             "amount": 302
#         }
#     }
#
#     mock_signature_creation.return_value = "generated_signature"
#     mock_post.return_value.status_code = 200
#
#     request_data = CallbackRequestModel(order_id="123456789")
#
#     response = await callback_request(request_data)
#
#     assert response.message == "Callback request successfully sent"
#     mock_find_order.assert_called_once()
#     mock_signature_creation.assert_not_called()
#     mock_post.assert_called_once_with(
#         url="https://callback.url",
#         json={
#             "payment": {
#                 "reference": "order reference",
#                 "status": "SUCCESS",
#                 "amount": 150.20
#             },
#             "code": 10,
#             "message": "Success"
#         },
#         headers={}
#     )

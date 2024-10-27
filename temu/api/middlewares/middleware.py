from fastapi import Request, Response
from fastapi.responses import JSONResponse
from pydantic_core import ValidationError
import hashlib
import hmac
import json

from temu.settings.config import settings
from ..models.payment import PaymentRequestModel

SECRET_KEY = settings.SECRET_KEY
skip_signature_amount = {105, 205}

excluded_endpoints: set[str] = {
    "/update-order",
    "/send-callback"
}


# async def signature_verification(request: Request, call_next):
#     body = await request.body()
#
#     if request.url.path not in excluded_endpoints:
#         x_signature = request.headers.get("x-signature")
#         if not x_signature:
#             return JSONResponse(status_code=401, content={"message": "Missing x-signature header"})
#
#         try:
#             body_dict = json.loads(body)
#             body_str = json.dumps(body_dict, sort_keys=True, separators=(",", ":"))
#         except json.JSONDecodeError:
#             return JSONResponse(status_code=400, content={"message": "Invalid JSON format in request body"})
#
#         signature = hmac.new(SECRET_KEY.encode(), body_str.encode(), hashlib.sha256).hexdigest()
#
#         if not hmac.compare_digest(signature, x_signature):
#             return JSONResponse(status_code=401, content={"message": "Invalid x-signature header"})
#
#     response = await call_next(request)
#
#     if request.url.path not in excluded_endpoints:
#
#         payment_request_amount = PaymentRequestModel.parse_raw(body).data.amount
#
#         if payment_request_amount not in skip_signature_amount:
#             response_body = b"".join([chunk async for chunk in response.body_iterator])
#             response.headers["x-signature"] = hmac.new(SECRET_KEY.encode(), response_body, hashlib.sha256).hexdigest()
#             response = Response(content=response_body, status_code=response.status_code, headers=response.headers)
#
#     return response


# async def signature_verification(request: Request, call_next):
#     body = await request.body()
#
#     if request.url.path not in excluded_endpoints:
#         x_signature = request.headers.get("x-signature")
#         if not x_signature:
#             return JSONResponse(status_code=401, content={"message": "Missing x-signature header"})
#
#         signature = hmac.new(SECRET_KEY.encode(), "message".encode(), hashlib.sha256).hexdigest()
#
#         if not hmac.compare_digest(signature, x_signature):
#             return JSONResponse(status_code=401, content={"message": "Invalid x-signature header"})
#
#     response = await call_next(request)


# async def response_sign(request: Request, response: Response):
#     if request.url.path not in excluded_endpoints:
#
#         try:
#             payment_request_amount = PaymentRequestModel.parse_raw(body).data.amount
#         except (ValidationError, json.JSONDecodeError):
#             return JSONResponse(status_code=400, content={"message": "Invalid request body"})
#
#         if payment_request_amount not in skip_signature_amount:
#             response_body = b"".join([chunk async for chunk in response.body_iterator])
#             response.headers["x-signature"] = hmac.new(SECRET_KEY.encode(), "message".encode(),
#                                                        hashlib.sha256).hexdigest()
#             response = Response(content=response_body, status_code=response.status_code, headers=response.headers)
#
#     return response

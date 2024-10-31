from fastapi import Request, HTTPException
import hashlib
import hmac

from temu.settings.config import settings
from ..models.payment import PaymentResponseModel

SECRET_KEY = settings.SECRET_KEY


async def signature_verification(request: Request):
    x_signature = request.headers.get("x-signature")
    if not x_signature:
        response = PaymentResponseModel(code=2, message="Missing x-signature header")
        raise HTTPException(status_code=401, detail=response.dict())

    request_body: bytes = await request.body()
    signature = hmac.new(SECRET_KEY.encode(), request_body, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(signature, x_signature):
        response = PaymentResponseModel(code=2, message="Invalid x-signature header")
        raise HTTPException(status_code=401, detail=response.dict())


async def signature_creation(response_body: bytes) -> str:
    return hmac.new(SECRET_KEY.encode(), response_body, hashlib.sha256).hexdigest()

from fastapi import Request, HTTPException
import hashlib
import hmac
import json
import logging

from temu.settings.config import settings
from ..models.payment import PaymentResponseModel

SECRET_KEY = settings.SECRET_KEY
logger = logging.getLogger(__name__)


async def signature_verification(request: Request):
    x_signature = request.headers.get("x-signature")
    if not x_signature:
        response = PaymentResponseModel(code=2, message="Missing x-signature header")
        logger.error(f"Missing x-signature header in incoming request")

        raise HTTPException(status_code=401, detail=response.dict())

    request_body = await request.json()
    signature = await signature_creation(request_body)

    if not hmac.compare_digest(signature, x_signature):
        response = PaymentResponseModel(code=2, message="Invalid x-signature header")
        logger.error(f"Invalid x-signature header in incoming request")

        raise HTTPException(status_code=401, detail=response.dict())


async def signature_creation(response_body: dict) -> str:
    return hmac.new(SECRET_KEY.encode(), json.dumps(response_body, separators=(',', ':')).encode('utf-8'),
                    hashlib.sha256).hexdigest()

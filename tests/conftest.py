import pytest
from fastapi.testclient import TestClient

from main import temu
from temu.api.models.payment import PaymentRequestModel, DataModel, CurrencyEnum, CustomerModel, SubclassEnum


@pytest.fixture
def client():
    return TestClient(temu)


@pytest.fixture
def valid_payment_request():
    return PaymentRequestModel(
        order_id="12345",
        data=DataModel(amount=100.0, currency=CurrencyEnum.currency),
        customer=[
            CustomerModel(full_name="John Doe", email="johndoe@example.com"),
            CustomerModel(full_name="Jane Smith", email="janesmith@example.com"),
        ],
        subclass=SubclassEnum.subclass,
        callback_url="https://example.com/callback"
    )

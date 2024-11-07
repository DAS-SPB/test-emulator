import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock

from main import temu
from temu.api.models.payment import PaymentRequestModel, DataModel, CurrencyEnum, CustomerModel, SubclassEnum


@pytest.fixture
def client():
    return TestClient(temu)


@pytest.fixture
def mock_insert_order(mocker):
    def _mock_insert_order(return_value=None, side_effect=None):
        mock_insert = mocker.patch("temu.db.database.insert_order", new_callable=AsyncMock)
        if side_effect is not None:
            mock_insert.side_effect = side_effect
        else:
            mock_insert.return_value = return_value
        return mock_insert

    return _mock_insert_order


@pytest.fixture
def valid_payment_request():
    return PaymentRequestModel(
        order_id="12345",
        data=DataModel(amount=100.22, currency=CurrencyEnum.currency),
        customer=[
            CustomerModel(full_name="John Doe", email="johndoe@example.com")
        ],
        subclass=SubclassEnum.subclass,
        callback_url="https://example.com/callback"
    ).model_dump()


@pytest.fixture
def payment_request_case_101():
    return PaymentRequestModel(
        order_id="12345",
        data=DataModel(amount=101, currency=CurrencyEnum.currency),
        customer=[
            CustomerModel(full_name="John Doe", email="johndoe@example.com")
        ],
        subclass=SubclassEnum.subclass,
        callback_url="https://example.com/callback"
    ).model_dump()


@pytest.fixture
def payment_request_case_102():
    return PaymentRequestModel(
        order_id="12345",
        data=DataModel(amount=102, currency=CurrencyEnum.currency),
        customer=[
            CustomerModel(full_name="John Doe", email="johndoe@example.com")
        ],
        subclass=SubclassEnum.subclass,
        callback_url="https://example.com/callback"
    ).model_dump()


@pytest.fixture
def payment_request_case_103():
    return PaymentRequestModel(
        order_id="12345",
        data=DataModel(amount=103, currency=CurrencyEnum.currency),
        customer=[
            CustomerModel(full_name="John Doe", email="johndoe@example.com")
        ],
        subclass=SubclassEnum.subclass,
        callback_url="https://example.com/callback"
    ).model_dump()

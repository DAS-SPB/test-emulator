import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock

from main import temu
from temu.api.models.payment import PaymentRequestModel, DataModel, CurrencyEnum, CustomerModel, SubclassEnum
from temu.api.models.check_status import CheckStatusRequestModel, SubclassEnum


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


@pytest.fixture
def mock_find_order(mocker):
    def _mock_find_order(response_amount=None, response_status=None, side_effect=None):
        mock_find = mocker.patch("temu.db.database.find_order", new_callable=AsyncMock)
        if side_effect is not None:
            mock_find.side_effect = side_effect
        else:
            mock_find.return_value = {
                "_id": {"$oid": "673092eacc53dc3ccf5cb758"},
                "order_id": "12345",
                "data": {
                    "amount": response_amount,
                    "currency": "EUR"
                },
                "customer": [
                    {
                        "full_name": "Fool Name",
                        "email": "email@email.com"
                    }
                ],
                "subclass": "subclass",
                "callback_url": "https://example.com/callback",
                "reference": "order reference",
                "status": response_status
            }
        return mock_find

    return _mock_find_order


@pytest.fixture
def valid_check_status_request():
    return CheckStatusRequestModel(
        order_id="12345",
        subclass=SubclassEnum.subclass
    ).model_dump()

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

@pytest.fixture(scope="module")
def client():
    return TestClient(app)

@pytest.fixture(scope="function")
def mock_stripe():
    with patch("app.services.stripe_service.stripe") as mock_stripe_lib:
        yield mock_stripe_lib

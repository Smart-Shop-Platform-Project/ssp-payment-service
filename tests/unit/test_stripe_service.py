import pytest
from unittest.mock import patch
from app.services.stripe_service import StripeService
import stripe

# Dummy settings for testing
class DummySettings:
    STRIPE_SECRET_KEY = "sk_test_dummy"
    STRIPE_WEBHOOK_SECRET = "whsec_dummy"

@pytest.fixture
def stripe_service(mock_stripe):
    with patch("app.services.stripe_service.settings", DummySettings()):
        return StripeService()

def test_create_payment_intent(stripe_service, mock_stripe):
    # Setup
    mock_stripe.PaymentIntent.create.return_value = {"client_secret": "pi_123_secret_456"}

    # Execute
    result = stripe_service.create_payment_intent(1000, "usd", "order_abc")

    # Assert
    assert result["client_secret"] == "pi_123_secret_456"
    mock_stripe.PaymentIntent.create.assert_called_once_with(
        amount=1000,
        currency="usd",
        automatic_payment_methods={'enabled': True},
        metadata={'order_id': 'order_abc'}
    )

def test_construct_webhook_event_success(stripe_service, mock_stripe):
    # Setup
    payload = b'{"id": "evt_123"}'
    sig_header = "t=123,v1=abc"
    mock_stripe.Webhook.construct_event.return_value = {"id": "evt_123", "type": "payment_intent.succeeded"}

    # Execute
    event = stripe_service.construct_webhook_event(payload, sig_header)

    # Assert
    assert event["id"] == "evt_123"
    mock_stripe.Webhook.construct_event.assert_called_once_with(
        payload, sig_header, DummySettings.STRIPE_WEBHOOK_SECRET
    )

def test_construct_webhook_event_invalid_signature(stripe_service, mock_stripe):
    # Setup
    mock_stripe.Webhook.construct_event.side_effect = stripe.error.SignatureVerificationError("Invalid signature", "sig")

    # Execute and Assert
    with pytest.raises(stripe.error.SignatureVerificationError):
        stripe_service.construct_webhook_event(b'{}', "bad_header")

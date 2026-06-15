import pytest
from unittest.mock import patch, AsyncMock
from app.services.stripe_service import StripeService

def test_create_payment_intent_api(client):
    with patch.object(StripeService, 'create_payment_intent') as mock_create:
        mock_create.return_value = {"client_secret": "pi_integration_secret"}
        
        response = client.post(
            "/api/v1/create-payment-intent",
            json={"amount": 2500, "order_id": "order_int_1"}
        )
        
        assert response.status_code == 200
        assert response.json() == {"clientSecret": "pi_integration_secret"}
        mock_create.assert_called_once_with(amount=2500, currency="usd", order_id="order_int_1")

def test_stripe_webhook_success(client):
    with patch.object(StripeService, 'construct_webhook_event') as mock_construct:
        # Simulate a successful payment intent event
        mock_construct.return_value = {
            "type": "payment_intent.succeeded",
            "data": {
                "object": {
                    "metadata": {"order_id": "order_int_webhook_1"}
                }
            }
        }
        
        # The webhook endpoint expects a raw body and a stripe-signature header
        response = client.post(
            "/api/v1/webhook",
            content=b'{"dummy": "payload"}',
            headers={"stripe-signature": "dummy_sig"}
        )
        
        assert response.status_code == 200
        assert response.json() == {"success": True}
        mock_construct.assert_called_once()

def test_stripe_webhook_missing_signature(client):
    # No signature header provided
    response = client.post(
        "/api/v1/webhook",
        content=b'{"dummy": "payload"}'
    )
    
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing Stripe signature"}

def test_health_check(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "SSP Payment Service is running", "status": "healthy"}

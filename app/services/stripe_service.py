import stripe
from ..core.config import settings
import logging

logger = logging.getLogger("ssp-payment-service")

class StripeService:
    def __init__(self):
        stripe.api_key = settings.STRIPE_SECRET_KEY

    def create_payment_intent(self, amount: int, currency: str, order_id: str):
        try:
            logger.info(f"Creating payment intent for order: {order_id}")
            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency=currency,
                automatic_payment_methods={'enabled': True},
                metadata={'order_id': order_id}
            )
            return intent
        except Exception as e:
            logger.error(f"Error creating payment intent for order {order_id}: {e}")
            raise

    def construct_webhook_event(self, payload, sig_header):
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
            return event
        except ValueError as e:
            logger.warning(f"Invalid webhook payload: {e}")
            raise
        except stripe.error.SignatureVerificationError as e:
            logger.warning(f"Invalid webhook signature: {e}")
            raise

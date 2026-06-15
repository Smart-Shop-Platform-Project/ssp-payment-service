from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from ..services.stripe_service import StripeService
import logging

logger = logging.getLogger("ssp-payment-service")

router = APIRouter()
stripe_service = StripeService()

class PaymentIntentRequest(BaseModel):
    amount: int
    currency: str = "usd"
    order_id: str

@router.post("/create-payment-intent", tags=["Payments"])
async def create_payment_intent(request: PaymentIntentRequest):
    try:
        intent = stripe_service.create_payment_intent(
            amount=request.amount,
            currency=request.currency,
            order_id=request.order_id
        )
        return {"clientSecret": intent['client_secret']}
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))

@router.post("/webhook", tags=["Payments"])
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    if not sig_header:
        raise HTTPException(status_code=400, detail="Missing Stripe signature")

    try:
        event = stripe_service.construct_webhook_event(payload, sig_header)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        order_id = payment_intent.get('metadata', {}).get('order_id')
        logger.info(f"Payment for order {order_id} succeeded.")
        # Typically you'd publish a Kafka event here
    else:
        logger.info(f"Unhandled Stripe event type: {event['type']}")
    
    return {"success": True}

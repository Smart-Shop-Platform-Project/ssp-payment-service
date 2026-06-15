# SSP Payment Service

This service securely handles financial transactions for the Smart Shop Platform. It acts as an integration layer between the internal order system and external payment gateways (like Stripe).

## Core Responsibilities & Features

1.  **Payment Intent Creation:**
    *   Provides an endpoint (`/api/v1/create-payment-intent`) to initiate a transaction.
    *   It communicates securely with the Stripe API to create a `PaymentIntent`, returning a `clientSecret` that the frontend UI uses to securely collect credit card details directly to Stripe, keeping sensitive PCI data out of our systems.

2.  **Webhook Processing & Event Publishing:**
    *   Provides a secure `/api/v1/webhook` endpoint that Stripe calls asynchronously when a payment succeeds or fails.
    *   The service strictly validates the webhook signature using a secret stored in AWS SSM to ensure the request is genuinely from Stripe.
    *   Upon successful payment verification, the service publishes an event (e.g., `payment_completed`) to the Kafka event bus. The Order Service listens for this event to finalize the order status.

## Architecture
- **Framework:** **FastAPI** (using Mangum for Lambda execution)
- **Deployment:** **AWS Lambda** (Container Image)
- **External Integration:** **Stripe** API
- **Dependencies:**
    - `stripe`: The official Stripe Python SDK.
    - `boto3`: To fetch API keys securely from AWS SSM Parameter Store.
    - `mangum`: To run the FastAPI application within an AWS Lambda environment.

## Security Posture
- Stripe API keys (`STRIPE_SECRET_KEY`) and Webhook secrets (`STRIPE_WEBHOOK_SECRET`) are **never** hardcoded. They are fetched at runtime from AWS Systems Manager (SSM) Parameter Store.
- The service does not process or store raw credit card numbers.

## Local Development

1.  Create a virtual environment: `python3 -m venv venv`
2.  Activate it: `source venv/bin/activate`
3.  Install dependencies: `pip install -r requirements.txt` and `pip install -r requirements-dev.txt`
4.  **Configuration:** You will need test API keys from a Stripe Developer account to test the integration locally.
5.  Run the application:
    ```bash
    uvicorn app.main:app --reload --port 8007
    ```

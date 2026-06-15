from pydantic_settings import BaseSettings
import os
import boto3
import logging

logger = logging.getLogger("ssp-payment-service")

def get_ssm_parameter(name, region):
    try:
        ssm_client = boto3.client('ssm', region_name=region)
        parameter = ssm_client.get_parameter(Name=name, WithDecryption=True)
        return parameter['Parameter']['Value']
    except Exception as e:
        logger.critical(f"Error fetching parameter {name}: {e}")
        raise

class Settings(BaseSettings):
    AWS_REGION: str = os.environ.get("AWS_REGION", "us-east-1")
    STRIPE_SECRET_KEY_NAME: str = os.environ.get("STRIPE_SECRET_KEY_NAME", "/ssp/payment/stripe_secret_key")
    STRIPE_WEBHOOK_SECRET_NAME: str = os.environ.get("STRIPE_WEBHOOK_SECRET_NAME", "/ssp/payment/stripe_webhook_secret")
    
    STRIPE_SECRET_KEY: str = ""
    STRIPE_WEBHOOK_SECRET: str = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            self.STRIPE_SECRET_KEY = get_ssm_parameter(self.STRIPE_SECRET_KEY_NAME, self.AWS_REGION)
            self.STRIPE_WEBHOOK_SECRET = get_ssm_parameter(self.STRIPE_WEBHOOK_SECRET_NAME, self.AWS_REGION)
        except Exception:
             self.STRIPE_SECRET_KEY = "sk_test_..."
             self.STRIPE_WEBHOOK_SECRET = "whsec_..."

settings = Settings()

from fastapi import FastAPI
import logging
import sys
from .api.payment_routes import router as payment_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='{"time":"%(asctime)s", "level":"%(levelname)s", "message":"%(message)s"}',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("ssp-payment-service")

app = FastAPI(title="SSP Payment Service")

app.include_router(payment_router, prefix="/api/v1")

@app.get("/", tags=["Health Check"])
async def root():
    return {"message": "SSP Payment Service is running"}

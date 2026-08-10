from fastapi import FastAPI

from app.routes.transactions import router as transactions_router
from app.routes.rewards import router as rewards_router
from app.routes.coin_balance import router as coin_balance_router


app = FastAPI(
    title="Digital Alpha Dashboard API",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Digital Alpha Dashboard API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


app.include_router(transactions_router)
app.include_router(rewards_router)
app.include_router(coin_balance_router)
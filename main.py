from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

import schemas

app = FastAPI(title="heitor-stone-challenge", version="0.0.1", redoc_url=None)

@app.get("/")
async def root():
    return {"message": "Welcome to Heitor Stone Challenge API"}

@app.get(
    "/ticker",
    response_model=schemas.StockQuotes,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "No phone found for received query string"},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "Failed to validate received query string"},
        status.HTTP_503_SERVICE_UNAVAILABLE: {
            "description": "Database is down or something weird happened with connection"
        },
    },
)
async def get_by_ticker():
    pass

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.stock_quotes import StockQuotesRepository
from dependencies.database import get_database_session

import schemas

app = FastAPI(title="heitor-stone-challenge", version="0.0.1", redoc_url=None)

@app.get("/")
async def root():
    return {"message": "Welcome to Heitor Stone Challenge API"}

@app.get(
    "/ticker/{ticker_name}",
)
async def get_by_ticker(ticker_name: str, session: AsyncSession = Depends(get_database_session)):

    stock_quotes_repository = StockQuotesRepository(session)

    found_stocks = await stock_quotes_repository.get_stock_quotes_by_ticker(ticker_name)

    return found_stocks


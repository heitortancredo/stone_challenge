from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session
from repositories.stock_quotes import StockQuotesRepository
from dependencies.database import get_database_session
from starlette import status

import schemas

app = FastAPI(title="heitor-stone-challenge", version="0.0.1", redoc_url=None)

@app.get("/")
async def root():
    return {"message": "Welcome to Heitor Stone Challenge API"}

@app.get(
    "/ticker/{ticker_name}",
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "No ticker found for received query string"},
        status.HTTP_503_SERVICE_UNAVAILABLE: {
            "description": "Database is down or something weird happened with connection"
        },
    },
)
async def get_stock_quotes(
        ticker_name: str,
        deal_date: str | None,
        session: Session = Depends(get_database_session)
):
    try:
        stock_quotes_repository = StockQuotesRepository(session)
        found_stocks = stock_quotes_repository.get_stock_quotes(ticker_name, deal_date=deal_date)

        if found_stocks:
            return found_stocks
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    except OperationalError:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE)

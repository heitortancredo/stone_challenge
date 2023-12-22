import sqlalchemy
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, and_
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from sqlalchemy.sql.expression import func, over

from models import StockQuotes

class StockQuotesRepository:
    def __init__(self, database: Session):
        self.__database = database

    def get_stock_quotes(self, ticker: str | None, query_parameters: str | None = None):
        return self.__get_stock_quotes_by_ticker(ticker)

    def __get_stock_quotes_by_ticker(self, ticker: str | None) -> dict:

        max_range_value = (self.__database.query(
            StockQuotes.id,
            StockQuotes.preco_negocio
        ).filter(StockQuotes.ticker == ticker)
                           .order_by(StockQuotes.preco_negocio.desc()).limit(1).subquery())

        result = self.__database.query(
            StockQuotes
        ).filter(StockQuotes.id == max_range_value.c.id)

        return jsonable_encoder(result.all())
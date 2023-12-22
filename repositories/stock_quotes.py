from typing import Optional, List, Any, Sequence

from sqlalchemy import Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models import StockQuotes


class StockQuotesRepository:
    def __init__(self, database: AsyncSession):
        self.__database = database

    async def get_stock_quotes(self, ticker: str | None, query_parameters: str | None = None):
        return await self.__get_stock_quotes_by_ticker(ticker)

    async def __get_stock_quotes_by_ticker(self, ticker: str | None) -> Sequence[RowMapping]:
        # query = select(StockQuotes, func.max(StockQuotes.preco_negocio)).over(partition_by=StockQuotes.ticker,
        #                                                                       order_by=StockQuotes.preco_negocio)
        query = (
            select(StockQuotes)
            .where(StockQuotes.ticker == ticker)
        )

        result = await self.__database.execute(query)

        return result.mappings().all()

    async def get_stock_quotes_by_date(self, stock_quote_date: str) -> Optional[StockQuotes]:
        query = (
            select(StockQuotes)
            .where(StockQuotes.data_negocio == stock_quote_date)
        )

        result = await self.__database.execute(query)

        return result.scalars().first()

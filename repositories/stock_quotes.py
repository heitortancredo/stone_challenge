from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import models


class StockQuotesRepository:
    def __init__(self, database: AsyncSession):
        self.__database = database

    async def get_stock_quotes_by_ticker(self, ticker: str) -> Optional[models.StockQuotes]:
        query = (
            select(models.StockQuotes)
            .where(models.StockQuotes.ticker == ticker)
        )

        result = await self.__database.execute(query)

        return result.scalars().first()

    async def get_stock_quotes_by_date(self, stock_quote_date: str) -> Optional[models.StockQuotes]:
        query = (
            select(models.StockQuotes)
            .where(models.StockQuotes.data_negocio == stock_quote_date)
        )

        result = await self.__database.execute(query)

        return result.scalars().first()

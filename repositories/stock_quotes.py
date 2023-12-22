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

    def get_stock_quotes(self, ticker: str | None, deal_date: str | None = None) -> dict:
        return self.__get_stock_quotes_by_ticker(ticker, deal_date)

    def __get_stock_quotes_by_ticker(self, ticker: str | None, deal_date: str | None) -> dict:
        
        query = text(f"""
            with 
                total_deals as (
                    select 
                        sq1.data_negocio,
                        sq1.ticker, SUM(quantidade_negociada) as max_daily_volume
                    from 
                        stock_quotes sq1
                    where 
                        sq1.data_negocio >= '2023-12-07' and sq1.ticker = '{ticker}' 
                    group by 
                        sq1.data_negocio, sq1.ticker 
                    order by 
                        max_daily_volume 
                    desc limit 1
                ),
                max_price as (
                    select 
                        sq2.ticker, sq2.preco_negocio as max_range_value
                    from 
                        stock_quotes sq2 
                    where
                        sq2.ticker = '{ticker}' 
                    group by 
                        sq2.ticker, max_range_value 
                    order by 
                        max_range_value
                    desc limit 1
                ),
                results as (
                    select 
                        total_deals.ticker, max_range_value, max_daily_volume 
                    from 
                        total_deals 
                    join 
                        max_price on max_price.ticker = total_deals.ticker
                )
                select * from results
            """)

        result = self.__database.execute(query)

        return result.mappings().all()
        
    #     max_range_value = (self.__database.query(
    #         StockQuotes.id,
    #         StockQuotes.preco_negocio
    #     ).filter(StockQuotes.ticker == ticker)
    #                        .order_by(StockQuotes.preco_negocio.desc()).limit(1).subquery())

    #     result = self.__database.query(
    #         StockQuotes
    #     ).filter(StockQuotes.id == max_range_value.c.id)

    #     return jsonable_encoder(result.all())

    def get_highest_number_of_deals(self, start_date: str | None) -> dict:
        if start_date:
            pass

        all_stock = self.__database.query(StockQuotes)

from sqlalchemy import RowMapping, TextClause  # type: ignore
from sqlalchemy.orm import Session
from sqlalchemy.sql import text


class StockQuotesRepository:
    def __init__(self, database: Session):
        self.__database = database

    def get_stock_quotes(self, ticker: str, deal_date: str | None = None) -> RowMapping:
        query = self.__build_query(ticker, deal_date)

        return self.__database.execute(query).mappings().first()

    @staticmethod
    def __build_query(ticker: str, start_date: str | None) -> TextClause:
        where_clause_with_data = text(f"""ticker = '{ticker}' and data_negocio >= '{start_date}'""")
        where_clause = text(f"""ticker = '{ticker}'""")

        query = text(
            f"""
            with
                total_deals as (
                    select
                        sq1.data_negocio,
                        sq1.ticker,
                        SUM(quantidade_negociada) as max_daily_volume
                    from
                        stock_quotes sq1
                    where
                        {where_clause_with_data if start_date else where_clause}
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
                        {where_clause}
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
            """
        )

        return query

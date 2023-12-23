from sqlalchemy import Integer, BigInteger, Column, DateTime, Index, String, Float
from sqlalchemy.dialects import sqlite
from sqlalchemy.orm import declarative_base

BaseModel = declarative_base()
BigIntegerType = BigInteger().with_variant(sqlite.INTEGER, "sqlite")


class StockQuotes(BaseModel):
    __tablename__ = "stock_quotes"

    id = Column(BigIntegerType, primary_key=True, autoincrement=True)
    ticker = Column(String(length=128), nullable=False)
    hora_fechamento = Column(String(length=128), nullable=False)
    preco_negocio = Column(Float, nullable=False)
    quantidade_negociada = Column(Integer, nullable=False)
    data_negocio = Column(DateTime, nullable=True, default=None)

    __table_args__ = (
        Index("ticker", ticker, postgresql_using="hash"),
        Index("data_negocio", data_negocio, postgresql_using="btree"),
        Index("ticker_data_negocio", ticker, data_negocio)

    )
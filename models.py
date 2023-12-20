from sqlalchemy import JSON, Integer, BigInteger, Column, DateTime, Index, String
from sqlalchemy.dialects import sqlite
from sqlalchemy.orm import declarative_base

BaseModel = declarative_base()
BigIntegerType = BigInteger().with_variant(sqlite.INTEGER, "sqlite")


class StockQuotes(BaseModel):
    __tablename__ = "stock_quotes"

    id = Column(BigIntegerType, primary_key=True, autoincrement=True)
    ticker = Column(String(length=128), nullable=False)
    hora_fechamento = Column(String(length=128), nullable=False)
    preco_negocio = Column(Integer, nullable=False)
    quantidade_negociada = Column(Integer, nullable=False)
    data_negocio = Column(DateTime, nullable=True, default=None)

    __table_args__ = (
        Index("ticker", ticker),
        Index("data_negocio", data_negocio),
    )
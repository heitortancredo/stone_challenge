from datetime import datetime

from pydantic import BaseModel


class StockQuotes(BaseModel):
    ticker: str
    hora_fechamento: str
    preco_negocio: int
    quantidade_negociada: int
    data_negocio: datetime

    class Config:
        from_attributes = True


class GetStockQuotesQueryString(BaseModel):
    deal_date: str

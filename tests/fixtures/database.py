import pytest
from datetime import date

from sqlalchemy import insert
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import Session, sessionmaker

from models import BaseModel, StockQuotes


@pytest.fixture
def initialized_database() -> Session:
    engine = create_engine("sqlite://")
    session_maker = sessionmaker(engine)

    with engine.begin() as connection:
        BaseModel.metadata.create_all(bind=engine)

        with session_maker() as session:
            yield session

        BaseModel.metadata.drop_all(bind=engine)

@pytest.fixture
def initialize_database_with_stock_quotes(initialized_database):

    insert_stmt1 = insert(StockQuotes).values(
        id=1,
        ticker="TST1",
        hora_fechamento="123213",
        preco_negocio=1122.23,
        quantidade_negociada=44,
        data_negocio=date(2023, 12, 7)
    )
    insert_stmt2 = insert(StockQuotes).values(
        id=2,
        ticker="TST1",
        hora_fechamento="567889",
        preco_negocio=23.23,
        quantidade_negociada=7,
        data_negocio=date(2023, 12, 8)
    )
    insert_stmt3 = insert(StockQuotes).values(
        id=3,
        ticker="TST1",
        hora_fechamento="436563",
        preco_negocio=232.23,
        quantidade_negociada=17,
        data_negocio=date(2023, 12, 8)
    )
    insert_stmt4 = insert(StockQuotes).values(
        id=4,
        ticker="TST2",
        hora_fechamento="1245677",
        preco_negocio=212.23,
        quantidade_negociada=172,
        data_negocio=date(2023, 12, 8)
    )

    initialized_database.execute(insert_stmt1)
    initialized_database.execute(insert_stmt2)
    initialized_database.execute(insert_stmt3)
    initialized_database.execute(insert_stmt4)
    initialized_database.commit()

    return initialized_database

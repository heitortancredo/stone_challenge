import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import Session
from sqlalchemy.types import DateTime, Float, Integer, String

from configs import DATABASE_HOSTNAME, DATABASE_NAME, DATABASE_PASSWORD, DATABASE_TABLE, DATABASE_USERNAME

STOCK_QUOTES_FILES = [
    # "sample.csv"
    "07-12-2023_NEGOCIOSAVISTA.csv",
    "08-12-2023_NEGOCIOSAVISTA.csv",
    "12-12-2023_NEGOCIOSAVISTA.csv",
    "13-12-2023_NEGOCIOSAVISTA.csv",
    "14-12-2023_NEGOCIOSAVISTA.csv",
    "15-12-2023_NEGOCIOSAVISTA.csv",
]

DATABASE_URL = URL.create(
    "postgresql+psycopg2",
    username=DATABASE_USERNAME,
    password=DATABASE_PASSWORD,
    host=DATABASE_HOSTNAME,
    port=5432,
    database=DATABASE_NAME,
)


def read_data_from_csv(csv_file: str) -> pd.DataFrame:
    return pd.read_csv(csv_file, delimiter=";", decimal=",", skip_blank_lines=True)


def load_to_database(input_data: pd.DataFrame, datatbase_engine: sqlalchemy.engine.base.Engine) -> None:
    df_filtered = pd.DataFrame(
        input_data,
        columns=["CodigoInstrumento", "HoraFechamento", "DataNegocio", "PrecoNegocio", "QuantidadeNegociada"],
    )
    df_filtered.columns = ["ticker", "hora_fechamento", "data_negocio", "preco_negocio", "quantidade_negociada"]
    df_filtered.to_sql(
        DATABASE_TABLE,
        datatbase_engine,
        if_exists="append",
        index=False,
        index_label="id",
        chunksize=1000,
        method="multi",
        dtype={
            "ticker": String(length=128),
            "hora_fechamento": String(length=128),
            "preco_negocio": Float,
            "quantidade_negociada": Integer,
            "data_negocio": DateTime,
        },
    )


def main():
    psql_engine = create_engine(DATABASE_URL, pool_recycle=3600, pool_pre_ping=True)

    with Session(psql_engine) as session:
        for file_csv in STOCK_QUOTES_FILES:
            print(f"importing {file_csv}...")
            input_df = read_data_from_csv(file_csv)
            load_to_database(input_df, datatbase_engine=psql_engine)
            session.commit()


if __name__ == "__main__":
    main()

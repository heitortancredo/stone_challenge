from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine
import pandas as pd


STOCK_QUOTES_FILES = "sample.csv"
DB_USERNAME = "postgres"
DB_PASSWORD = "postgres"
DB_HOSTNAME = "localhost"
DB_NAME = "postgres"

DATABASE_URL = URL.create(
    "postgresql+psycopg2",
    username=DB_USERNAME,
    password=DB_PASSWORD,
    host=DB_HOSTNAME,
    port=5432,
    database=DB_NAME,
)


def main():
    psql_engine = create_engine(DATABASE_URL, pool_recycle=3600, pool_pre_ping=True)

    df_csv = pd.read_csv(STOCK_QUOTES_FILES, delimiter=";", skip_blank_lines=True)

    df_filtered = pd.DataFrame(
        df_csv, columns=["CodigoInstrumento", "HoraFechamento", "DataNegocio", "PrecoNegocio", "QuantidadeNegociada"]
    )
    df_filtered.columns = ["ticker", "hora_fechamento", "data_negocio", "preco_negocio", "quantidade_negociada"]
    df_filtered.to_sql("stock_quotes", psql_engine, if_exists="append", index=True, index_label="id")


if __name__ == "__main__":
    main()

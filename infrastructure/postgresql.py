from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker

from configs import DATABASE_HOSTNAME, DATABASE_NAME, DATABASE_PASSWORD, DATABASE_USERNAME

DATABASE_URL = URL.create(
    "postgresql+psycopg2",
    username=DATABASE_USERNAME,
    password=DATABASE_PASSWORD,
    host=DATABASE_HOSTNAME,
    port=5432,
    database=DATABASE_NAME,
)

engine = create_engine(DATABASE_URL, pool_size=10, pool_recycle=3600, pool_pre_ping=True)
session_maker = sessionmaker(engine, expire_on_commit=False)

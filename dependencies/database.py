from typing import AsyncGenerator
from sqlalchemy.orm import Session

from infrastructure.postgresql import session_maker


def get_database_session() -> Session:
    with session_maker() as session:
        yield session

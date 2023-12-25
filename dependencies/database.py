from typing import Generator

from sqlalchemy.orm import Session

from infrastructure.postgresql import session_maker


def get_database_session() -> Generator[Session, None, None]:
    with session_maker() as session:
        yield session

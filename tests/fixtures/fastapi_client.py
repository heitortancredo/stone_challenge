from typing import Generator, Tuple

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from dependencies.database import get_database_session
from main import app
from tests.fixtures.database import initialize_database_with_stock_quotes, initialized_database  # noqa


@pytest.fixture
def client(initialize_database_with_stock_quotes: Session) -> Generator[Tuple[TestClient, Session], None, None]:
    def get_fresh_database_session():
        yield initialize_database_with_stock_quotes

    app.dependency_overrides[get_database_session] = get_fresh_database_session

    with TestClient(app) as test_client:
        yield test_client

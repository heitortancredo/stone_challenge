from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies.database import get_database_session
from main import app


@pytest.fixture
def client(initialized_database: AsyncSession) -> Generator[TestClient, None, None]:
    def get_fresh_database_session():
        yield initialized_database

    app.dependency_overrides[get_database_session] = get_fresh_database_session

    with TestClient(app) as test_client:
        yield test_client

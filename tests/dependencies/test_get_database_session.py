from typing import Generator

from sqlalchemy.orm import Session

from dependencies.database import get_database_session


class TestGetDatabaseSession:
    def test_when_invoked_should_return_a_generator_object(self):
        database_session = get_database_session()

        assert isinstance(database_session, Generator)

    def test_when_invoked_should_return_a_generator_with_a_session_object(self):
        database_session = get_database_session()

        session_object = next(database_session)

        assert isinstance(session_object, Session)

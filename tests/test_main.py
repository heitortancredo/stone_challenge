import pytest

from tests.fixtures.database import initialize_database_with_stock_quotes, initialized_database  # noqa
from tests.fixtures.fastapi_client import client


@pytest.fixture
def default_get_query_string() -> dict:
    return {
        "deal_date": "2023-12-08",
    }


class TestRoot:
    def test_should_return_success_response(self, client):
        response = client.get("/")

        assert response.status_code == 200


class TestGetStockQuotes:
    def test_when_no_stock_quote_found_should_return_404_status_code(self):
        pass

    def test_when_database_has_error_should_return_503_status_code(self):
        pass

    def test_when_given_a_valid_input_should_return_200_status_code(self):
        pass

    def test_when_given_ticker_with_no_deal_date_should_return_correspondent_result_from_whole_database(self):
        pass

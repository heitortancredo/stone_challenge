from datetime import datetime
import pytest
from precisely import assert_that, mapping_includes
from tests.fixtures.fastapi_client import client
from tests.fixtures.database import initialized_database, initialize_database_with_stock_quotes

import models

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
    def test_when_no_stock_quote_found_should_return_404_error_code(
        self, client, default_get_query_string, initialize_database_with_stock_quotes
    ):
        ticker = 'NotFoundTicker'
        response = client.get(f"/ticker/{ticker}")

        assert response.status_code == 404

    def test_when_given_ticker_with_no_deal_date_should_return_correspondent_result_from_whole_database(self, client, initialize_database_with_stock_quotes):
        response = client.get("/ticker/TST1").json()

        assert_that(
            response,
            mapping_includes(
                {
                    "ticker": "TST1",
                    "max_range_value": 1122.23,
                    "max_daily_volume": 17
                }
            )
        )



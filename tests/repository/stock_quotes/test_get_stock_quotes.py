import pytest
from precisely import assert_that, mapping_includes
from sqlalchemy import RowMapping  # type: ignore

from respository.stock_quotes import StockQuotesRepository
from tests.fixtures.database import initialize_database_with_stock_quotes


class TestGetStocks:
    def test_when_given_a_valid_ticker_should_return_a_list(self, initialize_database_with_stock_quotes):
        stock_quotes_repository = StockQuotesRepository(initialize_database_with_stock_quotes)

        result = stock_quotes_repository.get_stock_quotes(ticker="TST1")

        assert isinstance(result, list)

    def test_when_given_a_valid_ticker_should_return_a_list_of_rowmapping(self, initialize_database_with_stock_quotes):
        stock_quotes_repository = StockQuotesRepository(initialize_database_with_stock_quotes)

        result = stock_quotes_repository.get_stock_quotes(ticker="TST1")[0]

        assert isinstance(result, RowMapping)

    def test_when_given_an_invalid_ticker_should_an_empty_list(self, initialize_database_with_stock_quotes):
        stock_quotes_repository = StockQuotesRepository(initialize_database_with_stock_quotes)

        result = stock_quotes_repository.get_stock_quotes(ticker="InvalidTicker")

        assert len(result) == 0

    def test_when_given_an_invalid_deal_date_should_an_empty_list(self, initialize_database_with_stock_quotes):
        stock_quotes_repository = StockQuotesRepository(initialize_database_with_stock_quotes)

        result = stock_quotes_repository.get_stock_quotes(ticker="TST1", deal_date="2023-12-10")

        assert len(result) == 0

    @pytest.mark.parametrize(
        "ticker,expected_max_daily_volume,expected_max_range_value",
        [
            ("TST1", 44, 1122.23),
            ("TST2", 172, 212.23),
        ],
    )
    def test_when_given_ticker_without_deal_date_should_return_properties_from_whole_database(
        self, initialize_database_with_stock_quotes, ticker, expected_max_range_value, expected_max_daily_volume
    ):
        stock_quotes_repository = StockQuotesRepository(initialize_database_with_stock_quotes)

        result = stock_quotes_repository.get_stock_quotes(ticker=ticker)

        assert_that(
            result[0],
            mapping_includes(
                {
                    "ticker": ticker,
                    "max_range_value": expected_max_range_value,
                    "max_daily_volume": expected_max_daily_volume,
                }
            ),
        )

    def test_when_given_ticker_with_deal_date_should_return_properties_since_the_given_date(
        self, initialize_database_with_stock_quotes
    ):
        stock_quotes_repository = StockQuotesRepository(initialize_database_with_stock_quotes)

        result = stock_quotes_repository.get_stock_quotes(ticker="TST1", deal_date="2023-12-08")

        assert_that(result[0], mapping_includes({"ticker": "TST1", "max_range_value": 1122.23, "max_daily_volume": 17}))

    @pytest.mark.parametrize(
        "ticker,deal_date,expected_max_range_value",
        [
            ("TST1", "2023-12-07", 1122.23),
            ("TST1", "2023-12-08", 1122.23),
        ],
    )
    def test_when_given_ticker_should_return_properties_with_greater_value_to_preco_negocio(
        self, initialize_database_with_stock_quotes, ticker, deal_date, expected_max_range_value
    ):
        stock_quotes_repository = StockQuotesRepository(initialize_database_with_stock_quotes)

        result = stock_quotes_repository.get_stock_quotes(ticker=ticker, deal_date=deal_date)

        assert_that(
            result[0],
            mapping_includes(
                {
                    "ticker": "TST1",
                    "max_range_value": expected_max_range_value,
                }
            ),
        )

    @pytest.mark.parametrize(
        "ticker,deal_date,expected_max_daily_volume",
        [
            ("TST1", "2023-12-07", 44),
            ("TST1", "2023-12-08", 24),
        ],
    )
    def test_when_given_ticker_should_return_properties_with_greater_value_of_sum_from_each_day(
        self, initialize_database_with_stock_quotes, ticker, deal_date, expected_max_daily_volume
    ):
        stock_quotes_repository = StockQuotesRepository(initialize_database_with_stock_quotes)

        result = stock_quotes_repository.get_stock_quotes(ticker=ticker, deal_date=deal_date)

        assert_that(
            result[0],
            mapping_includes(
                {
                    "ticker": "TST1",
                    "max_daily_volume": expected_max_daily_volume,
                }
            ),
        )

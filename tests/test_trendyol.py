import pytest

from src.parsers import TrendyolParser


@pytest.fixture
def page_source():
    with open("tests/trendyol_product") as f:
        return f.read().replace("\n", "")


@pytest.fixture
def parser():
    return TrendyolParser()


class TestTrendyolParser:
    def test__parse_page(self, parser, page_source):
        expected_result = {
            "name": "Koton Trousers 1KAM43048MD ",
            "price": "129,99",
            "price_discount": "113,99",
            "price_sale": "79,79",
        }

        result = parser._parse_page(page_source)

        assert expected_result == result

    def test__parse_from_url(self, parser, page_source, mocker):
        mocker.patch("src.utils.load_url_source", return_value=page_source)

        expected_result = {
            "name": "Koton Trousers 1KAM43048MD ",
            "price": "129,99",
            "price_discount": "113,99",
            "price_sale": "79,79",
        }

        result = parser._parse_page(page_source)

        assert expected_result == result

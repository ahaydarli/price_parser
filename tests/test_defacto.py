import pytest

from src.parsers import DefactoParser, ParserError


@pytest.fixture
def page_source():
    with open("tests/defacto_product") as f:
        return f.read().replace("\n", "")


@pytest.fixture
def parser():
    return DefactoParser()


class TestDefactoParser:
    def test__parse_page(self, parser, page_source):
        expected_result = {
            "name": "Black Erkek Parfüm 50 ml",
            "price": "49,99",
            "price_discount": None,
            "price_sale": "25",
        }

        result = parser._parse_page(page_source)

        assert expected_result == result

    def test__parse_from_url(self, parser, page_source, mocker):
        mocker.patch("src.utils.load_url_source", return_value=page_source)

        expected_result = {
            "name": "Black Erkek Parfüm 50 ml",
            "price": "49,99",
            "price_discount": None,
            "price_sale": "25",
        }

        result = parser._parse_page(page_source)

        assert expected_result == result

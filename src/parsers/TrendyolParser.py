import logging
from typing import Dict

from bs4 import BeautifulSoup
from requests import HTTPError

from .Parser import Parser, ParserError
from src.utils import load_url_source

logger = logging.getLogger("product_price_parser")


class TrendyolParser(Parser):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1"
    }

    price_parsers = {
        "price": {"name": "span", "attrs": {"class": "prc-org"}},
        "price_discount": {"name": "span", "attrs": {"class": "prc-slg"}},
        "price_sale": {"name": "span", "attrs": {"class": "prc-dsc"}},
    }

    @classmethod
    def parse_from_url(cls, url: str) -> Dict:
        """Fetches product price data from given url

        Args:
          url (str): Product url

        Returns:
          dict: Product details

        Raises:
          ParserError: Parser error
        """
        try:
            logger.info(f"Loading page source for {url}")
            page_source_txt = load_url_source(url, cls.headers)
            return cls._parse_page(page_source_txt)
        except HTTPError as e:
            raise ParserError(f"Error while getting page source. More details: {e}")

    @classmethod
    def _parse_page(cls, page_source_text: str) -> Dict:
        """Get data from source text

        Args:
          page_source_text (str): Plain text

        Returns:
          dict: Product details
        """
        page_source = BeautifulSoup(page_source_text, "html.parser")
        product = page_source.find("div", attrs={"class": "pr-cn"})
        product_data = {
            "name": product.find("h1", attrs={"class": "pr-new-br"}).text,
            "price": None,
            "price_discount": None,
            "price_sale": None
        }
        for field, params in cls.price_parsers.items():
            val = product.find(**params)
            product_data[field] = val.text.split(" ")[0] if val else None
        return product_data

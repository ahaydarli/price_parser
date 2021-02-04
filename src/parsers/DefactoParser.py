import logging
from typing import Dict

from bs4 import BeautifulSoup
from requests import HTTPError

from .Parser import Parser, ParserError
from ..utils import load_url_source

logger = logging.getLogger("product_price_parser")


class DefactoParser(Parser):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1"
    }

    default_price_parsers = {
        "price": {"name": "div", "attrs": {"class": "product-info-prices-new"}},
    }

    old_price_parsers = {
        "price": {"name": "div", "attrs": {"class": "product-info-prices-old"}},
        "price_discount": {"name": "div", "attrs": {"class": "product-info-prices-new"}},
    }

    basket_old_price_parsers = {
        "price": {"name": "div", "attrs": {"class": "product-info-prices-basket-inline-old"}},
        "price_discount": {"name": "div", "attrs": {"class": "product-info-prices-basket-inline-new"}},
    }

    basket_price_parsers = {
        "price": {"name": "div", "attrs": {"class": "product-info-prices-basket-inline-new"}},
    }

    @classmethod
    def parse_from_url(cls, url: str) -> Dict:
        """Makes request to given url

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
        product = page_source.find("div", attrs={"class": "product-details"})
        product_price = product.find("div", attrs={"class": "product-info-prices-left"})
        basket = product_price.find("div", attrs={"class": "product-info-prices-basket"})
        product_data = {
            "name": product.find("h1", attrs={"class": "product-info-title"}).text,
            "price": None,
            "price_discount": None,
            "price_sale": None
        }

        # check basket sale
        if basket is None:
            old_price = product_price.find("div", attrs={"class": "product-info-prices-old"})
            parser = cls.old_price_parsers if old_price else cls.default_price_parsers
        else:
            old_price = product_price.find("div", attrs={"class": "product-info-prices-basket-inline-old"})
            parser = cls.basket_old_price_parsers if old_price else cls.basket_price_parsers
            sale = product_price.find('div', attrs={'class': 'product-info-prices-basket-sale'})
            # remove basket sale text
            sale.find('span', attrs={'class': 'product-info-prices-basket-sale-percentage'}).decompose()
            product_data['price_sale'] = sale.text.split(" ")[2]
        for field, params in parser.items():
            val = product.find(**params)
            product_data[field] = val.text.split(" ")[0] if val else None

        return product_data

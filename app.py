import re
import logging

from src.parsers import TrendyolParser, DefactoParser

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("product_price_parser")

parsers = {
    "trendyol": {
        "domain": "trendyol.com",
        "regex": r"^(https?:\/\/)?[a-z0-9]+([\-\.]trendyol+)\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$",
        "parser": TrendyolParser,
    },
    "defacto": {
        "domain": "defacto.com.tr",
        "regex": r"^(https?:\/\/)?[a-z0-9]+([\-\.]defacto+)\.[a-z]{2,5}.[a-z]{2,4}(:[0-9]{1,5})?(\/.*)?$",
        "parser": DefactoParser,
    },
}


def parse_and_print(url):
    """Makes request to given url

    Args:
      url (str): Product url
    """
    for parser, parser_params in parsers.items():
        if re.search(parser_params["regex"], url):
            logger.info(
                f"Found {parser} url. Parsing using {parser_params['parser'].__name__}"
            )
            data = parser_params["parser"].parse_from_url(url)
            print(data)


if __name__ == "__main__":
    logger.info("Starting application...")
    urls = []
    logger.info("Reading urls from file...")
    with open("urls") as f:
        for url in f.readlines():
            urls.append(url.strip())
    logger.info(f"{len(urls)} urls loaded from file. Starting execution...")

    for url in urls:
        try:
            parse_and_print(url)
        except Exception as e:
            logger.error(f"Error occurred while parsing data: {e}")
            continue

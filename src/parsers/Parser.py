from abc import ABC, abstractmethod
from typing import Dict


class ParserError(Exception):
    """A Parser object contains a lot of parsers
    Args:
        msg (str): Error message
    """

    def __init__(self, msg):
        super().__init__(msg)


class Parser(ABC):
    """A Parser object contains a lot of parsers"""

    @classmethod
    @abstractmethod
    def parse_from_url(cls, url: str) -> Dict:
        pass

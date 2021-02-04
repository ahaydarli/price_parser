from abc import ABC, abstractmethod
from typing import Dict


class ParserError(Exception):
    """Parser Exception that raised for issues during parsing
    Args:
        msg (str): Error message
    """

    def __init__(self, msg):
        super().__init__(msg)


class Parser(ABC):
    """Abstract Base Class for parsers to ensure that they all implement the same methods"""

    @classmethod
    @abstractmethod
    def parse_from_url(cls, url: str) -> Dict:
        pass

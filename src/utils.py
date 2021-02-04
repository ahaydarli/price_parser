from typing import Dict

import requests
from requests import HTTPError


def load_url_source(url: str, headers: Dict) -> str:
    """Make a request to  url using requests library
    Args:
        url (str): Product url.
        headers (dict): Headers.
    Raises:
        HTTPError: Url is redirects to another url or not found
    Returns:
        response (str): Plain text of response
    """
    try:
        response = requests.get(url, headers=headers, allow_redirects=False)
        if response.status_code != 200:
            raise HTTPError(f"Could not load url, status code {response.status_code}")
        return response.text
    except HTTPError as e:
        raise e

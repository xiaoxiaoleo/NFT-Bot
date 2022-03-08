"""
File responsible for managing simple tasks as requests.
"""
from typing import Union
import requests
from requests.models import Response
from wconfig import MoralisKey
import time

def get_moralis(endpoint: str, **kwargs) -> Union[dict, Response]:
    """Internal function for GETting opensea API endpoints."""

    # Limiting "limit" parametar to 50
    # if kwargs.get("limit"):
    #     kwargs["limit"] = 50 if kwargs["limit"] > 50 else kwargs["limit"]

    url = f"https://deep-index.moralis.io/api/v2/{endpoint}"
    headers = {
        "Accept": "application/json",
        "X-API-KEY": MoralisKey[0]
    }

    try:
        response = requests.get(url, params=kwargs,  headers=headers)
    except requests.exceptions.ConnectionError:
        time.sleep(5)
        response = requests.get(url, params=kwargs, headers=headers)


    # It is better to check the status code like this because you also check for status code 304...
    if response.ok:
        return response.json()
    else:
        return None
    #return response

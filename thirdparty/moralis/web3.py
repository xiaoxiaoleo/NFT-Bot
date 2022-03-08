from typing import Union, List
from requests.models import Response
import time
#from thirdparty.opensea.common import get_opensea
from thirdparty.moralis.models.web3 import Transaction

from thirdparty.moralis.common import get_moralis


def get_transaction(
    tx_hash: str = "",
) -> Union[Transaction, Response]:
    """
    """

    api_parameters = {
        'chain': 'eth',
    }

    uri = f"/transaction/{tx_hash}"
    response = get_moralis(uri, **api_parameters)
    while response is None:
        time.sleep(4)
        response = get_moralis(uri, **api_parameters)

    if isinstance(response, dict):
        return Transaction(response)
    return response
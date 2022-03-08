from typing import Union, List
from requests.models import Response
import time
#from thirdparty.opensea.common import get_opensea
from thirdparty.moralis.models.nft import LowPrice

from thirdparty.moralis.common import get_moralis


def get_nft_lastprice(
    address: str = "",
    days: int = 2,
) -> Union[List[LowPrice], Response]:

    api_parameters = {
      #  "offset": offset,
        "days": days,
        'chain': 'eth',
        'marketplace': 'opensea'
    }

    uri = f"nft/{address}/lowestprice"
    response = get_moralis(uri, **api_parameters)
    # while response is None:
    #     time.sleep(4)
    #     response = get_moralis(uri, **api_parameters)

    if isinstance(response, dict):
        return LowPrice(response)

    return response



from typing import Union, List
from requests.models import Response

from thirdparty.moralis.models.nft_owner import NFTOwner

from thirdparty.moralis.common import get_moralis


def get_nft_owner(
    address: str = "",
    limit: int = 5,
    token_address: str = '',
    offset: int = 0,
) -> Union[List[NFTOwner], Response]:
    """ Î
    """

    api_parameters = {
      #  "offset": offset,
        "limit": limit,
        'chain': 'eth',
        'offset': 0,
        'format': 'decimal'
    }

    uri = f"/nft/{token_address}/owners"
    response = get_moralis(uri, **api_parameters)
    if isinstance(response, dict):
        return [NFTOwner(i) for i in response["result"]]

    return response





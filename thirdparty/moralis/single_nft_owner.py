from typing import Union, List
from requests.models import Response

from thirdparty.moralis.models.nft_owner import NFTOwner
from thirdparty.moralis.account_nft_transfer import get_account_nft_transfer

from thirdparty.moralis.common import get_moralis


def get_single_nft_owner(
    limit: int = 5,
    token_address: str = '',
    token_id: str = '',
    offset: int = 0,
) -> Union[List[NFTOwner], Response]:
    """ Î
    """

    api_parameters = {
      #  "offset": offset,
        "limit": limit,
        'chain': 'eth',
        'offset': offset,
        'format': 'decimal'
    }

    uri = f"/nft/{token_address}/{token_id}/owners"
    response = get_moralis(uri, **api_parameters)
    if isinstance(response, dict):
        return [NFTOwner(i) for i in response["result"]]

    return None

# for eip1155
def get_single_nft_owner_all(
    total: int = 5,
    token_address: str = '',
    token_id: str = '',
) -> Union[List[NFTOwner], Response]:
    """ Î
    """
    limit = 300

    full_lst = []
    for i in range(0, int(total/limit)+1):
        offset = i * limit
        lst = get_single_nft_owner(
                limit,
                token_address,
                token_id,
                offset
        )

        full_lst = full_lst + lst

    return full_lst
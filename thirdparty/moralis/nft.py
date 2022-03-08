from typing import Union, List
from requests.models import Response
import json

from thirdparty.moralis.models.account_nft_owner import AccountNFTOwner, AccountNFTMetadata

from thirdparty.moralis.common import get_moralis
from thirdparty.moralis.models.nft import SingleNFTInfo


def get_account_nft_owner(
    address: str = "",
    limit: int = 5,
    token_address: str = '',
    offset: int = 0,
    chain: str = 'eth'
) -> Union[List[AccountNFTOwner], Response]:
    """
    Retrieves NFT bundles from opensea.io.

    :param owner: The address for the owner of the assets.
    :type owner: str

    :param limit: Number of NFT assets to retrieve, cannot be more than 50 due to api limitations. 10 by default.
    :type limit: int

    :param offset: Number of NFT assets to skip. 0 by default.
    :type offset: int
    """

    api_parameters = {
      #  "offset": offset,
        "limit": limit,
        'chain': chain,
        'format': 'decimal'
    }

    uri = f"{address}/nft/{token_address}"
    response = get_moralis(uri, **api_parameters)
    if isinstance(response, dict):
        return [AccountNFTOwner(i) for i in response["result"]]

    return response


def get_nft_collection_metadata(
        token_address: str = '',
) -> Union[List[AccountNFTOwner], Response]:
    """
    """

    api_parameters = {
        'chain': 'eth',
    }

    uri = f"/nft/{token_address}/metadata"
    response = get_moralis(uri, **api_parameters)
    if isinstance(response, dict):
        return AccountNFTMetadata(response)

    return response

def get_single_nft_metadata(
        token_address: str = '',
        token_id: str=''
) -> Union[List[AccountNFTOwner], Response]:
    """
    """

    api_parameters = {
        'chain': 'eth',
    }

    uri = f"/nft/{token_address}/{token_id}"
    response = get_moralis(uri, **api_parameters)
    return SingleNFTInfo(response)

    #return response



def get_all_nft_in_account(
    address: str = "",
    limit: int = 5,
    offset: int = 0,
    chain: str = 'eth'
) -> Union[List[AccountNFTOwner], Response]:
    """
    Retrieves NFT bundles from opensea.io.

    :param owner: The address for the owner of the assets.
    :type owner: str

    :param limit: Number of NFT assets to retrieve, cannot be more than 50 due to api limitations. 10 by default.
    :type limit: int

    :param offset: Number of NFT assets to skip. 0 by default.
    :type offset: int
    """

    api_parameters = {
      #  "offset": offset,
        "limit": limit,
        'chain': chain,
        'format': 'decimal',
        'offset': offset
    }

    uri = f"{address}/nft"
    response = get_moralis(uri, **api_parameters)
    if isinstance(response, dict):
        return [AccountNFTOwner(i) for i in response["result"]]

    return response


def get_full_nft_in_account(
    address: str = "",
    limit: int = 5,
    offset: int = 0,
    chain: str = 'eth'
) -> Union[List[AccountNFTOwner], Response]:
    """
    Retrieves NFT bundles from opensea.io.

    :param owner: The address for the owner of the assets.
    :type owner: str

    :param limit: Number of NFT assets to retrieve, cannot be more than 50 due to api limitations. 10 by default.
    :type limit: int

    :param offset: Number of NFT assets to skip. 0 by default.
    :type offset: int
    """
    # get total
    total  = 0
    api_parameters = {
      #  "offset": offset,
        "limit": 2,
        'chain': chain,
        'format': 'decimal',
        'offset': 0
    }

    uri = f"{address}/nft"
    response = get_moralis(uri, **api_parameters)
    if isinstance(response, dict):
        total = response['total']

    page_size = 500
    total_list = []
    for i in range(0, int(total/page_size)):
        api_parameters = {
            "limit": page_size,
            'chain': chain,
            'format': 'decimal',
            'offset': page_size * i
        }

        if isinstance(response, dict):
            total_list = total_list +  [AccountNFTOwner(i) for i in response["result"]]

    return total_list
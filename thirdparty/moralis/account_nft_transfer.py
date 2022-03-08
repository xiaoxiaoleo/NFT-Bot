from typing import Union, List
from requests.models import Response
import time
#from thirdparty.opensea.common import get_opensea
from thirdparty.moralis.models.account_nft_transfer import AccountNFTTransfer

from thirdparty.moralis.common import get_moralis


def get_account_nft_transfer(
    address: str = "",
    limit: int = 5,
    direction: str = 'from',
    offset: int = 0,
) -> Union[List[AccountNFTTransfer], Response]:
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
        'direction': direction,
        'chain': 'eth',
        'format': 'decimal'
    }

    uri = f"{address}/nft/transfers"
    response = get_moralis(uri, **api_parameters)
    while response is None:
        time.sleep(4)
        response = get_moralis(uri, **api_parameters)

    if isinstance(response, dict):
        return [AccountNFTTransfer(i) for i in response["result"]]

    return response



def get_total(address: str = "",):
    api_parameters = {
      #  "offset": offset,
        "limit": 1,
        'chain': 'eth',
        'format': 'decimal',
        "offset": 0
    }

    uri = f"/nft/{address}/transfers"
    response = get_moralis(uri, **api_parameters)
    while response is None:
        print('respose is none')
        time.sleep(4)
        response = get_moralis(uri, **api_parameters)

    if isinstance(response, dict):
        totalpages = response['total']
        print(f"total pages {totalpages}")
        return totalpages

def get_nft_transfer(
    address: str = "",
    limit: int = 5,
    offset: int = 0,
) -> Union[List[AccountNFTTransfer], Response]:
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
        'chain': 'eth',
        'format': 'decimal',
        "offset": offset
    }

    uri = f"/nft/{address}/transfers"
    response = get_moralis(uri, **api_parameters)
    while response is None:
        time.sleep(4)
        response = get_moralis(uri, **api_parameters)

    if isinstance(response, dict):
        return [AccountNFTTransfer(i) for i in response["result"]]

    return response

def get_block_nft_transfer(
    from_block: int = 0,
    to_block: int = 0,
    offset: int = 0,
    limit: int = 500,
) -> Union[List[AccountNFTTransfer], Response]:
 # https://deep-index.moralis.io/api/v2/nft/transfers?chain=eth&from_block=14023700&to_block=14023701&format=decimal
    api_parameters = {
       "offset": offset,
        "limit": limit,
        'from_block': from_block,
        'to_block': to_block,
        'chain': 'eth',
        'format': 'decimal'
    }

    uri = f"nft/transfers"
    response = get_moralis(uri, **api_parameters)
    while response is None:
        time.sleep(4)
        response = get_moralis(uri, **api_parameters)

    if isinstance(response, dict):
        return [AccountNFTTransfer(i) for i in response["result"]]

    return response



#
# class get_account_nft_transfer:
#     def __init__(self, json_data):
#         """
#         """
#         # ASSET DETAILS
#         # self.name = json_data["name"]
#         # self.description = json_data["description"]
#         # self.token_id = json_data["token_id"]
#         # self.asset_url = json_data["permalink"]
#         # self.contract_address = json_data["asset_contract"]["address"]
#
#         # # COLLECTION DETAILS
#         # self.collection_name = json_data["collection"]["name"]
#         # self.collection_description = json_data["collection"]["description"]
#         # self.collection_slug = json_data["collection"]["slug"]
#         # self.verification_status = json_data["collection"]["safelist_request_status"]
#         # self.is_verified = json_data["collection"]["safelist_request_status"] == "verified"
#         #
#         # # OWNER DETAILS
#         # self.owner = Account(json_data["owner"])
#         #
#         #self.__ASSET_API_URL = f"https://api.opensea.io/api/v1/asset/{self.contract_address}/{self.token_id}"
#         api_parameters = {
#             "owner": owner,
#             "offset": offset,
#             "limit": limit,
#         }
#
#         response = get_moralis("", **api_parameters)
#         if isinstance(response, dict):
#             return [Bundle(i) for i in response["bundles"]]
#
#         return response

    # def get_json(self):
    #     response = request("GET", self.__ASSET_API_URL)
    #     if response.status_code == 200:
    #         return response.json()
    #     else:
    #         return None
    #
    # def get_floor_price(self):
    #     """
    #     Returns the floor price of the collection an asset belongs to
    #     """
    #     asset_json = self.get_json()
    #     floor_price = asset_json["collection"]["stats"]["floor_price"]
    #     return floor_price
    #
    # def get_current_price(self):
    #     asset_json = self.get_json()
    #     try:
    #         current_price = asset_json["orders"][0]["current_price"]
    #     except:
    #         current_price = None
    #     return current_price
    #
    # def get_average_price(self):
    #     asset_json = self.get_json()
    #     average_price = asset_json["collection"]["stats"]["average_price"]
    #     return average_price

import requests
#import pandas as pd


class MoralisApiHandler:
    def __init__(self):
        self.url_base = 'https://deep-index.moralis.io/api/v2/'
        self.api_key = None

    def set_api_key(self, api_key):
        self.api_key = api_key

    def api_request(self, endpoint, method="GET"):
        headers = {
            "x-api-key": self.api_key
        }
        response = requests.request(url=self.url_base + endpoint, method=method, headers=headers)
        if response.status_code == 200:
            response_object = response.json()
            return response_object
        else:
            return False

    # Available values : eth, 0x1, ropsten, 0x3, rinkeby, 0x4, goerli, 0x5, kovan, 0x2a, polygon, 0x89, mumbai, 0x13881, bsc, 0x38, bsc testnet, 0x61, avalanche, 0xa86a, avalanche testnet, 0xa869, fantom, 0xfa
    # https://admin.moralis.io/web3Api#
    def get_native_balance(self, wallet_address, chain):
        endpoint = wallet_address + "/balance?chain=" + chain
        return float(self.api_request(endpoint)['balance'])

    def get_tokens_for_wallet(self, wallet_address, chain):
        endpoint = wallet_address + "/erc20?chain=" + chain
        return self.api_request(endpoint)

    def get_token_price(self, token_address, chain):
        endpoint = 'erc20/' + token_address + "/price?chain=" + chain
        return self.api_request(endpoint)

    def convert_native_amount_to_token_amount(self, token_address, chain, native_price_amount):
        price_api_response = self.get_token_price(token_address, chain)
        native_price = float(price_api_response['nativePrice']['value']) * (
                    10 ** float(-price_api_response['nativePrice']['decimals']))
        native_amount = (1 / native_price) * native_price_amount
        return native_amount

    def convert_token_amount_to_native_amount(self, token_address, chain, token_amount):
        price_api_response = self.get_token_price(token_address, chain)
        native_price = float(price_api_response['nativePrice']['value']) * (
                    10 ** float(-price_api_response['nativePrice']['decimals']))
        token_amount = (native_price) * token_amount
        return token_amount

    def get_total_token_assets(self, wallet_address, chains, tokens_to_exclude=None):
        if tokens_to_exclude is None:
            tokens_to_exclude = ['KK8.io']
        native_token_assets = []
        erc20_token_assets = []
        erc20_assets = 0
        for chain in chains:
            native_balance = self.get_native_balance(wallet_address, chain)
            print(chain+"  "+str(native_balance))
            native_token_assets.append({"chain": chain, "native_balance": native_balance})
            tokens = self.get_tokens_for_wallet(wallet_address, chain=chain)
            for token in tokens:
                token_price = self.get_token_price(token['token_address'], chain=chain)
                token_quantity = float(token['balance'])*(10**-float(token['decimals']))
                holdings_value = token_quantity*float(token_price['usdPrice'])
                print(chain+"  "+token['symbol']+"  quantity:"+str(token_quantity)+" price:$"+str(token_price['usdPrice'])+" extended value:$"+str(holdings_value)+"  "+token['token_address'])
                erc20_token_assets.append({
                    "chain": chain
                    ,"symbol": token['symbol']
                    ,"token_address": token['token_address']
                    ,"price": token_price
                    ,"quantity": token_quantity
                    ,"holdings_value":holdings_value
                    ,"detail_object": token
                })

                if token['symbol'] not in tokens_to_exclude:
                    erc20_assets += float(holdings_value)

        #native_token_assets_df = pd.DataFrame(native_token_assets)
        #erc20_token_assets_df = pd.DataFrame(erc20_token_assets)

        print("total ERC-20 token assets: ", erc20_assets)
        return erc20_assets#, native_token_assets_df, erc20_token_assets_df
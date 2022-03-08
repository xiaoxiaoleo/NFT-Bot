import json

class LowPrice:
    def __init__(self, json_data):
        """
        Put useful information from json_data into their own variables under Account class.

        :param json_data: json object returned by the opensea-api
        :type json_data: dict
        """
        # ACCOUNT DETAILS
        self.transaction_hash = json_data["transaction_hash"]
        #self.to_address = json_data["to_address"]
        self.price = json_data['price']
        self.block_timestamp = json_data['block_timestamp']
        self.block_number = json_data['block_number']

        self.token_address = json_data["token_address"]


class SingleNFTInfo:
    def __init__(self, json_data):
        """
        Put useful information from json_data into their own variables under Account class.

        :param json_data: json object returned by the opensea-api
        :type json_data: dict
        """
        # ACCOUNT DETAILS
        self.name = json_data["name"]
        #self.to_address = json_data["to_address"]
        self.symbol = json_data['symbol']
        self.metadata = json.loads(json_data['metadata'])
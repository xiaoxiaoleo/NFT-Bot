class NFTOwner:
    def __init__(self, json_data):
        """
        Put useful information from json_data into their own variables under Account class.

        :param json_data: json object returned by the opensea-api
        :type json_data: dict
        """
        # ACCOUNT DETAILS
        self.owner = json_data["owner_of"]
        #self.to_address = json_data["to_address"]
        self.token_address = json_data['token_address']
        self.token_id = json_data['token_id']
        self.amount = json_data['amount']
        self.name = json_data['name']
        self.symbol = json_data['symbol']
        self.contract_type = json_data['contract_type']
        self.synctime = json_data['synced_at']

class AccountNFTTransfer:
    def __init__(self, json_data):
        """
        Put useful information from json_data into their own variables under Account class.

        :param json_data: json object returned by the opensea-api
        :type json_data: dict
        """
        # ACCOUNT DETAILS
        self.from_address = json_data["from_address"]
        self.to_address = json_data["to_address"]
        self.token_address = json_data['token_address']
        self.token_id = json_data['token_id']
        self.transaction_hash = json_data['transaction_hash']
        self.amount = json_data['amount']
        self.block_timestamp = json_data['block_timestamp']


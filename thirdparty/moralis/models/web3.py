class Transaction:
    def __init__(self, json_data):
        """
        """
        # ACCOUNT DETAILS
        self.from_address = json_data["from_address"]
        self.block_hash = json_data['block_hash']
        self.block_number = json_data['block_number']
        self.to_address = json_data['to_address']
        self.input = json_data['input']
        self.value=int(json_data['value'])/10**18

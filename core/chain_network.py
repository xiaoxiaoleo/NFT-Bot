from typing import (
    Callable,
    Dict,
)
from datetime import datetime

from web3 import Web3
from web3.gas_strategies.time_based import (
    fast_gas_price_strategy,
    medium_gas_price_strategy,
    slow_gas_price_strategy,
    glacial_gas_price_strategy,
)
from web3.middleware import geth_poa_middleware
import concurrent.futures


from core.libs import get_logger, Wei
from wconfig import CHAIN_PROVIDER

GAS_STRATEGY_MAP: Dict[str, Callable] = {
    'fast': fast_gas_price_strategy,  # 1 minute
    'medium': medium_gas_price_strategy,  # 5 minutes
    'slow': slow_gas_price_strategy,  # 1 hour
    'glacial': glacial_gas_price_strategy,  # 24 hours
}


class W3ClientError(Exception):
    pass


logger = get_logger('chain_network.log')


class ChainNetwork():
    def __init__(self,
                 chain_name: str = None,
                 ) -> None:
        self.chain_name = chain_name
        provider = CHAIN_PROVIDER[chain_name]
        if provider.startswith('https://') or provider.startswith('http://'):
            web3_provider = Web3.HTTPProvider(provider, request_kwargs={"timeout": 60})
        elif provider.startswith('wss://'):
            web3_provider = Web3.WebsocketProvider(provider)
        elif provider.startswith('/'):
            web3_provider = Web3.IPCProvider(provider)
        else:
            raise (f"Unknown provider type '{provider}'")

        self.w3 = Web3(web3_provider)
    def chain_info(self):
        logger.info(f'chain: {self.chain_name} chain_id: {self.chain_id}')
        logger.info(f'provider: {self.provider}')

    @property
    def is_connected(self) -> bool:
        return self.w3.isConnected()

    def get_last_block(self):
        if self.chain_name != 'eth' and not self.w3.middleware_onion.__contains__(geth_poa_middleware):
            self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        return self.w3.eth.get_block('latest')

    def get_last_block_time(self):
        if self.chain_name != 'eth' and not self.w3.middleware_onion.__contains__(geth_poa_middleware):
            self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        block = self.w3.eth.get_block('latest')
        block_num = block.number
        ts = datetime.utcfromtimestamp(block.timestamp).strftime('%Y-%m-%d %H:%M:%S')
        #logger.debug(f'block timestamp:{ts}\t{block.timestamp}\tblock:{block_num}')
        return int(block.timestamp)

    def get_tx_logs(self, tx):
        return self.w3.eth.getTransactionReceipt(tx).logs


    def get_tx_from(self, tx):
        return self.w3.eth.get_transaction(tx)['from'].lower()

    def get_tx(self, tx):
        return self.w3.eth.get_transaction(tx)

    def get_pending_tx(self, tx):
        pass

    def balance(self, address):
        address = self.w3.toChecksumAddress(address)
        balance = self.w3.eth.get_balance(address)
        return  balance / 10 ** 18

    @staticmethod
    def convert_to_blocktime(timestr):
        """
         fmt: #'%Y-%m-%d %H:%M:%S'
        :param self:
        :return:
        """
        ts = datetime.strptime(timestr, '%Y-%m-%d %H:%M:%S').timestamp()
        return int(ts)

    @staticmethod
    def convert_to_blocktimestr(timestr):
        """
         fmt: #'%Y-%m-%d %H:%M:%S'

        :param self:
        :return:
        """
        ts = datetime.utcfromtimestamp(timestr).strftime('%Y-%m-%d %H:%M:%S')
        return ts

    def suggest_gas_price(self, mode: str = 'medium') -> Wei:
        """
        Suggests gas price depending on required transaction priority.
        Supported priorities are: 'fast', 'medium', 'slow', 'glacial'.

        Warning: This operation is very slow (~30sec)!
        """

        if mode not in GAS_STRATEGY_MAP:
            raise W3ClientError(
                f"Unsupported gas strategy type, pick from: {[k for k in GAS_STRATEGY_MAP]}"
            )

        self.w3.eth.setGasPriceStrategy(GAS_STRATEGY_MAP[mode])
        return self.w3.eth.generateGasPrice()


def chain_pool_push(chain_name: str, signed_tx):
    providers = CHAIN_PROVIDER[chain_name + '_pool']
    w3_pool = []
    for provider in providers:
        if provider.startswith('https://') or provider.startswith('http://'):
            web3_provider = Web3.HTTPProvider(provider, request_kwargs={"timeout": 60})
        elif provider.startswith('wss://'):
            web3_provider = Web3.WebsocketProvider(provider)
        elif provider.startswith('/'):
            web3_provider = Web3.IPCProvider(provider)
        else:
            raise (f"Unknown provider type '{provider}'")

        w3 = Web3(web3_provider)
        w3_pool.append(w3)

    max_works = len(providers)
    rawTransaction = signed_tx.rawTransaction
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_works) as executor:
        # Start the load operations and mark each future with its URL
        future_to_url = {executor.submit(single_push, w3, rawTransaction): w3 for w3 in w3_pool}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                data = future.result()
                print(data)
            except Exception as exc:
                print('generated an exception: %s' % (exc))


def single_push(w3, rawTransaction):
    tx_hash = w3.eth.send_raw_transaction(rawTransaction)
    return Web3.toHex(tx_hash)


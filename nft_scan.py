
from monitor.libs import get_related_nft_transfer, alert_logic, verify_nft_buy_transfer, verify_nft_sell_transfer
import threading, queue, time
from core.chain_network import ChainNetwork
from core.libs import get_logger

QUEUE_BLOCK_NUMBER = queue.Queue(maxsize=20)
QUEUE_TX = queue.Queue(maxsize=20)
QUEUE_VERIFIED_BUY_TXS = queue.Queue(maxsize=50)
QUEUE_VERIFIED_SELL_TXS = queue.Queue(maxsize=50)

logger = get_logger('nftmonitor')

chain = ChainNetwork(chain_name='eth')

original_address_list = [
    {'address': '0x08046e2349017615d53d3977c307d39ab4eeb3cf', 'comment': 'Nansen smart maxnaut.eth'},
    {'address': '0x4f3215bb59dbd3a868510ebc02971570778aa360', 'comment': 'Nansen smart carerack.eth'},
    {'address': '0x2465bd53a0e4f726dc6bf059e07979715c44dc0b', 'comment': 'Nansen smart jam123.eth'},
    {'address': '0x877adf7a6d29a4678dc86cba270a2c5257b6ecc9', 'comment': 'Nansen smart darejewb.eth'},
    {'address': '0x7ef61cacd0c785eacdfe17649d1c5bcba676a858', 'comment': 'Nansen smart kkmoneyy.eth'},
]

# format
address_list = []
for user_info in original_address_list:
    address_list.append({"address": user_info['address'].lower(), 'comment': user_info['comment']})


def test(start_block):

    #tg_alert('test alert...start.', 1)
    from_block = start_block
    to_block = start_block
    all_transfer_obj = get_related_nft_transfer(from_block, to_block)
    transfer_lst = verify_nft_buy_transfer(chain, address_list, all_transfer_obj)
    alert_logic(transfer_lst, address_list, 1)


def producer_block_number():
    last_block = 14246553 # chain.get_last_block().number  # 14198485
    #QUEUE_BLOCK_NUMBER.put(last_block)
    while True:
        chain_block_number = chain.get_last_block().number
        if chain_block_number > last_block:
            logger.info(f'put new block number {chain_block_number} to queue')
            QUEUE_BLOCK_NUMBER.put(chain_block_number)
            last_block = chain_block_number
        time.sleep(1)


def producer_tx():
    while True:
        if not QUEUE_BLOCK_NUMBER.empty():
            block_number = QUEUE_BLOCK_NUMBER.get()
            chain_block_number = chain.get_last_block().number

            if int(chain_block_number) - int(block_number) > 6:
                logger.info(f'{block_number} missed')
                continue

            all_transfer_obj = get_related_nft_transfer(block_number)
            if len(all_transfer_obj) > 0:
                QUEUE_TX.put(all_transfer_obj)
                continue
            else:
                QUEUE_BLOCK_NUMBER.put(block_number)
        else:
            logger.info(f'queue BLOCK_NUMBER is empty ')
        time.sleep(1)


def consumer_tx():
    while True:
        if not QUEUE_TX.empty():
            all_transfer_obj = QUEUE_TX.get()
            transfer_buy_lst = verify_nft_buy_transfer(chain, address_list, all_transfer_obj)
            QUEUE_VERIFIED_BUY_TXS.put(transfer_buy_lst)

            transfer_sell_lst = verify_nft_sell_transfer(chain, address_list, all_transfer_obj)
            QUEUE_VERIFIED_SELL_TXS.put(transfer_sell_lst)
        else:
            logger.info(f'queue QUEUE_TX is empty ')
        time.sleep(1)

def consumer_alert_buy():
    while True:
        if not QUEUE_VERIFIED_BUY_TXS.empty():
            transfer_lst = QUEUE_VERIFIED_BUY_TXS.get()
            alert_logic(transfer_lst, address_list, 1, 'buy')
        time.sleep(1)

def consumer_alert_sale():
    while True:
        if not QUEUE_VERIFIED_SELL_TXS.empty():
            transfer_lst = QUEUE_VERIFIED_SELL_TXS.get()
            alert_logic(transfer_lst, address_list, 2, 'sale')
        time.sleep(1)

if __name__ == "__main__":

    p0 = threading.Thread(target=producer_block_number)
    p1 = threading.Thread(target=producer_tx)
    c1 = threading.Thread(target=consumer_tx)
    c2 = threading.Thread(target=consumer_alert_buy)
    c3 = threading.Thread(target=consumer_alert_sale)
    p0.start()
    p1.start()
    c1.start()
    c2.start()
    c3.start()

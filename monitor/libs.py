

from thirdparty.moralis.account_nft_transfer import get_account_nft_transfer, get_block_nft_transfer
from thirdparty.moralis.web3 import get_transaction
#from common.data.handle_data import insert_to_smartmoney
from thirdparty.moralis.datalib import get_nft_info, get_nft_name
from thirdparty.moralis.web3 import get_transaction
import datetime
from core.libs import get_logger
from thirdparty.notify.telegram import tg_alert

logger = get_logger('msglog')

def if_moniter_address(address_list, address):
    for i in address_list:
        if i['address'].lower() == address.lower():
            return True
    return False

def get_addresscomment(address_list, address):
    for i in address_list:
        if i['address'].lower() == address.lower():
            return i['comment']

def get_event_mark():
    timestr = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    mark_str = f"alert {timestr}:"
    return  mark_str


def verify_from(chain, tx_hash, address):
    from_address = chain.get_tx_from(tx_hash)
    #obj = get_transaction(tx_hash)
    return from_address.lower() == address.lower()
    #if (obj.to_address is None) :
    #    return False
    #return obj.from_address.lower() == address.lower()

def get_related_nft_transfer(block_number):
    from_block = to_block = block_number
    #to_block = chain.get_last_block().number
    rsp = get_block_nft_transfer(from_block=from_block, to_block=to_block)
    logger.info(f'{from_block} - {to_block}  NFT txs: {len(rsp)}')
    return rsp

def verify_nft_buy_transfer(chain, address_list, rsp):
    transfer_lst = []
    for obj in rsp:
        if (obj.to_address is None) or (obj.from_address is None) or (obj.block_timestamp is None):
            continue
        address = obj.to_address.lower()
        if if_moniter_address(address_list, address):
            if verify_from(chain, obj.transaction_hash, address):
                transfer_lst.append(obj)
    return transfer_lst

def verify_nft_sell_transfer(chain, address_list, rsp):
    transfer_lst = []
    for obj in rsp:
        if (obj.to_address is None) or (obj.from_address is None) or (obj.block_timestamp is None):
            continue
        address = obj.from_address.lower()
        if if_moniter_address(address_list, address):
            transfer_lst.append(obj)
    return transfer_lst

def get_fun_info(tx):
    transaction_hash = tx.transaction_hash
    txobj = get_transaction(transaction_hash)
    function_info = f'{txobj.input[:10]}'

    if tx.from_address == '0x0000000000000000000000000000000000000000':
        return f'mint {txobj.value}E'

    if txobj.input.startswith('0xab834bab'):
        function_info = 'opensea' # automicmatch
    if txobj.input.startswith('0x23b872dd'):
        function_info = 'transferfrom'
    if txobj.input.startswith('0xf242432a'):
        function_info = 'safetransferfrom'
    if txobj.input.startswith('0x5eacc63a'):
        function_info = 'gemswap'
    if txobj.input.startswith('0x9a2b8115'):
        function_info = 'gemswap'
    if txobj.input.startswith('0x186b100c'):
        function_info = 'genieswap'
    if txobj.input.startswith('0x357a150b'):
        function_info = 'x2y2'
    if txobj.input.startswith('0xb4e4b296'):
        function_info = 'looksrare'
    return f"{function_info} {txobj.value}E"

def html_encode(msg):
    if isinstance(msg, str):
        return msg.replace('&', ' ').replace('<', ' ').replace('>', ' ').replace('"', ' ').replace("'", ' ').replace("#", ' ')
    else:
        return 'None'

def alert_logic(transfer_lst: list,  address_list, channel_id, tx_type):
    if len(transfer_lst) == 0 :
        return None
    all_msg = ''
    for tx in transfer_lst:
        token_id = tx.token_id
        if tx_type == 'buy':
            address = tx.to_address
            funinfo = get_fun_info(tx)
        if tx_type == 'sale':
            address = tx.from_address
            funinfo = 'sale'

        token_address = tx.token_address
        etherscan_urls = etherscan_url(address, token_address)
        opensaurl = opensea_url(token_address, token_id)
        nftnerdurl = nftner_url(token_address)
        user_comment = get_addresscomment(address_list, address)
        nft_name = get_nft_name(token_address=token_address, token_id=token_id)

        push_msg = f"[<ins><strong>{html_encode(nft_name)}</strong></ins>] [{funinfo}] [<strong>{html_encode(user_comment) }</strong>] [{etherscan_urls} {opensaurl} {nftnerdurl}]  "

        all_msg = all_msg + push_msg + '\n'

    logger.info(all_msg)
    tg_alert(all_msg, channel_id)


def etherscan_url(user_address, tokenaddr):
    url = f'https://etherscan.io/token/{tokenaddr}?a={user_address}'
    return f"<a href='{url}'>etherscan</a>"

def opensea_url(tokenaddr, tokenid):
    url = f'https://opensea.io/assets/{tokenaddr.lower()}/{tokenid}'
    return f"<a href='{url}'>opensea</a>"

def nftner_url(token_address):
    url = f"https://nftnerds.ai/collection/{token_address}"
    return f"<a href='{url}'>nftnerd</a>"

def nft_info_lst(user_buy_list):
    nft_lst = []
    for tokenaddr in user_buy_list:
        nft = get_nft_info(token_address=tokenaddr)
        nft_lst.append(nft.name)
    return nft_lst

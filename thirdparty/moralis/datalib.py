
from thirdparty.moralis.orm import nft_orm
from thirdparty.moralis.nft import get_nft_collection_metadata, get_single_nft_metadata

from thirdparty.moralis.nft_owner import get_nft_owner

from thirdparty.moralis.orm import address_orm, nftbuy_orm, nft_orm,nft_address_orm

def get_nft_info(token_address):
    obj = nft_orm.get_or_none(nft_orm.token_address == token_address)
    if obj:
        return obj
    else:
        i = get_nft_collection_metadata(token_address=token_address)
        nft_orm.create(token_address=i.token_address, name=i.name,
                       symbol=i.symbol, synctime=i.synctime, contract_type=i.contract_type)
        return i



def get_nft_name(token_address, token_id):
    nft = get_nft_info(token_address)
    nft_name = nft.name
    if nft_name == "OpenSea Shared Storefront":
        single_nft = get_single_nft_metadata(token_address=token_address, token_id=token_id)
        nft_name = "Opensea " + single_nft.metadata['name']

    return nft_name


def save_token_addr(token_address):
    obj = nft_address_orm.get_or_none(nft_address_orm.token_address == token_address)
    if obj:
        return None
    else:
        #i = get_account_nft_metadata(token_address=token_address)
        nft_address_orm.create(token_address=token_address)

def save_token_info(nft):
    price = int(nft.price) / 10**18
    price = round(price, 2)
    q = nft_address_orm.update({
        'lastprice': price,
        'transaction_hash': nft.transaction_hash,
        'block_timestamp': nft.block_timestamp,
    }).where(nft_address_orm.token_address == nft.token_address)

    q.execute()

def save_nft_owner(token_address):
    rsp = get_nft_owner(token_address=token_address, limit=10000)
    query = address_orm.delete().where(address_orm.token_address==token_address)
    query.execute()
    for i in rsp:
        # rsp1 = get_account_nft_transfer(address=i.owner, limit=limit, direction='to')
        #if address_orm.get_or_none(address_orm.owner == i.owner):
        #    pass
        #else:
        address_orm.create(owner=i.owner, token_address=i.token_address, name=i.name, amount=i.amount,
                               token_id=i.token_id, synctime=i.synctime, contract_type=i.contract_type)


def save_signle_nft_owner(token_address, nft):
    #rsp = get_nft_owner(token_address=token_address, limit=10000)
    #query = address_orm.delete().where(address_orm.token_address==token_address)
    #query.execute()
    #for i in rsp:
        # rsp1 = get_account_nft_transfer(address=i.owner, limit=limit, direction='to')
        #if address_orm.get_or_none(address_orm.owner == i.owner):
        #    pass
        #else:
    i = nft
    address_orm.create(owner=i.owner, token_address=i.token_address, name=i.name, amount=i.amount,
                               token_id=i.token_id, synctime=i.synctime, contract_type=i.contract_type)
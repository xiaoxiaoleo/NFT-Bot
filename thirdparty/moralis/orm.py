# coding: utf-8
import peewee
from peewee import DateTimeField
import datetime
from playhouse.sqlite_ext import SqliteExtDatabase
from wconfig import DATA_PATH

db = SqliteExtDatabase(DATA_PATH + '/nft.db')

class nft_orm(peewee.Model):
    id = peewee.IntegerField(primary_key=True, unique=True)
    token_address = peewee.CharField(64, default='')
    name = peewee.CharField(64, default='')
    symbol = peewee.CharField(64, default='')
    contract_type = peewee.CharField(20)
    synctime =  peewee.CharField(64, default='')

    created = DateTimeField(default=datetime.datetime.now)
    modified = DateTimeField(default=datetime.datetime.now)


    class Meta:
        database = db

class nft_address_orm(peewee.Model):
    id = peewee.IntegerField(primary_key=True, unique=True)
    token_address = peewee.CharField(64, default='')
    lastprice =  peewee.FloatField(default=0)
    transaction_hash = peewee.CharField(70, default='')
    block_timestamp = DateTimeField(default=datetime.datetime.now)

    modified = DateTimeField(default=datetime.datetime.now)


    class Meta:
        database = db


class address_orm(peewee.Model):
    id = peewee.IntegerField(primary_key=True, unique=True)
    owner = peewee.CharField(64, default='')
    token_address = peewee.CharField(64, default='')
    name = peewee.CharField(64, default='')
    amount = peewee.IntegerField(default=0)
    token_id = peewee.CharField(100)
    contract_type = peewee.CharField(20)
    synctime =  peewee.CharField(64, default='')
    eth_balance = peewee.FloatField(default=0)
    created = DateTimeField(default=datetime.datetime.now)
    modified = DateTimeField(default=datetime.datetime.now)


    class Meta:
        database = db


class nftbuy_orm(peewee.Model):
    id = peewee.IntegerField(primary_key=True, unique=True)
    from_address = peewee.CharField(64)
    to_address = peewee.CharField(64)
    transaction_hash = peewee.CharField(100)
    token_id = peewee.CharField(100)
    token_address = peewee.CharField(64)
    amount = peewee.IntegerField(default=0)
    block_timestamp = peewee.CharField(64)
    created = DateTimeField(default=datetime.datetime.now)
    modified = DateTimeField(default=datetime.datetime.now)
    mark_project = peewee.CharField(64)
    direction = peewee.CharField(10)
    class Meta:
        database = db


db.connect()

#address_orm.drop_table()
#nftbuy_orm.drop_table()
#nftsell_orm.drop_table()
#nft_address_orm.drop_table()

nft_orm.create_table(fail_silently=True)
address_orm.create_table(fail_silently=True)
nftbuy_orm.create_table(fail_silently=True)
nft_address_orm.create_table(fail_silently=True)
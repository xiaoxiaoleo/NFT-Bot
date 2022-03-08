import os
import logging


env_dist = os.environ

DATA_PATH = env_dist.get('DATA_PATH') if env_dist.get('DATA_PATH') else "data"
LOG_PATH = env_dist.get('LOG_PATH') if env_dist.get('LOG_PATH') else f"/tmp/"


LOG_LEVEL = logging.DEBUG


MoralisKey = ['xxx']

CHAIN_PROVIDER = {
    "eth":'https://api.mycryptoapi.com/eth', }

Telegram_Bot =  '5055969351:AAHbCpuFNQKBSoYiF3AARM33Xp'
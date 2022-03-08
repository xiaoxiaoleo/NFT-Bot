import json
import logging
import os
import sys
from logging import handlers
import time
from wconfig import LOG_PATH, LOG_LEVEL

Wei = int
GWei = int
Ether = float
TokenWei = int
Token = float
TxHash = str
AddressType = str

EmptyAddress = '0x0000000000000000000000000000000000000000'

MAX_APPROVAL_HEX: str = '0x' + 'f' * 64
MAX_APPROVAL_INT: int = int('0x' + 'f' * 64, 16)




def get_logger(name):
    logger = logging.getLogger(name)
    fmt = '%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s'
    when = 'D'
    backCount = 10000
    fpath = os.path.join(LOG_PATH, name)
    logger.setLevel(LOG_LEVEL)
    if not logger.handlers:
        # Prevent logging from propagating to the root logger
        logger.propagate = 0
        console = logging.StreamHandler()
        logger.addHandler(console)
        formatter = logging.Formatter(fmt)
        console.setFormatter(formatter)
        format_str = logging.Formatter(fmt)  # 设置日志格式
        th = handlers.TimedRotatingFileHandler(filename=fpath, when=when, backupCount=backCount,
                                               encoding='utf-8')  # 往文件里写入#指定间隔时间自动生成文件的处理器
        th.setFormatter(format_str)  # 设置文件里写入的格式
        logger.addHandler(th)  # 把对象加到logger里
    return logger


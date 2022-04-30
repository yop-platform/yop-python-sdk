# -*- coding: utf-8 -*-

# @title : 封装数字信封、拆开数字信封、签名、验签的工具类
# @Author : zhanglele
# @Date : 18/6/14
# @Desc :

from builtins import range
import base64
from Crypto.PublicKey import RSA
from yop_python_sdk.security.crc64 import Crc64
import yop_python_sdk.utils.yop_logger as yop_logger

try:
    from importlib import reload
except ImportError:
    # fix: 'ascii' codec can't decode byte 0xe6 in position 68
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")

# 摘要算法，默认为sha256(参照配置文件)

logger = yop_logger.get_logger(__name__)

# AES根据16位对齐
BS = 16


def parse_rsa_pri_key(private_key_string):
    """
    Parse RSA private key string.

    Args:
        private_key_string: write your description
    """
    private_key = '-----BEGIN PRIVATE KEY-----\n' + \
        private_key_string + '\n-----END PRIVATE KEY-----'
    return RSA.importKey(private_key)


def parse_rsa_pub_key(public_key_string):
    """
    Parse a public key string into an RSA key object.

    Args:
        public_key_string: write your description
    """
    public_key = '-----BEGIN PUBLIC KEY-----\n' + \
        public_key_string + '\n-----END PUBLIC KEY-----'
    return RSA.importKey(public_key)


def decode_base64(data):
    '''
    base64解码
    '''
    missing_padding = 4 - len(data) % 4
    if missing_padding:
        data += '=' * missing_padding
    return base64.urlsafe_b64decode(data)


def encode_base64(data):
    '''
    base64编码
    '''
    data = base64.urlsafe_b64encode(data)
    for i in range(3):
        if data.endswith('='.encode('latin-1')):
            data = data[:-1]
    return data.decode()


def cal_file_crc64(file, block_size=64 * 1024, init_crc=0):
    """
    Calculate the CRC64 checksum of a file.

    Args:
        file: write your description
        block_size: write your description
        init_crc: write your description
    """
    crc64 = Crc64(init_crc)
    file.seek(0)
    while True:
        data = file.read(block_size)
        if not data:
            break
        crc64.update(data)
    return crc64.crc

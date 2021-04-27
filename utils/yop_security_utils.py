# -*- coding: utf-8 -*-

# @title : 封装数字信封、拆开数字信封、签名、验签的工具类
# @Author : zhanglele
# @Date : 18/6/14
# @Desc :

from builtins import range
from builtins import bytes
import base64
import hashlib
# from Crypto import Random
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from utils.crc64 import Crc64
import utils.yop_logging_utils as yop_logging_utils

try:
    from importlib import reload
except ImportError:
    # fix: 'ascii' codec can't decode byte 0xe6 in position 68
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")

# 摘要算法，默认为sha256(参照配置文件)

logger = yop_logging_utils.get_logger(__name__)

# AES根据16位对齐
BS = 16


def parse_pri_key(private_key_string):
    private_key = '-----BEGIN PRIVATE KEY-----\n' + private_key_string + '\n-----END PRIVATE KEY-----'
    return RSA.importKey(private_key)


def parse_pub_key(public_key_string):
    public_key = '-----BEGIN PUBLIC KEY-----\n' + public_key_string + '\n-----END PUBLIC KEY-----'
    return RSA.importKey(public_key)


# def verify_rsa(content, signature, public_key, alg_name=SHA256):
#     # RSA 非对称验签
#     h = SHA256.new(bytes(content, encoding='utf-8'))
#     verifier = PKCS1_v1_5.new(public_key)
#     return verifier.verify(h, decode_base64(signature))


def sign_aes(content, secret_key, alg_name='sha256'):
    # 对称签名
    to_sign_str = ''.join([secret_key, content, secret_key])
    __alg_func = getattr(hashlib, alg_name)
    signature = __alg_func(to_sign_str).hexdigest()
    return signature


def verify_aes(content, signature, secret_key, alg_name='sha256'):
    # 对称验签
    to_sign_str = ''.join([secret_key, content, secret_key])
    __alg_func = getattr(hashlib, alg_name)
    verify = __alg_func(to_sign_str).hexdigest()
    return verify == signature


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
    return data


def cal_file_crc64(file, block_size=64 * 1024, init_crc=0):
    crc64 = Crc64(init_crc)
    file.seek(0)
    while True:
        data = file.read(block_size)
        if not data:
            break
        crc64.update(data)
    return crc64.crc

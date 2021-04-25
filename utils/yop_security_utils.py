# -*- coding: utf-8 -*-

# @title : 封装数字信封、拆开数字信封、签名、验签的工具类
# @Author : zhanglele
# @Date : 18/6/14
# @Desc :

from builtins import range
from builtins import bytes
import os
import base64
import hashlib
from Crypto import Random
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from utils.crc64 import Crc64
import utils.yop_logging_utils as yop_logging_utils
from Crypto.Cipher import AES
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Util.Padding import pad, unpad
BLOCK_SIZE = 32  # Bytes
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

# 伪随机数生成器
random_generator = Random.new().read


def parse_pri_key(private_key_string):
    private_key = '-----BEGIN PRIVATE KEY-----\n' + private_key_string + '\n-----END PRIVATE KEY-----'
    return RSA.importKey(private_key)


def parse_pub_key(public_key_string):
    public_key = '-----BEGIN PUBLIC KEY-----\n' + public_key_string + '\n-----END PUBLIC KEY-----'
    return RSA.importKey(public_key)


def sign_rsa(content, private_key, alg_name=SHA256):
    # RSA 非对称签名
    h = SHA256.new(bytes(content, encoding='utf-8'))
    signer = PKCS1_v1_5.new(private_key)
    signature = signer.sign(h)
    return encode_base64(signature)


def verify_rsa(content, signature, public_key, alg_name=SHA256):
    # RSA 非对称验签
    h = SHA256.new(bytes(content, encoding='utf-8'))
    verifier = PKCS1_v1_5.new(public_key)
    return verifier.verify(h, decode_base64(signature))


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


def envelope_encrypt(content, private_key, public_key, alg_name=SHA256):
    # 封装数字信封

    # 生成随机密钥
    # random_key1 = 'kLNl5Q7MOV0FRw_dl1VDPg'
    # logger.debug('random_key:{}'.format(random_key))

    random_key = get_random_key_readable(16)
    logger.debug('random_key type:{}, random_key value:{}\n'.format(type(random_key), random_key))

    # 用随机密钥对数据和签名进行加密
    cipher = AES.new(random_key, AES.MODE_ECB)
    # 对数据进行签名
    sign_to_base64 = sign_rsa(content, private_key, alg_name)
    encrypted_data = cipher.encrypt(pad(content + '$' + sign_to_base64, BLOCK_SIZE))
    encrypted_data = encode_base64(encrypted_data)

    # 对密钥加密
    cipher = Cipher_pkcs1_v1_5.new(public_key)
    encrypted_random_key = encode_base64(cipher.encrypt(random_key))
    cigher_text = [encrypted_random_key]
    cigher_text.append(encrypted_data)
    cigher_text.append('AES')
    cigher_text.append('SHA256')
    return '$'.join(cigher_text)


def envelope_decrypt(content, private_key, public_key, alg_name=SHA256):
    # 拆开数字信封
    args = content.split('$')
    if len(args) != 4:
        raise Exception("source invalid", args)

    # 分解参数
    encrypted_random_key = decode_base64(args[0])
    encrypted_data = decode_base64(args[1])
    # symmetric_encrypt_alg = args[2]
    digest_alg = args[3]

    # 用私钥对随机密钥进行解密
    cipher = Cipher_pkcs1_v1_5.new(private_key)
    random_key = cipher.decrypt(encrypted_random_key, random_generator)
    if random_key == random_generator:
        raise Exception("isv private key is illegal!")

    cipher = AES.new(random_key, AES.MODE_ECB)
    data = unpad(cipher.decrypt(encrypted_data), BLOCK_SIZE)

    # 分解参数
    data = data.split('$')
    source_data = data[0]
    signature = data[1].rstrip('\n')
    verify_sign = verify_rsa(source_data, signature, public_key, digest_alg)
    if not verify_sign:
        raise Exception("verifySign fail!")
    return source_data


def get_random_key_readable(key_size=16):
    # 生成随机密钥
    ulen = int(key_size // 4 * 3)
    key = base64.b64encode(os.urandom(ulen))
    return key


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

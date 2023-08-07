# -*- coding: utf-8 -*-

import base64
import os
from builtins import bytes

from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5

import yop_python_sdk.utils.yop_logger as yop_logger
import yop_python_sdk.utils.yop_security_utils as yop_security_utils
from yop_python_sdk.security.ecdsa.utils.compatibility import pad, unpad
from . import encryptor

YOP_RSA_ALGORITHM = 'YOP-RSA2048-SHA256'

# 伪随机数生成器
random_generator = Random.new().read


class RsaEncryptor(encryptor.Encryptor):
    '''
    RSA 加密机接口
    '''

    def __init__(self, private_key=None, public_key=None):
        """
        Initializes the instance with the appropriate logger and private key.

        Args:
            self: write your description
            private_key: write your description
            public_key: write your description
        """
        self.logger = yop_logger.get_logger()
        self.private_key = private_key
        self.public_key = public_key

    def get_random_key_readable(self, key_size=16):
        """
        Generate a random key that can be used for authentication.

        Args:
            self: write your description
            key_size: write your description
        """
        # 生成随机密钥
        ulen = int(key_size // 4 * 3)
        key = base64.b64encode(os.urandom(ulen))
        return key

    def signature(self, data, private_key=None):
        '''
        RSA 非对称签名
        '''
        if private_key is None:
            private_key = self.private_key

        h = SHA256.new(bytes(data, encoding='utf-8'))
        signer = PKCS1_v1_5.new(private_key)
        signature = signer.sign(h)
        return yop_security_utils.encode_base64(signature), YOP_RSA_ALGORITHM, "SHA256"

    def verify_signature(self, data, signature, public_key=None, serial_no=None):
        '''
        RSA 非对称验签
        '''
        if public_key is None:
            public_key = self.public_key
        elif public_key is dict and serial_no is not None:
            public_key = public_key.get(serial_no)

        h = SHA256.new(bytes(data, encoding='utf-8'))
        verifier = PKCS1_v1_5.new(public_key)
        return verifier.verify(h, yop_security_utils.decode_base64(signature))

    def envelope_encrypt(self, content, private_key=None, public_key=None):
        """
        Encrypts the content with the given private key and public key.

        Args:
            self: write your description
            content: write your description
            private_key: write your description
            public_key: write your description
        """
        # 封装数字信封

        if None is private_key:
            private_key = self.private_key

        if None is public_key:
            public_key = self.public_key

        random_key = self.get_random_key_readable(16)
        self.logger.debug('random_key type:{}, random_key value:{}\n'.format(
            type(random_key), random_key))

        # 用随机密钥对数据和签名进行加密
        cipher = AES.new(random_key, AES.MODE_ECB)
        # 对数据进行签名
        sign_to_base64, algorithm, hash_algorithm = self.signature(
            content, private_key)
        encrypted_data = cipher.encrypt(
            pad(content + '$' + sign_to_base64, 16))
        encrypted_data = yop_security_utils.encode_base64(encrypted_data)

        # 对密钥加密
        cipher = Cipher_pkcs1_v1_5.new(public_key)
        encrypted_random_key = yop_security_utils.encode_base64(
            cipher.encrypt(random_key))
        cigher_text = [encrypted_random_key]
        cigher_text.append(encrypted_data)
        cigher_text.append(u'AES')
        cigher_text.append(hash_algorithm)
        return '$'.join(cigher_text)

    def envelope_decrypt(self, content, private_key=None, public_key=None):
        """
        Decrypt Envelope Decryption

        Args:
            self: write your description
            content: write your description
            private_key: write your description
            public_key: write your description
        """
        # 拆开数字信封
        args = content.split('$')
        if len(args) != 4:
            raise Exception("source invalid", args)

        if None is private_key:
            private_key = self.private_key

        if None is public_key:
            public_key = self.public_key

        # 分解参数
        encrypted_random_key = yop_security_utils.decode_base64(args[0])
        encrypted_data = yop_security_utils.decode_base64(args[1])
        # symmetric_encrypt_alg = args[2]
        # digest_alg = args[3]

        # 用私钥对随机密钥进行解密
        cipher = Cipher_pkcs1_v1_5.new(private_key)
        random_key = cipher.decrypt(encrypted_random_key, random_generator)
        if random_key == random_generator:
            raise Exception("isv private key is illegal!")

        cipher = AES.new(random_key, AES.MODE_ECB)
        data = cipher.decrypt(encrypted_data)

        # 对 pkcs7 格式的数据做特殊处理
        data = unpad(data, len(random_key))

        # 分解参数
        data = data.rsplit('$', 1)
        source_data = data[0]
        signature = data[1].rstrip('\n')
        verify_sign = self.verify_signature(source_data, signature, public_key)
        if not verify_sign:
            raise Exception("verifySign fail!")
        return source_data

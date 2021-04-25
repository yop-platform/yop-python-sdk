# -*- coding: utf-8 -*-

import binascii
from utils.security.gmssl import sm2
import utils.security.encryptor as encryptor
import utils.yop_logging_utils as yop_logging_utils
import utils.yop_security_utils as yop_security_utils

class SmEncryptor(encryptor.Encryptor):
    '''
    SM 加密机接口
    '''

    def __init__(self, private_key, public_key):
        self.logger = yop_logging_utils.get_logger()
        self.sm2_crypt = sm2.CryptSM2(public_key=public_key, private_key=private_key)

    def signature(self, data):
        '''
        RSA 非对称签名
        '''
        sign_16 = self.sm2_crypt.sign_with_sm3(data)
        sign_bytes = binascii.unhexlify(sign_16)
        sign_base64 = yop_security_utils.encode_base64(sign_bytes)
        return sign_base64

    def verify_signature(self, signature, data):
        '''
        RSA 非对称验签
        '''
        sign_bytes = yop_security_utils.decode_base64(signature)
        sign_16 = binascii.hexlify(sign_bytes)
        return self.sm2_crypt.verify_with_sm3(sign_16, data)

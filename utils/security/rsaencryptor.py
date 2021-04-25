# -*- coding: utf-8 -*-

import utils.security.encryptor as encryptor
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
import utils.yop_logging_utils as yop_logging_utils
import utils.yop_security_utils as yop_security_utils
from builtins import bytes


class RsaEncryptor(encryptor.Encryptor):
    '''
    RSA 加密机接口
    '''

    def __init__(self, private_key, public_key):
        self.logger = yop_logging_utils.get_logger()
        self.public_key = public_key
        self.private_key = private_key

    def signature(self, data):
        '''
        RSA 非对称签名
        '''
        h = SHA256.new(bytes(data, encoding='utf-8'))
        signer = PKCS1_v1_5.new(self.private_key)
        signature = signer.sign(h)
        return yop_security_utils.encode_base64(signature)

    def verify_signature(self, data, signature):
        '''
        RSA 非对称验签
        '''
        h = SHA256.new(bytes(data, encoding='utf-8'))
        verifier = PKCS1_v1_5.new(self.public_key)
        return verifier.verify(h, signature)

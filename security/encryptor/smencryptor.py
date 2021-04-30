# -*- coding: utf-8 -*-

import binascii
from ..gmssl import sm2
from . import encryptor
import utils.yop_logging_utils as yop_logging_utils
import utils.yop_security_utils as yop_security_utils
from security.ecdsa.privateKey import PrivateKey

YOP_SM_ALGORITHM = 'YOP-SM2-SM3'


class SmEncryptor(encryptor.Encryptor):
    '''
    SM 加密机接口
    '''

    def __init__(self, private_key=None, public_key_dict=None):
        self.logger = yop_logging_utils.get_logger()
        self.sm2_crypt = sm2.CryptSM2()

        # 如果是商户自己的加密机
        if private_key is not None:
            self.private_key = str(hex(private_key.secret))[2:-1]
            self.public_key = private_key.publicKey().toStr()

        # 如果是YOP的加密机
        if public_key_dict is not None:
            self.yop_public_key_dict = public_key_dict

    def signature(self, data, private_key=None):
        '''
        RSA 非对称签名
        '''
        if private_key is None:
            private_key = self.private_key

        sign_16 = self.sm2_crypt.sign_with_sm3(data, self.public_key, private_key)
        sign_bytes = binascii.unhexlify(sign_16)
        sign_base64 = yop_security_utils.encode_base64(sign_bytes)
        return sign_base64, YOP_SM_ALGORITHM, "SM3"

    def verify_signature(self, data, signature, public_key=None, serial_no=None):
        '''
        RSA 非对称验签
        '''
        sign_bytes = yop_security_utils.decode_base64(signature)
        sign_16 = binascii.hexlify(sign_bytes)

        if public_key is None:
            if self.yop_public_key_dict is None:
                public_key = self.public_key
            elif not isinstance(self.yop_public_key_dict, dict):
                public_key = self.yop_public_key_dict
            else:
                if serial_no is None:
                    public_key = self.yop_public_key_dict.values()[0]
                else:
                    public_key = self.yop_public_key_dict.get(serial_no)

        return self.sm2_crypt.verify_with_sm3(sign_16, data, public_key)

# -*- coding: utf-8 -*-

from security.ecdsa.privateKey import PrivateKey
from security.encryptor.rsaencryptor import RsaEncryptor
from security.encryptor.smencryptor import SmEncryptor
from Crypto.PublicKey import RSA


class YopCredentials:
    def __init__(self, appKey=None, priKey=None, cert_type='SM2'):
        self.appKey = appKey
        self.cert_type = cert_type

        if isinstance(priKey, str):
            if cert_type.startswith('SM'):
                self.priKey = PrivateKey.fromPem(priKey)
            else:
                self.priKey = RSA.importKey('-----BEGIN PRIVATE KEY-----\n' +
                                            priKey +
                                            '\n-----END PRIVATE KEY-----')
        else:
            self.priKey = priKey

        if cert_type.startswith('SM'):
            self.encryptor = SmEncryptor(private_key=self.priKey)
        else:
            self.encryptor = RsaEncryptor(private_key=self.priKey)

    def get_appKey(self):
        return self.appKey

    def get_priKey(self):
        return self.priKey

    def get_cert_type(self):
        return self.cert_type

# -*- coding: utf-8 -*-

from yop_python_sdk.security.ecdsa.privateKey import PrivateKey
from yop_python_sdk.security.encryptor.rsaencryptor import RsaEncryptor
from yop_python_sdk.security.encryptor.smencryptor import SmEncryptor
from Crypto.PublicKey import RSA


class YopCredentials:
    def __init__(self, appKey=None, priKey=None, cert_type='SM2'):
        """
        PKCS12 PKCS12 PKCS12 PKCS12 PKCS

        Args:
            self: write your description
            appKey: write your description
            priKey: write your description
            cert_type: write your description
        """
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
        """
        Return the appKey for this device.

        Args:
            self: write your description
        """
        return self.appKey

    def get_priKey(self):
        """
        Return the priKey as a string

        Args:
            self: write your description
        """
        return self.priKey

    def get_cert_type(self):
        """
        Return the certificate type.

        Args:
            self: write your description
        """
        return self.cert_type

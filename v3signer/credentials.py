# -*- coding: utf-8 -*-

class YopCredentials:
    def __init__(self, appKey=None, priKey=None, cert_type='SM2'):
        self.appKey = appKey
        self.priKey = priKey
        self.cert_type = cert_type

    def get_appKey(self):
        return self.appKey

    def get_priKey(self):
        return self.priKey

    def get_cert_type(self):
        return self.cert_type

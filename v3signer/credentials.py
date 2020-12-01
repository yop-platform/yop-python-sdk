# -*- coding: utf-8 -*-

import utils.yop_security_utils as yop_security_utils


class YopCredentials:
    def __init__(self, appKey=None, priKey=None):
        self.appKey = appKey
        if isinstance(priKey, str):
            priKey = yop_security_utils.parse_pri_key(priKey)
        self.priKey = priKey

    def get_appKey(self):
        return self.appKey

    def get_priKey(self):
        return self.priKey

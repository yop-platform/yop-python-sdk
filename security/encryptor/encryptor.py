# -*- coding: utf-8 -*-

import utils.yop_logger as yop_logger


class Encryptor:
    '''
    加密机接口
    '''

    def __init__(self):
        self.logger = yop_logger.get_logger()

    def signature(self, data):
        return "", "", ""

    def verify_signature(self, data, signature, serial_no=None):
        return "", "", ""

# -*- coding: utf-8 -*-

import utils.yop_logging_utils as yop_logging_utils


class Encryptor:
    '''
    加密机接口
    '''

    def __init__(self):
        self.logger = yop_logging_utils.get_logger()

    def signature(self, data):
        return ""

    def verify_signature(self, data, signature):
        return ""

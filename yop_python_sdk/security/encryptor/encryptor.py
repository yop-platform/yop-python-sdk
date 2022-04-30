# -*- coding: utf-8 -*-

import yop_python_sdk.utils.yop_logger as yop_logger


class Encryptor:
    '''
    加密机接口
    '''

    def __init__(self):
        """
        Initialize the yop logger

        Args:
            self: write your description
        """
        self.logger = yop_logger.get_logger()

    def signature(self, data):
        """
        Signature is a JSON object with the form

        Args:
            self: write your description
            data: write your description
        """
        return "", "", ""

    def verify_signature(self, data, signature, serial_no=None):
        """
        Verifies the signature of the data.

        Args:
            self: write your description
            data: write your description
            signature: write your description
            serial_no: write your description
        """
        return "", "", ""

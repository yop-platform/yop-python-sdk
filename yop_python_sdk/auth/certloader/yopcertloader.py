# -*- coding: utf-8 -*-

import yop_python_sdk.utils.yop_logger as yop_logger


class YopCertLoader:
    clientConfig = None

    def __init__(self, clientConfig=None, env=None):
        """
        Initializes the SDK client

        Args:
            self: self
            clientConfig: config of client
            env: run env
        """
        self.logger = yop_logger.get_logger()
        self.path = clientConfig.sdk_config.get(
            'yop_cert_store', '/tmp').get('path', '/tmp')
        self.env = env

    def load(self, serial_no):
        '''
        从YOP加载证书
        '''
        self.logger.error(
            "本版本的SDK尚未实现从YOP平台加载证书还没有实现，请自行实现或升级到最新版本, serial_no:{}".format(serial_no))
        return serial_no

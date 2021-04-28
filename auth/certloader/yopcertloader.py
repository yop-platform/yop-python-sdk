# -*- coding: utf-8 -*-
#!/usr/bin/env python

class YopCertLoader:
    clientConfig = None

    def __init__(self, clientConfig=None, env=None):
        self.path = clientConfig.sdk_config.get('yop_cert_store', '/tmp').get('path', '/tmp')

    def load(serial_no):
        '''
        从YOP加载证书
        '''
        return serial_no

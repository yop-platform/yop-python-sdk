# -*- coding: utf-8 -*-

# @title : 封装数字信封、拆开数字信封、签名、验签的工具类
# @Author : zhanglele
# @Date : 18/6/14
# @Desc :
from v3signer.credentials import YopCredentials
import utils.yop_security_utils as security_utils
import simplejson
import utils.yop_logging_utils as yop_logging_utils


class YopClientConfig:
    def __init__(self, config_file='config/yop_sdk_config_rsa_default.json'):
        self.logger = yop_logging_utils.get_logger()
        self.config_file = config_file
        self.sdk_config = self._init_config(config_file)

    def _init_config(self, config_file):
        # 获取配置文件信息
        with open(config_file, 'r') as f:
            sdk_config = simplejson.load(f)
            app_key = sdk_config['app_key']
            isv_private_key_list = sdk_config['isv_private_key']
            for isv_private_key in isv_private_key_list:
                credentials = self._parse_isv_private_key(app_key, isv_private_key)
                if credentials is not None:
                    sdk_config['credentials'] = credentials
                    break

            yop_public_key_list = sdk_config['yop_public_key']
            for yop_public_key in yop_public_key_list:
                yop_public_key = self._parse_yop_public_key(yop_public_key)
                if yop_public_key is not None:
                    sdk_config['yop_public_key'] = yop_public_key
                    break

        return sdk_config

    def _parse_isv_private_key(self, appKey, config):
        store_type = config['store_type']
        cert_type = config['cert_type']
        if 'string' == store_type:
            private_key_string = config['value']
            if cert_type.startswith('RSA'):
                private_key = security_utils.parse_pri_key(private_key_string)
            else:
                private_key = private_key_string
            return YopCredentials(appKey, private_key)
        else:
            self.logger.warn('暂时不支持的密钥类型 {}'.format(store_type))
            return None

    def _parse_yop_public_key(self, config):
        store_type = config['store_type']
        cert_type = config['cert_type']
        if 'string' == store_type:
            public_key_string = config['value']
            if cert_type.startswith('RSA'):
                yop_public_key = security_utils.parse_pub_key(public_key_string)
            else:
                yop_public_key = public_key_string
            return yop_public_key
        else:
            self.logger.warn('暂时不支持的密钥类型 {}'.format(store_type))
            return None

    def get_server_root(self):
        """
        docstring
        """
        return self.sdk_config['server_root']

    def get_yos_server_root(self):
        """
        docstring
        """
        return self.sdk_config['yos_server_root']

    def get_sandbox_server_root(self):
        """
        docstring
        """
        return self.sdk_config['sandbox_server_root']

    def get_credentials(self, appKey=None):
        return self.sdk_config['credentials']

    def get_yop_public_key(self):
        return self.sdk_config['yop_public_key']

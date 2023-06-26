# -*- coding: utf-8 -*-

from yop_python_sdk.security.ecdsa.publicKey import PublicKey
from yop_python_sdk.security.ecdsa.privateKey import PrivateKey
import OpenSSL
from yop_python_sdk.auth.v3signer.credentials import YopCredentials
import simplejson
import yop_python_sdk.utils.yop_logger as yop_logger
from Crypto.PublicKey import RSA
from . import client_config


class YopClientConfig(client_config.ClientConfig):

    def __init__(self, config_file='config/yop_sdk_config_rsa_prod.json'):
        """
        Initializes the SDK.

        Args:
            self: write your description
            config_file: write your description
        """
        self.logger = yop_logger.get_logger()
        self.config_file = config_file
        self.sdk_config = self._init_config(config_file)

    def _init_config(self, config_file):
        """
         config_file

        Args:
            self: write your description
            config_file: write your description
        """
        # 获取配置文件信息
        with open(config_file, 'r') as f:
            sdk_config = simplejson.load(f)
            app_key = sdk_config.get('app_key', '')

            # platform public key
            yop_public_key_dict = {}
            yop_public_key_list = sdk_config['yop_public_key']
            for yop_public_key_str in yop_public_key_list:
                yop_public_key, cert_type, serial_no = self._parse_yop_public_key(
                    yop_public_key_str)
                dict1 = yop_public_key_dict.setdefault(cert_type, {})
                dict1[serial_no] = yop_public_key
            sdk_config['yop_public_key'] = yop_public_key_dict

            # isv private key
            credentials_dict = {}
            isv_private_key_list = sdk_config['isv_private_key']
            for isv_private_key in isv_private_key_list:
                credentials = self._parse_isv_private_key(
                    app_key, isv_private_key)
                credentials_dict[credentials.appKey] = credentials
                # 仅支持一个私钥，避免请求时不知道用哪个私钥签名
                if credentials is not None:
                    sdk_config['credentials'] = credentials_dict
                    break

            # http client
            http_client_dict = sdk_config['http_client']
            connect_timeout, read_timeout, max_conn_total, max_conn_per_route = self._parse_http_client(http_client_dict)
            http_client_dict['connect_timeout'] = connect_timeout
            http_client_dict['read_timeout'] = read_timeout
            http_client_dict['max_conn_total'] = max_conn_total
            http_client_dict['max_conn_per_route'] = max_conn_per_route
            sdk_config['http_client'] = http_client_dict

        return sdk_config

    def _parse_isv_private_key(self, appKey, config):
        """
        Parse the isv private key and return YopCredentials object.

        Args:
            self: write your description
            appKey: write your description
            config: write your description
        """
        store_type = config.get('store_type', 'string')
        cert_type = config.get('cert_type', 'RSA2048')
        appKey = config.get('app_key', appKey)
        return super(YopClientConfig, self)._parse_isv_pri_key(appKey, config['value'], store_type,
                                                               cert_type)

    def _parse_yop_public_key(self, config):
        """
        Parse the yop public key from a config file.

        Args:
            self: write your description
            config: write your description
        """
        store_type = config.get('store_type', 'string')
        cert_type = config.get('cert_type', 'RSA2048')
        serial_no = config.get('serial_no', 'unknown')
        return super(YopClientConfig, self)._parse_yop_pub_key(config['value'],
                                                               store_type,
                                                               cert_type,
                                                               serial_no)

    def _parse_http_client(self, config):
        """
        Parse the http client from a config file.

        Args:
            self: write your description
            config: write your description
        """
        connect_timeout = config.get('connect_timeout', 10000)
        read_timeout = config.get('read_timeout', 30000)
        max_conn_total = config.get('max_conn_total', 200)
        max_conn_per_route = config.get('max_conn_per_route', 100)
        return super(YopClientConfig, self)._parse_http_client(connect_timeout,
                                                               read_timeout,
                                                               max_conn_total,
                                                               max_conn_per_route)

    def get_http_client(self):
        """
        docstring
        """
        return self.sdk_config['http_client']

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
        """
        Get credentials for SDK.

        Args:
            self: write your description
            appKey: write your description
        """
        if appKey is None:
            return list(self.sdk_config['credentials'].values())[0]
        else:
            return self.sdk_config['credentials'].get(appKey)

    def get_yop_public_key(self):
        """
        Get Yoop public key

        Args:
            self: write your description
        """
        return self.sdk_config['yop_public_key']

# -*- coding: utf-8 -*-

from yop_python_sdk.security.ecdsa.publicKey import PublicKey
from yop_python_sdk.security.ecdsa.privateKey import PrivateKey
import OpenSSL
from yop_python_sdk.auth.v3signer.credentials import YopCredentials
import yop_python_sdk.utils.yop_logger as yop_logger
from Crypto.PublicKey import RSA


class ClientConfig(object):

    def __init__(self):
        """
        Initializes the SDK.

        Args:
            self: write your description
            config_file: write your description
        """
        self.logger = yop_logger.get_logger()

    def _parse_isv_pri_key(self, appKey, pri_key_value, store_type, cert_type):
        """
        Parse the isv private key and return YopCredentials object.

        Args:
            self: write your description
            appKey: write your description
            config: write your description
        """
        if 'string' == store_type:
            if cert_type.startswith('RSA'):
                private_key = RSA.importKey('-----BEGIN PRIVATE KEY-----\n' +
                                            pri_key_value +
                                            '\n-----END PRIVATE KEY-----')
            else:
                private_key = PrivateKey.fromPem(pri_key_value)
            return YopCredentials(appKey=appKey,
                                  priKey=private_key,
                                  cert_type=cert_type)
        else:
            self.logger.warn('暂时不支持的密钥类型 {}'.format(store_type))
            return None

    def _parse_yop_pub_key(self, pub_key_value, store_type, cert_type,
                           serial_no):
        """
        Parse the yop public key from a config file.

        Args:
            self: write your description
            config: write your description
        """
        if 'string' == store_type:
            if cert_type.startswith('RSA'):
                yop_public_key = RSA.importKey('-----BEGIN PUBLIC KEY-----\n' +
                                               pub_key_value +
                                               '\n-----END PUBLIC KEY-----')
            else:
                yop_public_key = PublicKey.fromPem(pub_key_value).toStr()
        elif 'file_cer' == store_type:
            yop_public_key = self.cer_analysis(pub_key_value)
            if cert_type.startswith('RSA'):
                yop_public_key = RSA.importKey(yop_public_key)
            else:
                yop_public_key = PublicKey.fromPem(yop_public_key).toStr()
        else:
            self.logger.warn('暂时不支持的密钥类型 {}'.format(store_type))
            yop_public_key = None

        return yop_public_key, cert_type, serial_no

    def _parse_http_client(self, connect_timeout, read_timeout, max_conn_total, max_conn_per_route):
        """
        Parse the http client key from a config file.

        Args:
            self: write your description
            config: write your description
        """
        try:
            connect_timeout = self.check_is_number(connect_timeout)
            read_timeout = self.check_is_number(read_timeout)
            max_conn_total = self.check_is_number(max_conn_total)
            max_conn_per_route = self.check_is_number(max_conn_per_route)
        except Exception as e:
            self.logger.error(e)
            raise e
        return connect_timeout, read_timeout, max_conn_total, max_conn_per_route

    def check_is_number(self, value):
        if (isinstance(value, int) or isinstance(value, float)) and value > 0:
            return value
        else:
            raise Exception("value must be int or float type and > 0, value: {}".format(value))

    def cer_analysis(self, ceradd):
        '''
        解析证书文件
        '''
        file = open(ceradd)
        file_context = file.read()
        cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM,
                                               file_context)

        certIssue = cert.get_issuer()
        version = cert.get_version() + 1
        serial_no = cert.get_serial_number()
        # signature = cert.get_signature_algorithm().decode("UTF-8")
        comname = certIssue.commonName
        starttime = cert.get_notBefore()
        endtime = cert.get_notAfter()
        flag = cert.has_expired()
        # long = cert.get_pubkey().bits()
        public = OpenSSL.crypto.dump_publickey(
            OpenSSL.crypto.FILETYPE_PEM, cert.get_pubkey()).decode("utf-8")
        # ext = cert.get_extension_count()
        # components = certIssue.get_components()

        self.logger.info(
            "comname:{}\nversion:{}\nserial_no:{}\nstarttime:{}\nendtime:{}\nexpired:{}\n{}"
            .format(comname, version, serial_no, starttime, endtime, flag,
                    public))
        file.close()
        return public

    def get_server_root(self):
        """
        docstring
        """
        return ""

    def get_yos_server_root(self):
        """
        docstring
        """
        return ""

    def get_sandbox_server_root(self):
        """
        docstring
        """
        return ""

    def get_credentials(self, appKey=None):
        """
        Get credentials for SDK.

        Args:
            self: write your description
            appKey: write your description
        """
        return ""

    def get_yop_public_key(self):
        """
        Get Yoop public key

        Args:
            self: write your description
        """
        return ""

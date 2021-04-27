# -*- coding: utf-8 -*-

import OpenSSL
from dateutil import parser
import base64
import binascii
from v3signer.credentials import YopCredentials
import simplejson
import utils.yop_logging_utils as yop_logging_utils
from Crypto.PublicKey import RSA


class YopClientConfig:
    def __init__(self, config_file='config/yop_sdk_config_rsa_prod.json'):
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
                private_key = RSA.importKey('-----BEGIN PRIVATE KEY-----\n' +
                                            private_key_string +
                                            '\n-----END PRIVATE KEY-----')
            else:
                # private_key = self.cert2pem(private_key_string)
                private_key = private_key_string
            return YopCredentials(appKey, private_key, cert_type)
        else:
            self.logger.warn('暂时不支持的密钥类型 {}'.format(store_type))
            return None

    def _parse_yop_public_key(self, config):
        store_type = config['store_type']
        cert_type = config['cert_type']
        if 'string' == store_type:
            public_key_string = config['value']
            if cert_type.startswith('RSA'):
                yop_public_key = RSA.importKey(
                    '-----BEGIN PUBLIC KEY-----\n' +
                    public_key_string +
                    '\n-----END PUBLIC KEY-----')
            else:
                yop_public_key = public_key_string
        elif 'file_cer' == store_type:
            cert_file = config['value']
            if cert_type.startswith('RSA'):
                yop_public_key = RSA.importKey(self.cer_analysis(cert_file))
            else:
                yop_public_key = self.cer_analysis(cert_file)
                yop_public_key = self.cert2pem(yop_public_key)
        else:
            self.logger.warn('暂时不支持的密钥类型 {}'.format(store_type))
            yop_public_key = None
        self.cert_type = cert_type
        return yop_public_key

    def cer_analysis(self, ceradd):
        '''
        解析证书文件
        '''
        file_context = open(ceradd).read()
        cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, file_context)

        certIssue = cert.get_issuer()
        version = cert.get_version() + 1
        sernum = cert.get_serial_number()
        # signature = cert.get_signature_algorithm().decode("UTF-8")
        comname = certIssue.commonName
        datetime_struct = parser.parse(cert.get_notBefore().decode("UTF-8"))
        starttime = datetime_struct.strftime('%Y-%m-%d %H:%M:%S')
        datetime_struct = parser.parse(cert.get_notAfter().decode("UTF-8"))
        endtime = datetime_struct.strftime('%Y-%m-%d %H:%M:%S')
        flag = cert.has_expired()
        # long = cert.get_pubkey().bits()
        public = OpenSSL.crypto.dump_publickey(OpenSSL.crypto.FILETYPE_PEM, cert.get_pubkey()).decode("utf-8")
        # ext = cert.get_extension_count()
        # components = certIssue.get_components()

        self.logger.info(
            "certIssue:{}, comname:{}, version:{}, sernum:{}, starttime:{}, endtime:{}, expired:{}\npublic:{}".format(
                certIssue,
                comname,
                version,
                sernum,
                starttime,
                endtime,
                flag,
                public))
        return public

    def cert2pem(self, pem_data):
        # lines = pem_data.replace(" ", '').split()
        # line = ''.join(lines[1:-1])
        line = "".join([l.strip() for l in pem_data.splitlines() if l and not l.startswith("-----")])

        base64_line = base64.standard_b64decode(line)
        return binascii.hexlify(base64_line)

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

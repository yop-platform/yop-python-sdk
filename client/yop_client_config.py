# -*- coding: utf-8 -*-

from security.ecdsa.publicKey import PublicKey
from security.ecdsa.privateKey import PrivateKey
import OpenSSL
from auth.v3signer.credentials import YopCredentials
import simplejson
import utils.yop_logger as yop_logger
from Crypto.PublicKey import RSA


class YopClientConfig:
    def __init__(self, config_file='config/yop_sdk_config_rsa_prod.json'):
        self.logger = yop_logger.get_logger()
        self.config_file = config_file
        self.sdk_config = self._init_config(config_file)

    def _init_config(self, config_file):
        # 获取配置文件信息
        with open(config_file, 'r') as f:
            sdk_config = simplejson.load(f)
            app_key = sdk_config.get('app_key', '')

            # platform public key
            yop_public_key_dict = {}
            yop_public_key_list = sdk_config['yop_public_key']
            for yop_public_key_str in yop_public_key_list:
                yop_public_key, cert_type, serial_no = self._parse_yop_public_key(yop_public_key_str)
                dict1 = yop_public_key_dict.setdefault(cert_type, {})
                dict1[serial_no] = yop_public_key
            sdk_config['yop_public_key'] = yop_public_key_dict

            # isv private key
            credentials_dict = {}
            isv_private_key_list = sdk_config['isv_private_key']
            for isv_private_key in isv_private_key_list:
                credentials = self._parse_isv_private_key(app_key, isv_private_key)
                credentials_dict[credentials.appKey] = credentials
                # 仅支持一个私钥，避免请求时不知道用哪个私钥签名
                if credentials is not None:
                    sdk_config['credentials'] = credentials_dict
                    break

        return sdk_config

    def _parse_isv_private_key(self, appKey, config):
        store_type = config.get('store_type', 'string')
        cert_type = config.get('cert_type', 'RSA2048')
        appKey = config.get('app_key', appKey)
        if 'string' == store_type:
            private_key_string = config['value']
            if cert_type.startswith('RSA'):
                private_key = RSA.importKey('-----BEGIN PRIVATE KEY-----\n' +
                                            private_key_string +
                                            '\n-----END PRIVATE KEY-----')
            else:
                private_key = PrivateKey.fromPem(private_key_string)
            return YopCredentials(appKey=appKey, priKey=private_key, cert_type=cert_type)
        else:
            self.logger.warn('暂时不支持的密钥类型 {}'.format(store_type))
            return None

    def _parse_yop_public_key(self, config):
        store_type = config.get('store_type', 'string')
        cert_type = config.get('cert_type', 'RSA2048')
        serial_no = config.get('serial_no', 'unknown')
        if 'string' == store_type:
            public_key_string = config['value']
            if cert_type.startswith('RSA'):
                yop_public_key = RSA.importKey(
                    '-----BEGIN PUBLIC KEY-----\n' +
                    public_key_string +
                    '\n-----END PUBLIC KEY-----')
            else:
                yop_public_key = PublicKey.fromPem(public_key_string).toStr()
        elif 'file_cer' == store_type:
            cert_file = config['value']
            yop_public_key = self.cer_analysis(cert_file)
            if cert_type.startswith('RSA'):
                yop_public_key = RSA.importKey(yop_public_key)
            else:
                yop_public_key = PublicKey.fromPem(yop_public_key).toStr()
        else:
            self.logger.warn('暂时不支持的密钥类型 {}'.format(store_type))
            yop_public_key = None

        return yop_public_key, cert_type, serial_no

    def cer_analysis(self, ceradd):
        '''
        解析证书文件
        '''
        file_context = open(ceradd).read()
        cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, file_context)

        certIssue = cert.get_issuer()
        version = cert.get_version() + 1
        serial_no = cert.get_serial_number()
        # signature = cert.get_signature_algorithm().decode("UTF-8")
        comname = certIssue.commonName
        starttime = cert.get_notBefore()
        endtime = cert.get_notAfter()
        flag = cert.has_expired()
        # long = cert.get_pubkey().bits()
        public = OpenSSL.crypto.dump_publickey(OpenSSL.crypto.FILETYPE_PEM, cert.get_pubkey()).decode("utf-8")
        # ext = cert.get_extension_count()
        # components = certIssue.get_components()

        self.logger.info(
            "certIssue:{}\ncomname:{}\nversion:{}\nserial_no:{}\nstarttime:{}\nendtime:{}\nexpired:{}\n{}".format(
                certIssue,
                comname,
                version,
                serial_no,
                starttime,
                endtime,
                flag,
                public))
        return public

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
        if appKey is None:
            return list(self.sdk_config['credentials'].values())[0]
        else:
            return self.sdk_config['credentials'].get(appKey)

    def get_yop_public_key(self):
        return self.sdk_config['yop_public_key']

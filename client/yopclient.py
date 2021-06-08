# -*- coding: utf-8 -*-

import os
from security.encryptor.rsaencryptor import RsaEncryptor
from security.encryptor.smencryptor import SmEncryptor
import simplejson
from simplejson.decoder import JSONDecodeError
import platform
import locale
from auth.v3signer.auth import SigV3AuthProvider
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
from client.yop_client_config import YopClientConfig
import utils.yop_logger as yop_logger

SDK_VERSION = '4.1.1'
platform_info = platform.platform().split("-")
python_compiler = platform.python_compiler().split(' ')
locale_info = locale.getdefaultlocale()
locale_lang = locale_info[0]
if locale_lang is None:
    locale_lang = 'zh-CN'
USER_AGENT = "/".join(['python',
                       SDK_VERSION,
                       platform_info[0],
                       platform_info[1],
                       python_compiler[0],
                       python_compiler[1],
                       platform.python_version(),
                       locale_lang])


class YopClient:
    clientConfig = None

    def __init__(self, clientConfig=None, cert_type=None, env=None):
        self.logger = yop_logger.get_logger()
        self.env = env
        self.cert_type = cert_type
        if clientConfig is None:
            clientConfig = YopClientConfig()

        # 同时支持RSA、SM两种加密机
        self.yop_encryptor_dict = {}
        for cert_type, yop_public_key_dict in clientConfig.sdk_config['yop_public_key'].items():
            if len(yop_public_key_dict) > 0:
                self.yop_encryptor_dict[cert_type] = self.get_encryptor(cert_type, yop_public_key_dict)

        self.clientConfig = clientConfig
        self.authProvider = SigV3AuthProvider(self.yop_encryptor_dict)

    def get_encryptor(self, cert_type, yop_public_key_dict):
        if 'SM2' == cert_type:
            return SmEncryptor(public_key_dict=yop_public_key_dict)
        else:
            return RsaEncryptor(public_key=list(yop_public_key_dict.values())[0])

    def get(self, api, query_params={}, credentials=None, basePath=None):
        if credentials is None:
            credentials = self.clientConfig.get_credentials()

        if basePath is None:
            basePath = self.clientConfig.get_server_root()

        authorization = self.authProvider.new_authenticator()
        headers = authorization.generate_signature(
            url=api, http_method='GET', query_params=query_params,
            credentials=credentials)
        headers['user-agent'] = USER_AGENT

        # for k, v in query_params.items():
        #         query_params[k] = quote(str(v), 'utf-8')

        url = ''.join([basePath, api])
        res = self._get_request(url, query_params=query_params, headers=headers)
        self.logger.info(
            'request:\nGET {}\nheaders:{}\nparams:{}\nresponse:\nheaders:{}\nbody:{}\ntime:{}ms\n'.format(
                url, headers, query_params, res.headers, res.text, res.elapsed.microseconds / 1000.))

        if res.status_code == 400:
            raise Exception("isv.service.not-exists")

        authorization._verify_res(res, credentials.get_cert_type())
        try:
            return simplejson.loads(res.text)
        except JSONDecodeError as e:
            self.logger.warn(res.text)
            raise e

    def download(self, api, query_params={}, credentials=None, basePath=None, file_path=None):
        if credentials is None:
            credentials = self.clientConfig.get_credentials()

        if basePath is None:
            basePath = self.clientConfig.get_server_root()

        authorization = self.authProvider.new_authenticator()
        headers = authorization.generate_signature(
            url=api, http_method='GET', query_params=query_params,
            credentials=credentials)
        headers['user-agent'] = USER_AGENT

        # for k, v in query_params.items():
        #         query_params[k] = quote(str(v), 'utf-8')

        url = ''.join([basePath, api])
        res = self._get_request(url, query_params=query_params, headers=headers)
        self.logger.info(
            'request:\nGET {}\nheaders:{}\nparams:{}\nresponse:\nheaders:{}\ntime:{}ms\n'.format(
                url, headers, query_params, res.headers, res.elapsed.microseconds / 1000.))

        if res.status_code == 400:
            raise Exception("isv.service.not-exists")
        if res.status_code >= 500:
            authorization._verify_res(res, credentials.get_cert_type())
            try:
                return simplejson.loads(res.text)
            except JSONDecodeError as e:
                self.logger.warn(res.text)
                raise e

        filename = res.headers['Content-Disposition'].split('; ')[1].replace('filename=', '')
        filename = filename[filename.rindex('/') + 1:len(filename)]

        try:
            if not os.path.exists(file_path):
                os.mkdir(file_path)
            full_filename = file_path + '/' + filename
            with open(full_filename, "wb+") as file:
                file.write(res.content)
                authorization._verify_res_download(res, credentials.get_cert_type(), file)
            return 0
        except OSError as e:
            self.logger.warn('找不到文件路径:{}'.format(file_path))
            raise e
        else:
            return 1

    def _get_request(self,
                     url, query_params={},
                     headers={}):
        res = requests.get(url=url, params=query_params, headers=headers)
        return res

    def post_json(
            self,
            api,
            post_params={},
            credentials=None,
            basePath=None):
        return self.post(api, post_params, credentials, basePath=basePath, json_param=True)

    def post(self, api, post_params={}, credentials=None, basePath=None, json_param=False):
        if credentials is None:
            credentials = self.clientConfig.get_credentials()

        if basePath is None:
            basePath = self.clientConfig.get_server_root()

        authorization = self.authProvider.new_authenticator()
        headers = authorization.generate_signature(
            url=api, http_method='POST', post_params=post_params,
            credentials=credentials,
            json_param=json_param)
        headers['user-agent'] = USER_AGENT

        # for k, v in post_params.items():
        #         post_params[k] = quote(str(v), 'utf-8')

        url = ''.join([basePath, api])

        if json_param:
            headers['content-type'] = 'application/json'
            data = simplejson.dumps(
                post_params, sort_keys=True, indent=4, separators=(
                    ',', ': '), ensure_ascii=True).encode("latin-1")
            res = self._post_request(url, payload=data, headers=headers)
        else:
            res = self._post_request(url, params=post_params, headers=headers)

        if res.status_code == 400:
            raise Exception("isv.service.not-exists")

        authorization._verify_res(res, credentials.get_cert_type())
        try:
            return simplejson.loads(res.text)
        except JSONDecodeError as e:
            self.logger.warn(res.text)
            raise e

    def upload(self, api, post_params={}, credentials=None, basePath=None):
        if credentials is None:
            credentials = self.clientConfig.get_credentials()

        if basePath is None:
            basePath = self.clientConfig.get_yos_server_root()

        authorization = self.authProvider.new_authenticator()
        headers = authorization.generate_signature(
            url=api, http_method='POST', post_params=post_params,
            credentials=credentials)
        headers['user-agent'] = USER_AGENT

        # 封装文件上传编码器
        multipart = MultipartEncoder(
            fields=post_params
        )
        headers['content-type'] = multipart.content_type

        url = ''.join([basePath, api])
        res = self._post_request(url, payload=multipart, headers=headers)

        if res.status_code == 400:
            raise Exception("isv.service.not-exists")

        authorization._verify_res_upload(res, credentials.get_cert_type(), post_params)
        try:
            return simplejson.loads(res.text)
        except JSONDecodeError as e:
            self.logger.warn(res.text)
            raise e

    def _post_request(self, url, payload=None, params=None, headers={}):
        res = requests.post(url=url, headers=headers, data=payload, params=params)
        self.logger.debug(
            'request:\nPOST {}\nheaders:{}\nparams:{}\nresponse:\nheaders:{}\nbody:{}\ntime:{}ms\n'.format(
                url, headers, params, res.headers, res.text, res.elapsed.microseconds / 1000.))
        return res

# -*- coding: utf-8 -*-
import json
import locale
import os
import platform

import requests
import simplejson
from requests_toolbelt.multipart.encoder import MultipartEncoder
from simplejson.decoder import JSONDecodeError

import yop_python_sdk.utils.yop_logger as yop_logger
from yop_python_sdk.auth.v3signer.auth import SigV3AuthProvider
from yop_python_sdk.client.yop_client_config import YopClientConfig
from yop_python_sdk.security.encryptor.rsaencryptor import RsaEncryptor
from yop_python_sdk.security.encryptor.smencryptor import SmEncryptor

SDK_VERSION = '4.3.0'
platform_info = platform.platform().split("-")
python_compiler = platform.python_compiler().split(' ')
locale_info = locale.getdefaultlocale()
locale_lang = locale_info[0]
if locale_lang is None:
    locale_lang = 'zh-CN'
USER_AGENT = "/".join([
    'python', SDK_VERSION, platform_info[0], platform_info[1],
    python_compiler[0], python_compiler[1],
    platform.python_version(), locale_lang
])

try:
    # python 3.x
    from urllib.parse import quote, quote_plus
except ImportError:
    # python 2.x
    from urllib import quote

class YopClient:
    clientConfig = None

    def __init__(self, clientConfig=None, cert_type=None, env=None):
        """
        Yop的

        Args:
            self: write your description
            clientConfig: write your description
            cert_type: write your description
            env: write your description
        """
        self.logger = yop_logger.get_logger()
        self.env = env
        self.cert_type = cert_type
        if clientConfig is None:
            clientConfig = YopClientConfig()

        # 同时支持RSA、SM两种加密机
        self.yop_encryptor_dict = {}
        for cert_type, yop_public_key_dict in clientConfig.sdk_config[
                'yop_public_key'].items():
            if len(yop_public_key_dict) > 0:
                self.yop_encryptor_dict[cert_type] = self.get_encryptor(
                    cert_type, yop_public_key_dict)

        self.clientConfig = clientConfig
        self.authProvider = SigV3AuthProvider(self.yop_encryptor_dict)

    def get_encryptor(self, cert_type, yop_public_key_dict):
        """
        Returns the appropriate encryptor depending on the cert_type.

        Args:
            self: write your description
            cert_type: write your description
            yop_public_key_dict: write your description
        """
        if 'SM2' == cert_type:
            return SmEncryptor(public_key_dict=yop_public_key_dict)
        else:
            return RsaEncryptor(
                public_key=list(yop_public_key_dict.values())[0])

    def get(self, api, query_params={}, credentials=None, basePath=None, http_param=None):
        """
        Make a GET request to the API.

        Args:
            self: write your description
            api: write your description
            query_params: write your description
            credentials: write your description
            basePath: write your description
        """
        if credentials is None:
            credentials = self.clientConfig.get_credentials()

        if basePath is None:
            basePath = self.clientConfig.get_server_root()

        http_client = self.parse_http_param(http_param)
        authorization = self.authProvider.new_authenticator()
        headers = authorization.generate_signature(url=api,
                                                   http_method='GET',
                                                   query_params=query_params,
                                                   credentials=credentials)
        headers['user-agent'] = USER_AGENT
        headers['content-type'] = 'application/x-www-form-urlencoded'
        for k, v in query_params.items():
            query_params[k] = quote_plus(str(v), 'utf-8')
        self.logger.debug(query_params)

        url = ''.join([basePath, api])
        res = self._get_request(url,
                                query_params=query_params,
                                headers=headers,
                                http_client=http_client)
        self.logger.info(
            'request:\nGET {}\nheaders:{}\nparams:{}\nresponse:\nheaders:{}\nbody:{}\ntime:{}ms\n'
            .format(url, headers, query_params, res.headers, res.text,
                    res.elapsed.microseconds / 1000.))

        if res.status_code == 400:
            raise Exception("isv.service.not-exists")

        authorization._verify_res(res, credentials.get_cert_type())
        try:
            return simplejson.loads(res.text)
        except JSONDecodeError as e:
            self.logger.warn(res.text)
            raise e

    def parse_http_param(self, http_param={}):
        http_client = self.clientConfig.get_http_client()
        tem_dict = {}
        if http_param is not None:
            for key, value in http_client.items():
                tem_dict[key] = value
                if key in http_param:
                    tem_value = http_param[key]
                    if (isinstance(tem_value, int) or isinstance(tem_value, float)) and tem_value > 0:
                        tem_dict[key] = value
                    else:
                        raise Exception("http client parameter is nonstandard, key: {}".format(key))
        else:
            tem_dict = http_client
        return tem_dict

    def download(self,
                 api,
                 query_params={},
                 credentials=None,
                 basePath=None,
                 file_path=None,
                 http_param=None):
        """
        Downloads the specified API from the server.

        Args:
            self: write your description
            api: write your description
            query_params: write your description
            credentials: write your description
            basePath: write your description
            file_path: write your description
        """
        if credentials is None:
            credentials = self.clientConfig.get_credentials()

        if basePath is None:
            basePath = self.clientConfig.get_server_root()

        http_client = self.parse_http_param(http_param)
        authorization = self.authProvider.new_authenticator()
        headers = authorization.generate_signature(url=api,
                                                   http_method='GET',
                                                   query_params=query_params,
                                                   credentials=credentials)
        headers['user-agent'] = USER_AGENT

        # for k, v in query_params.items():
        #         query_params[k] = quote(str(v), 'utf-8')

        url = ''.join([basePath, api])
        res = self._get_request(url,
                                query_params=query_params,
                                headers=headers,
                                http_client=http_client)
        self.logger.debug(
            'request:\nGET {}\nheaders:{}\nparams:{}\nresponse:\nheaders:{}\ntime:{}ms\n'
            .format(url, headers, query_params, res.headers,
                    res.elapsed.microseconds / 1000.))

        if res.status_code == 400:
            raise Exception("isv.service.not-exists")
        if res.status_code >= 500:
            authorization._verify_res(res, credentials.get_cert_type())
            try:
                return simplejson.loads(res.text)
            except JSONDecodeError as e:
                self.logger.warn(res.text)
                raise e

        filename = res.headers['Content-Disposition'].split('; ')[1].replace(
            'filename=', '')
        filename = filename[filename.rindex('/') + 1:len(filename)]

        try:
            if not os.path.exists(file_path):
                os.mkdir(file_path)
            full_filename = file_path + '/' + filename
            with open(full_filename, "wb+") as file:
                file.write(res.content)
                authorization._verify_res_download(res,
                                                   credentials.get_cert_type(),
                                                   file)
            return 0
        except OSError as e:
            self.logger.warn('找不到文件路径:{}'.format(file_path))
            raise e
        else:
            return 1
        finally:
            file.close()

    def _get_request(self, url, query_params={}, headers={}, http_client={}):
        """
        Wrapper for requests. get that handles the headers and returns the response.

        Args:
            self: write your description
            url: write your description
            query_params: write your description
            headers: write your description
        """
        connect_timeout = round(http_client['connect_timeout'] / 1000, 3)
        read_timeout = round(http_client['read_timeout'] / 1000, 3)
        return requests.get(url=url,
                            params=query_params,
                            headers=headers,
                            timeout=(connect_timeout, read_timeout))

    def post_json(self, api, post_params={}, credentials=None, basePath=None, http_param=None):
        """
        POST the specified post params to the specified API

        Args:
            self: write your description
            api: write your description
            post_params: write your description
            credentials: write your description
            basePath: write your description
        """
        return self.post(api,
                         post_params,
                         credentials,
                         basePath=basePath,
                         json_param=True,
                         http_param=http_param)

    def post(self,
             api,
             post_params={},
             credentials=None,
             basePath=None,
             json_param=False,
             http_param=None):
        """
        Make a POST request to the API.

        Args:
            self: write your description
            api: write your description
            post_params: write your description
            credentials: write your description
            basePath: write your description
            json_param: write your description
        """
        if credentials is None:
            credentials = self.clientConfig.get_credentials()

        if basePath is None:
            basePath = self.clientConfig.get_server_root()

        http_client = self.parse_http_param(http_param)

        authorization = self.authProvider.new_authenticator()
        headers = authorization.generate_signature(url=api,
                                                   http_method='POST',
                                                   post_params=post_params,
                                                   credentials=credentials,
                                                   json_param=json_param)
        headers['user-agent'] = USER_AGENT

        url = ''.join([basePath, api])

        if json_param:
            headers['content-type'] = 'application/json'
            data = json.dumps(post_params,
                              separators=(',', ':')).encode('utf-8')
            res = self._post_request(url, payload=data, headers=headers,
                                     http_client=http_client)
        else:
            headers['content-type'] = 'application/x-www-form-urlencoded'
            for k, v in post_params.items():
                post_params[k] = quote_plus(str(v), 'utf-8')
            self.logger.debug(post_params)
            res = self._post_request(url, params=post_params, headers=headers,
                                     http_client=http_client)

        if res.status_code == 400:
            raise Exception("isv.service.not-exists")

        authorization._verify_res(res, credentials.get_cert_type())
        try:
            return simplejson.loads(res.text)
        except JSONDecodeError as e:
            self.logger.warn(res.text)
            raise e

    def upload(self, api, post_params={}, credentials=None, basePath=None,
               http_param=None):
        """
        Upload a new file to Yos.

        Args:
            self: write your description
            api: write your description
            post_params: write your description
            credentials: write your description
            basePath: write your description
        """
        if credentials is None:
            credentials = self.clientConfig.get_credentials()

        if basePath is None:
            basePath = self.clientConfig.get_yos_server_root()

        http_client = self.parse_http_param(http_param)
        authorization = self.authProvider.new_authenticator()
        headers = authorization.generate_signature(url=api,
                                                   http_method='POST',
                                                   post_params=post_params,
                                                   credentials=credentials)
        headers['user-agent'] = USER_AGENT

        # 封装文件上传编码器
        multipart = MultipartEncoder(fields=post_params)
        headers['content-type'] = multipart.content_type

        url = ''.join([basePath, api])
        res = self._post_request(url, payload=multipart, headers=headers, http_client=http_client)

        if res.status_code == 400:
            raise Exception("isv.service.not-exists")

        authorization._verify_res_upload(res, credentials.get_cert_type(),
                                         post_params)
        try:
            return simplejson.loads(res.text)
        except JSONDecodeError as e:
            self.logger.warn(res.text)
            raise e

    def _post_request(self, url, payload=None, params=None, headers={}, http_client={}):
        """
        Perform a POST request.

        Args:
            self: write your description
            url: write your description
            payload: write your description
            params: write your description
            headers: write your description
        """
        connect_timeout = round(http_client['connect_timeout'] / 1000, 3)
        read_timeout = round(http_client['read_timeout'] / 1000, 3)
        res = requests.post(url=url,
                            headers=headers,
                            data=payload,
                            params=params,
                            timeout=(connect_timeout, read_timeout))
        self.logger.debug(
            'request:\nPOST {}\nheaders:{}\nparams:{}\nresponse:\nheaders:{}\nbody:{}\ntime:{}ms\n'
            .format(url, headers, params, res.headers, res.text,
                    res.elapsed.microseconds / 1000.))
        return res

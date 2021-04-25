# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import simplejson
from simplejson.decoder import JSONDecodeError
import platform
import locale
from v3signer.auth import SigV3AuthProvider
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
from utils.yop_config_utils import YopClientConfig
import utils.yop_security_utils as yop_security_utils
import utils.yop_logging_utils as yop_logging_utils

SDK_VERSION = '3.4.0'
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

    def __init__(self, clientConfig=None):
        self.logger = yop_logging_utils.get_logger()
        if clientConfig is None:
            clientConfig = YopClientConfig()
        self.clientConfig = clientConfig
        self.authProvider = SigV3AuthProvider()

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
            'get url:{}\nheaders:{}\nparams:{}\nresponse:{}\ntime:{}ms\n'.format(
                url, headers, query_params, res.text, res.elapsed.microseconds / 1000.))

        if res.status_code == 400:
            raise Exception("isv.service.not-exists")

        self._verify_res(res)
        try:
            return simplejson.loads(res.text)
        except JSONDecodeError as identifier:
            self.logger.warn(res.text)
            pass

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
            'get url:{}\n headers:{}\n params:{}\n time:{}ms\n'.format(
                url, headers, query_params, res.elapsed.microseconds / 1000.))

        if res.status_code == 400:
            raise Exception("isv.service.not-exists")
        if res.status_code >= 500:
            self._verify_res(res)
            try:
                return simplejson.loads(res.text)
            except JSONDecodeError as identifier:
                self.logger.warn(res.text)
                pass

        filename = res.headers['Content-Disposition'].split('; ')[1].replace('filename=', '')
        filename = filename[filename.rindex('/') + 1:len(filename)]

        try:
            if not os.path.exists(file_path):
                os.mkdir(file_path)
            full_filename = file_path + '/' + filename
            with open(full_filename, "wb+") as file:
                file.write(res.content)
                self._verify_res_download(res, file)
            return 0
        except FileNotFoundError as identifier:
            self.logger.warn('找不到文件路径:{}'.format(file_path))
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

        self._verify_res(res)
        try:
            return simplejson.loads(res.text)
        except JSONDecodeError as identifier:
            self.logger.warn(res.text)
            pass

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

        self._verify_res_upload(res, post_params)
        try:
            return simplejson.loads(res.text)
        except JSONDecodeError as identifier:
            self.logger.warn(res.text)
            pass

    def _verify_res(self, res, post_params=None):
        self._verify_res_sha256(res)

    def _verify_res_upload(self, res, post_params=None):
        self._verify_res_sha256(res)

        # crc64ecma
        if post_params is not None and res.headers.__contains__('x-yop-hash-crc64ecma'):
            actual_crc64ecma = self._files_crc64(post_params)
            expect_crc64ecma = res.headers['x-yop-hash-crc64ecma']
            if actual_crc64ecma != expect_crc64ecma:
                self.logger.info(
                    'crc verify failed, expect_crc64ecma:{}, actual_crc64ecma:{}'.format(
                        expect_crc64ecma, actual_crc64ecma, ))
                raise Exception("isv.scene.filestore.put.crc-failed")

    def _verify_res_download(self, res, file):
        # crc64ecma
        if res.headers.__contains__('x-yop-hash-crc64ecma'):
            actual_crc64ecma = str(yop_security_utils.cal_file_crc64(file))
            expect_crc64ecma = res.headers['x-yop-hash-crc64ecma']
            if actual_crc64ecma != expect_crc64ecma:
                self.logger.info(
                    'crc verify failed, expect_crc64ecma:{}, actual_crc64ecma:{}'.format(
                        expect_crc64ecma, actual_crc64ecma, ))
                raise Exception("isv.scene.filestore.get.crc-failed")

    def _verify_res_sha256(self, res):
        # 验签
        if res.headers.__contains__('x-yop-sign'):
            text = res.text.replace('\t', '').replace('\n', '').replace(' ', '')
            signature = res.headers['x-yop-sign']
            sig_flag = yop_security_utils.verify_rsa(text, signature, self.clientConfig.get_yop_public_key())
            if not sig_flag:
                self.logger.info(
                    'signature verify failed, text:{}, signature:{}'.format(
                        text, signature, ))
                raise Exception("sdk.invoke.digest.verify-failure")

    def _files_crc64(self, post_params={}):
        sorted_items = sorted(post_params.items())
        crc64ecma = []
        for k, v in sorted_items:
            if isinstance(v, tuple):
                crc64ecma.append(str(yop_security_utils.cal_file_crc64(v[1])))

        return '/'.join(crc64ecma)

    def _post_request(self, url, payload=None, params=None, headers={}):
        res = requests.post(url=url, headers=headers, data=payload, params=params)
        self.logger.info(
            'get url:{}\n headers:{}\n params:{}\n response:{}\n time:{}ms\n'.format(
                url, headers, params, res.text, res.elapsed.microseconds / 1000.))
        return res

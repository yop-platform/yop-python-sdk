# -*- coding: utf-8 -*-

# @title : 拼接需要的headers
# @Author : zhanglele
# @Date : 18/5/21
# @Desc :

try:
    # python 3.x
    from urllib.parse import quote
except ImportError:
    # python 2.x
    from urllib import quote
import datetime
import hashlib
import json
import urllib
import uuid

import yop_python_sdk.utils.yop_logger as yop_logger
import yop_python_sdk.utils.yop_security_utils as yop_security_utils

EXPIRATION_IN_SECONDS = '1800'
_SIGV4_TIMESTAMP_FORMAT = "%Y%m%dT%H%M%S"


class SigV3AuthProvider:

    def __init__(self, yop_encryptor_dict):
        """
        Initialize the YarpEncryptor.

        Args:
            self: write your description
            yop_encryptor_dict: write your description
        """
        self.logger = yop_logger.get_logger()
        self.session_id = str(uuid.uuid4())
        self.yop_encryptor_dict = yop_encryptor_dict

    def new_authenticator(self):
        """
        Return a new authenticator for this session.

        Args:
            self: write your description
        """
        return SigV3Authenticator(self.yop_encryptor_dict, self.session_id)


class SigV3Authenticator:

    def __init__(self, yop_encryptor_dict, session_id=''):
        """
        Initialize the YarpEncryptor.

        Args:
            self: write your description
            yop_encryptor_dict: write your description
            session_id: write your description
        """
        self.logger = yop_logger.get_logger()
        self.yop_encryptor_dict = yop_encryptor_dict
        self.session_id = session_id

    def _format_iso8601_timestamp(
        self, date_time=datetime.datetime.utcnow().replace(microsecond=0)):
        """
        Format ISO8601 timestamp.

        Args:
            self: write your description
            date_time: write your description
            datetime: write your description
            datetime: write your description
            utcnow: write your description
            replace: write your description
            microsecond: write your description
        """
        return "{}Z".format(date_time.strftime(_SIGV4_TIMESTAMP_FORMAT))

    def get_query_str(self, items, t1='=', t2='&'):
        """
        Returns a query string for the given items.

        Args:
            self: write your description
            items: write your description
            t1: write your description
            t2: write your description
        """
        lt = []
        sorted_items = sorted(items)
        self.logger.debug("sorted_items:{}".format(sorted_items))
        for k, v in sorted_items:
            # logger.debug("k:{}, v:{}".format(k, v))
            if isinstance(v, tuple):
                continue
            elif isinstance(v, list):
                sorted_sub_items = sorted(v)
                for sub_v in sorted_sub_items:
                    lt.append(k + t1 + quote(str(sub_v), 'utf-8'))
            else:
                lt.append(k + t1 + quote(str(v), 'utf-8'))
        return t2.join(lt)

    def generate_signature(self,
                           url,
                           credentials,
                           http_method='POST',
                           query_params=None,
                           post_params=None,
                           json_param=False):
        """
        Generate the signature for the request.

        Args:
            self: write your description
            url: write your description
            credentials: write your description
            http_method: write your description
            query_params: write your description
            post_params: write your description
            json_param: write your description
        """
        protocol_version = 'yop-auth-v3'
        app_key = credentials.get_appKey()
        yop_date = self._format_iso8601_timestamp()
        expired_seconds = EXPIRATION_IN_SECONDS

        query_str = ''
        if 'GET' == http_method and query_params:
            query_str = self.get_query_str(query_params.items())
        # elif 'POST' == http_method and not json_param and post_params:
        #     query_str = self.get_query_str(post_params.items())

        self.logger.debug('http_method:{}, query_str:{}'.format(
            http_method, query_str))

        headers = {}
        yop_request_id = str(uuid.uuid4())
        canonical_header_str = 'x-yop-appkey:' + quote(app_key, 'utf-8')
        yop_content_sha256 = self.content_sha256(http_method, json_param, post_params)
        headers['x-yop-content-sha256'] = yop_content_sha256
        canonical_header_str = canonical_header_str + \
                               '\nx-yop-content-sha256:' + quote(yop_content_sha256, 'utf-8') + \
                               '\nx-yop-request-id:' + quote(yop_request_id, 'utf-8')
        signed_headers = 'x-yop-appkey;x-yop-content-sha256;x-yop-request-id'

        auth_str = protocol_version + '/' + app_key + \
            '/' + yop_date + '/' + expired_seconds
        canonical_request = auth_str + '\n' + http_method + '\n' + \
            url + '\n' + query_str + '\n' + canonical_header_str

        signature, algorithm, hash_algorithm = credentials.encryptor.signature(
            canonical_request)

        self.logger.debug(
            'canonical_header_str:\n{}'.format(canonical_header_str))
        self.logger.debug('signed_headers:{}'.format(signed_headers))
        self.logger.debug('auth_str:{}'.format(auth_str))
        self.logger.debug('canonical_request:\n{}'.format(canonical_request))
        self.logger.debug('signature:\n{}'.format(signature))

        authorization_header = algorithm + ' ' + auth_str + '/' + \
            signed_headers + '/' + signature

        self.logger.debug(
            'authorization_header:{}'.format(authorization_header))

        headers['authorization'] = authorization_header + '$' + hash_algorithm
        headers['x-yop-session-id'] = self.session_id
        headers['x-yop-request-id'] = yop_request_id
        headers['x-yop-appkey'] = app_key
        return headers

    def content_sha256(self, http_method, json_param, post_params):
        """
        Generate sha256 hash of json_params.

        Args:
            self: write your description
            http_method: write your description
            json_params: write your description
            post_params: write your description
        """
        sha256 = hashlib.sha256()
        query_str = ''
        if 'POST' == http_method and not json_param and post_params:
            query_str = self.get_query_str(post_params.items())
        elif 'POST' == http_method and json_param and post_params:
            query_str = json.dumps(post_params,
                                   separators=(',', ':'))
        encode = query_str.encode('utf-8')
        sha256.update(encode)
        return sha256.hexdigest()

    def combine_url(self, url, query_dict):
        """
        Combine url and query_dict.

        Args:
            self: write your description
            url: write your description
            query_dict: write your description
        """
        if not query_dict:
            return url
        if isinstance(query_dict, dict):
            query_dict = urllib.urlencode(query_dict)
        return url + '?' + query_dict

    def handle_request(self, query_dict):
        """
        Handles the request.

        Args:
            self: write your description
            query_dict: write your description
        """
        if isinstance(query_dict, dict):
            query_dict = urllib.urlencode(query_dict)
        return query_dict

    def _verify_res(self, res, cert_type, post_params=None):
        """
        Verify a signed response.

        Args:
            self: write your description
            res: write your description
            cert_type: write your description
            post_params: write your description
        """
        self._do_verify_res(res, cert_type)

    def _verify_res_upload(self, res, cert_type, post_params=None):
        """
        Verifies the uploaded file is valid.

        Args:
            self: write your description
            res: write your description
            cert_type: write your description
            post_params: write your description
        """
        self._do_verify_res(res, cert_type)

        # crc64ecma
        # if post_params is not None and res.headers.__contains__(
        #         'x-yop-hash-crc64ecma'):
        #     actual_crc64ecma = self._files_crc64(post_params)
        #     expect_crc64ecma = res.headers['x-yop-hash-crc64ecma']
        #     if actual_crc64ecma != expect_crc64ecma:
        #         self.logger.info(
        #             'crc verify failed, expect_crc64ecma:{}, actual_crc64ecma:{}'
        #             .format(
        #                 expect_crc64ecma,
        #                 actual_crc64ecma,
        #             ))
        #         raise Exception("isv.scene.filestore.put.crc-failed")

    def _verify_res_download(self, res, cert_type, file):
        """
        Verify the download response is correct

        Args:
            self: write your description
            res: write your description
            cert_type: write your description
            file: write your description
        """
        # crc64ecma
        if res.headers.__contains__('x-yop-hash-crc64ecma'):
            actual_crc64ecma = str(yop_security_utils.cal_file_crc64(file))
            expect_crc64ecma = res.headers['x-yop-hash-crc64ecma']
            if actual_crc64ecma != expect_crc64ecma:
                self.logger.warn(
                    'crc verify failed, expect_crc64ecma:{}, actual_crc64ecma:{}'
                    .format(
                        expect_crc64ecma,
                        actual_crc64ecma,
                    ))
                raise Exception("isv.scene.filestore.get.crc-failed")

    def _do_verify_res(self, res, cert_type):
        """
        Verifies the signature on the response.

        Args:
            self: write your description
            res: write your description
            cert_type: write your description
        """
        # 验签
        if res.headers.__contains__('x-yop-sign'):
            text = res.text.replace('\t', '').replace('\n',
                                                      '').replace(' ', '')
            signature = res.headers['x-yop-sign']
            serial_no = res.headers.get('x-yop-serial-no', default=None)
            sig_flag = self.yop_encryptor_dict[cert_type].verify_signature(
                text, signature, serial_no=serial_no)
            if not sig_flag:
                self.logger.warn(
                    'signature verify failed, text:{}, signature:{}'.format(
                        text,
                        signature,
                    ))
                raise Exception("sdk.invoke.digest.verify-failure")

    def _files_crc64(self, post_params={}):
        """
        Calculate the CRC64 of the files

        Args:
            self: write your description
            post_params: write your description
        """
        sorted_items = sorted(post_params.items())
        crc64ecma = []
        for k, v in sorted_items:
            self.logger.info('crc verify v:{}'.format(v, ))
            if isinstance(v, tuple):
                crc64ecma.append(str(yop_security_utils.cal_file_crc64(v[1])))

        return '/'.join(crc64ecma)

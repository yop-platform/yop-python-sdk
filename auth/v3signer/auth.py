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
import uuid
import urllib
import simplejson
import hashlib
import datetime
import utils.yop_logger as yop_logger
import utils.yop_security_utils as yop_security_utils

EXPIRATION_IN_SECONDS = '1800'
_SIGV4_TIMESTAMP_FORMAT = "%Y%m%dT%H%M%S"


class SigV3AuthProvider:
    def __init__(self, yop_encryptor_dict):
        self.logger = yop_logger.get_logger()
        self.session_id = str(uuid.uuid4())
        self.yop_encryptor_dict = yop_encryptor_dict

    def new_authenticator(self):
        return SigV3Authenticator(self.yop_encryptor_dict, self.session_id)


class SigV3Authenticator:
    def __init__(self, yop_encryptor_dict, session_id=''):
        self.logger = yop_logger.get_logger()
        self.yop_encryptor_dict = yop_encryptor_dict
        self.session_id = session_id

    def _format_iso8601_timestamp(self, date_time=datetime.datetime.utcnow().replace(microsecond=0)):
        return "{}Z".format(date_time.strftime(_SIGV4_TIMESTAMP_FORMAT))

    def get_query_str(self, items, t1='=', t2='&'):
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
        protocol_version = 'yop-auth-v2'
        app_key = credentials.get_appKey()
        yop_date = self._format_iso8601_timestamp()
        expired_seconds = EXPIRATION_IN_SECONDS

        query_str = ''
        if 'GET' == http_method and query_params:
            query_str = self.get_query_str(query_params.items())
        elif 'POST' == http_method and not json_param and post_params:
            query_str = self.get_query_str(post_params.items())

        self.logger.debug('http_method:{}, query_str:{}'.format(http_method, query_str))

        headers = {}
        yop_request_id = str(uuid.uuid4())
        canonical_header_str = 'x-yop-appkey:' + quote(app_key, 'utf-8')
        if json_param:
            yop_content_sha256 = self.content_sha256(json_param)
            headers['x-yop-content-sha256'] = yop_content_sha256
            canonical_header_str = canonical_header_str + '\nx-yop-content-sha256:' + quote(yop_content_sha256, 'utf-8')
            signed_headers = 'x-yop-appkey;x-yop-content-sha256;x-yop-request-id'
        else:
            signed_headers = 'x-yop-appkey;x-yop-request-id'
        canonical_header_str = canonical_header_str + '\nx-yop-request-id:' + quote(yop_request_id, 'utf-8')

        auth_str = protocol_version + '/' + app_key + '/' + yop_date + '/' + expired_seconds
        canonical_request = auth_str + '\n' + http_method + '\n' + url + '\n' + query_str + '\n' + canonical_header_str

        signature, algorithm, hash_algorithm = credentials.encryptor.signature(canonical_request)

        self.logger.debug('canonical_header_str:\n{}'.format(canonical_header_str))
        self.logger.debug('signed_headers:{}'.format(signed_headers))
        self.logger.debug('auth_str:{}'.format(auth_str))
        self.logger.debug('canonical_request:\n{}'.format(canonical_request))
        self.logger.debug('signature:\n{}'.format(signature))

        authorization_header = algorithm + ' ' + auth_str + '/' + \
            signed_headers + '/' + signature

        self.logger.debug('authorization_header:{}'.format(authorization_header))

        headers['authorization'] = authorization_header + '$' + hash_algorithm
        headers['x-yop-session-id'] = self.session_id
        headers['x-yop-request-id'] = yop_request_id
        headers['x-yop-appkey'] = app_key
        return headers

    def content_sha256(self, json_params):
        sha256 = hashlib.sha256()
        sha256.update(
            simplejson.dumps(
                json_params,
                sort_keys=True,
                indent=4,
                separators=(
                    ',',
                    ': '),
                ensure_ascii=True).encode("latin-1"))
        return sha256.hexdigest()

    def combine_url(self, url, query_dict):
        if not query_dict:
            return url
        if isinstance(query_dict, dict):
            query_dict = urllib.urlencode(query_dict)
        return url + '?' + query_dict

    def handle_request(self, query_dict):
        if isinstance(query_dict, dict):
            query_dict = urllib.urlencode(query_dict)
        return query_dict

    def _verify_res(self, res, cert_type, post_params=None):
        self._do_verify_res(res, cert_type)

    def _verify_res_upload(self, res, cert_type, post_params=None):
        self._do_verify_res(res, cert_type)

        # crc64ecma
        if post_params is not None and res.headers.__contains__('x-yop-hash-crc64ecma'):
            actual_crc64ecma = self._files_crc64(post_params)
            expect_crc64ecma = res.headers['x-yop-hash-crc64ecma']
            if actual_crc64ecma != expect_crc64ecma:
                self.logger.info(
                    'crc verify failed, expect_crc64ecma:{}, actual_crc64ecma:{}'.format(
                        expect_crc64ecma, actual_crc64ecma, ))
                raise Exception("isv.scene.filestore.put.crc-failed")

    def _verify_res_download(self, res, cert_type, file):
        # crc64ecma
        if res.headers.__contains__('x-yop-hash-crc64ecma'):
            actual_crc64ecma = str(yop_security_utils.cal_file_crc64(file))
            expect_crc64ecma = res.headers['x-yop-hash-crc64ecma']
            if actual_crc64ecma != expect_crc64ecma:
                self.logger.info(
                    'crc verify failed, expect_crc64ecma:{}, actual_crc64ecma:{}'.format(
                        expect_crc64ecma, actual_crc64ecma, ))
                raise Exception("isv.scene.filestore.get.crc-failed")

    def _do_verify_res(self, res, cert_type):
        # 验签
        if res.headers.__contains__('x-yop-sign'):
            text = res.text.replace('\t', '').replace('\n', '').replace(' ', '')
            signature = res.headers['x-yop-sign']
            serial_no = res.headers.get('x-yop-serial-no', default=None)
            sig_flag = self.yop_encryptor_dict[cert_type].verify_signature(text, signature, serial_no=serial_no)
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

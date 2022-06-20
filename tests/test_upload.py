# -*- coding: utf-8 -*-

import tests.assertion as assertion
from yop_python_sdk.auth.v3signer.credentials import YopCredentials
import urllib
import sys

sys.path.append("./")


class Test(object):

    def test_upload(self, client):
        """
        Uploads a file to the API and verifies the upload is successful.

        Args:
            self: write your description
            client: write your description
        """
        file_path = './LICENSE'
        # with open(file_path, mode='r', encoding='utf8') as f:
        api = '/yos/v1.0/mer/merchant/qual/upload'
        file = open(file_path, mode='rb')
        params = {
            'merQual': ('file_name', file, 'multipart/form-data'),
            'remark': '演示普通参数传递，该api没有remark参数'
        }
        res = client.upload(api, params)
        file.close()
        assertion.success(res)

    def test_upload_with_credentials(self, client):
        """
        Test uploading with credentials.

        Args:
            self: write your description
            client: write your description
        """
        if 'sm' == client.cert_type:
            return

        file_path = './LICENSE'
        api = '/yos/v1.0/mer/merchant/qual/upload'
        file = open(file_path, mode='rb')
        params = {
            'merQual': ('file_name', file, 'multipart/form-data'),
            'remark': '演示普通参数传递，该api没有remark参数'
        }
        credentials = YopCredentials(
            appKey='OPR:10000470992',
            cert_type='RSA2048',
            priKey=
            'MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCMTXz1XQeTx+Eq/Zom7RQeam15IZ23CNCgxl/lG93JFQlGNszQn9yaXlrD4BH99tN6816Ven0pi3+NN0oiunwqfAAiRrxBPXmZKRCjQRKqzAiBYcGZsW9kmzDoCfBLGmmHSWxs58Z3+iAU6RrHLJ5BPhSxpEzed8h5d0pNe8ltDlS9fTr9IvWpVkLKKAPdAmUbRZlbUm/sabdkB9fXGK+dSee+tTJ8lzW2UeSLHeZKKeCbkNckmlD8K+Fgk3N3uEoS0pixycg92VQZrIaH3fKTO/cV1HkubyNEwCF6EwSyOvmyXUr4WqOHzeg+ikPufH1nQvdsudjAv1DN7be65oz7AgMBAAECggEAakL19U+0QXUNUOYqLnk416B7sVaIgOwoNtyIHJnybC2GjKtMjGXHSxNTYy798X9TxLc2V7ghu6lvvaC2gX8EM5ke8NbqFe9dfWbgtwS+AqXtezBy1NjSKTxw2g1M9VTXwCMX/5O7eXrzeWLjaR6d7YP7YF+z6HqIV5bFq9GpSPKGjaiYlZ5rRf0nwen0+BI2wvIRxglvpHvB0zUK3r330Z2gNQvnM2R7YW6Y0zIb3O7ASu+Qh2nGyI4J+OayP1bBohSyZ8KVHc+rDZ3lZRF9Tsj9p9A+JcDS2cLosVRfnVefhRn1356noEB8uR3zNhLHAgEJ3ddZM6DB0u3aKMmIYQKBgQDByH0e8mR3yoFnf6XG2qzflIxwvRPZx7EUhfGby3FlpbN1d3a3yTIt5vyrXRxbFwhdhGOFHJuqhK8+oR/DBTGB+tMNuQh5pdj4D4DW5kfyeOmeNRVQCJ0s5KqmB9GpGD2h49R6k0np3qWp3rtpamPXF8sT22Gp3dP5dYS39KE1dQKBgQC5WU8MuRMHkyhhFSZ12v8blZKeJdSEnlbbmxtB8mXWNpr/C3+bhurn97dz4kx6Od0OBrG6TS0uPhwtM9gPO4q3i0SHF0MWRXS63r08tKyztTOF/fMD0UMoOaQLduQ/uKZnJuLJnrQO7lRjIQQ+KOFFzGJE6CEgSRcsQCFNuOy6rwKBgGXqsAOqsDRgiRaKCAJB2FHuqr5QczRC1ltY5u1tXkJ7l5rcLdATPRTvO0xVOCigQIIOsti7ZxOTnSdvTmkfPh6CcKXy/wYbt7UfUj+z9XsNJLFUcdUZ8rA9w5J24knwudl/Ha0p8eHSe4aP4jla/w+NL/1NkFvqkyXMLPUi7/ZRAoGAbwzlYfgZQLaYwOINMxvNMVfCiuKbnAHKhLU/9ZkoDtqUry7Se/qwD9/JmLMDo0+79EVqgvbulQA9nY+saiQAjsvweQgk99kRgU0nEJInz1xHzIZE7gqZNCak9QF86/jUKoWP58EgnLmK8gG8KwoPPuSgFC0Ie/GO4sJhsdGUdJ0CgYEApuMUHLIuO/ABwfs/r0KsiJzbgvd7QLGhgjjmIW2x7U3um0JMz7zYJRSKENK9ACOGWoTtRjO5e/7ox1LeGvEzgJ7nSXn+ALW3HvknpvgQrXeCnyQ5UPRYjMP1mnILEgs/LL5vXjofyQWJNULU6q+FkVVjvkKyFUQQ3HI0KUyVlfk='
        )
        res = client.upload(api, params, credentials)
        file.close()
        assertion.success(res)

    def test_upload_failed(self, client):
        """
        Test that uploading a file fails.

        Args:
            self: write your description
            client: write your description
        """
        file_path = './LICENSE'
        api = '/yos/v1.0/mer/merchant/qual/upload2'
        file = open(file_path, mode='rb')
        params = {
            'merQual': ('file_name', file, 'multipart/form-data'),
            'remark': '演示普通参数传递，该api没有remark参数'
        }
        res = client.upload(api, params)
        file.close()
        assertion.failure(res, '40042')

    def test_upload_remote_file(self, client):
        """
        Uploads a file to the API and verifies the upload is successful.

        Args:
            self: write your description
            client: write your description
        """
        file_url = 'https://www.yeepay.com/static/images/logo.png'

        # python2
        # with urllib2.urlopen(file_url) as response:

        # python3
        file = urllib.request.urlopen(file_url)
        api = '/yos/v1.0/mer/merchant/qual/upload'
        params = {
            'merQual': ('file_name', file.read(), 'multipart/form-data'),
            'remark': '演示普通参数传递，该api没有remark参数'
        }
        res = client.upload(api, params)
        assertion.success(res)

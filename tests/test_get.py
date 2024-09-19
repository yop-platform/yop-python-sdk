# -*- coding: utf-8 -*-

import tests.assertion as assertion
from yop_python_sdk.auth.v3signer.credentials import YopCredentials


class Test(object):

    def test_get(self, client):
        """
        Run the get test.

        Args:
            self: write your description
            client: write your description
        """
        api = '/rest/v1.0/cnppay/bank-limit/query'
        params = {'merchantNo': '10000470992'}
        res = client.get(api, params)
        if 'prod' == client.env:
            if 'sm' == client.cert_type:
                assertion.failure(res, '40029')
            else:
                assertion.success(res)
                assert '00000' == res['result']['code']
        else:
            assert '40042' == res['code']

    def test_get_with_rsa_credentials(self, client):
        """
        Specific test for getting data with RSA credentials.

        Args:
            self: write your description
            client: write your description
        """
        api = '/rest/v1.0/cnppay/bank-limit/query'
        params = {'merchantNo': '10000470992'}
        credentials = YopCredentials(
            appKey='OPR:10000470992',
            priKey=
            'MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCMTXz1XQeTx+Eq/Zom7RQeam15IZ23CNCgxl/lG93JFQlGNszQn9yaXlrD4BH99tN6816Ven0pi3+NN0oiunwqfAAiRrxBPXmZKRCjQRKqzAiBYcGZsW9kmzDoCfBLGmmHSWxs58Z3+iAU6RrHLJ5BPhSxpEzed8h5d0pNe8ltDlS9fTr9IvWpVkLKKAPdAmUbRZlbUm/sabdkB9fXGK+dSee+tTJ8lzW2UeSLHeZKKeCbkNckmlD8K+Fgk3N3uEoS0pixycg92VQZrIaH3fKTO/cV1HkubyNEwCF6EwSyOvmyXUr4WqOHzeg+ikPufH1nQvdsudjAv1DN7be65oz7AgMBAAECggEAakL19U+0QXUNUOYqLnk416B7sVaIgOwoNtyIHJnybC2GjKtMjGXHSxNTYy798X9TxLc2V7ghu6lvvaC2gX8EM5ke8NbqFe9dfWbgtwS+AqXtezBy1NjSKTxw2g1M9VTXwCMX/5O7eXrzeWLjaR6d7YP7YF+z6HqIV5bFq9GpSPKGjaiYlZ5rRf0nwen0+BI2wvIRxglvpHvB0zUK3r330Z2gNQvnM2R7YW6Y0zIb3O7ASu+Qh2nGyI4J+OayP1bBohSyZ8KVHc+rDZ3lZRF9Tsj9p9A+JcDS2cLosVRfnVefhRn1356noEB8uR3zNhLHAgEJ3ddZM6DB0u3aKMmIYQKBgQDByH0e8mR3yoFnf6XG2qzflIxwvRPZx7EUhfGby3FlpbN1d3a3yTIt5vyrXRxbFwhdhGOFHJuqhK8+oR/DBTGB+tMNuQh5pdj4D4DW5kfyeOmeNRVQCJ0s5KqmB9GpGD2h49R6k0np3qWp3rtpamPXF8sT22Gp3dP5dYS39KE1dQKBgQC5WU8MuRMHkyhhFSZ12v8blZKeJdSEnlbbmxtB8mXWNpr/C3+bhurn97dz4kx6Od0OBrG6TS0uPhwtM9gPO4q3i0SHF0MWRXS63r08tKyztTOF/fMD0UMoOaQLduQ/uKZnJuLJnrQO7lRjIQQ+KOFFzGJE6CEgSRcsQCFNuOy6rwKBgGXqsAOqsDRgiRaKCAJB2FHuqr5QczRC1ltY5u1tXkJ7l5rcLdATPRTvO0xVOCigQIIOsti7ZxOTnSdvTmkfPh6CcKXy/wYbt7UfUj+z9XsNJLFUcdUZ8rA9w5J24knwudl/Ha0p8eHSe4aP4jla/w+NL/1NkFvqkyXMLPUi7/ZRAoGAbwzlYfgZQLaYwOINMxvNMVfCiuKbnAHKhLU/9ZkoDtqUry7Se/qwD9/JmLMDo0+79EVqgvbulQA9nY+saiQAjsvweQgk99kRgU0nEJInz1xHzIZE7gqZNCak9QF86/jUKoWP58EgnLmK8gG8KwoPPuSgFC0Ie/GO4sJhsdGUdJ0CgYEApuMUHLIuO/ABwfs/r0KsiJzbgvd7QLGhgjjmIW2x7U3um0JMz7zYJRSKENK9ACOGWoTtRjO5e/7ox1LeGvEzgJ7nSXn+ALW3HvknpvgQrXeCnyQ5UPRYjMP1mnILEgs/LL5vXjofyQWJNULU6q+FkVVjvkKyFUQQ3HI0KUyVlfk=',
            cert_type='RSA2048')
        res = client.get(api, params, credentials)
        if 'prod' == client.env:
            assertion.success(res)
            assert '00000' == res['result']['code']
        else:
            assert '40042' == res['code']

    def test_get_failed(self, client):
        """
        Test that getting a resource fails on an untrusted endpoint

        Args:
            self: write your description
            client: write your description
        """
        api = '/rest/v1.0/bank/xxx'
        params = {
            'name': '张三',
            'bankCardNo': '6214830128005989',
            'goods': ['苹果', '香蕉', '草莓']
        }
        res = client.get(api, params)
        assertion.failure(res, '40042')

    def test_get_with_http_param(self, client):
        """
        Run the get test with http parameters.

        Args:
            self: write your description
            client: write your description
        """
        api = '/rest/v1.0/cnppay/bank-limit/query'
        params = {'merchantNo': '10000470992'}
        http_param = {'connect_timeout': 1000,
                      'read_timeout': 1000}
        res = client.get(api, params, http_param=http_param)
        if 'prod' == client.env:
            if 'sm' == client.cert_type:
                assertion.failure(res, '40029')
            else:
                assertion.success(res)
                assert '00000' == res['result']['code']
        else:
            assert '40042' == res['code']

    def test_get_v3(self, client):
        """
        Run the get test with http parameters.

        Args:
            self: write your description
            client: write your description
        """
        api = '/rest/v1.0/trade/order/query'
        params = {'merchantNo': '100800xxxxx',
                  'parentMerchantNo': '100800xxxx',
                  'orderId': 'order_xxxx'}
        res = client.get(api, params)
        if 'prod' == client.env:
            if 'sm' == client.cert_type:
                assertion.failure(res, '40029')
            else:
                assertion.success(res)
                assert 'OPR00000' == res['result']['code']
        else:
            assert 'OPR00000' == res['result']['code']

# -*- coding: utf-8 -*-

import tests.assertion as assertion
from yop_python_sdk.auth.v3signer.credentials import YopCredentials


class Test(object):

    def test_post_json(self, client):
        """
        Test POST JSON response.

        Args:
            self: write your description
            client: write your description
        """
        api = '/rest/v1.0/std/eaccount/topupquery'
        params = {
            'parentMerchantNo': '10000470992',
            'merchantNo': '10000470992',
            'orderId': '12345'
        }
        res = client.post_json(api, params)
        if 'qa' == client.env and '40020' != res.get('code'):
            assertion.success(res)

    def test_post_json_with_credentials(self, client):
        """
        Test for POST json with credentials.

        Args:
            self: write your description
            client: write your description
        """
        if 'sm' == client.cert_type:
            return

        api = '/rest/v1.0/std/eaccount/topupquery'
        params = {
            'parentMerchantNo': '10000470992',
            'merchantNo': '10000470992',
            'orderId': '12345'
        }
        credentials = YopCredentials(
            appKey='OPR:10000470992',
            cert_type='RSA2048',
            priKey=
            'MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCMTXz1XQeTx+Eq/Zom7RQeam15IZ23CNCgxl/lG93JFQlGNszQn9yaXlrD4BH99tN6816Ven0pi3+NN0oiunwqfAAiRrxBPXmZKRCjQRKqzAiBYcGZsW9kmzDoCfBLGmmHSWxs58Z3+iAU6RrHLJ5BPhSxpEzed8h5d0pNe8ltDlS9fTr9IvWpVkLKKAPdAmUbRZlbUm/sabdkB9fXGK+dSee+tTJ8lzW2UeSLHeZKKeCbkNckmlD8K+Fgk3N3uEoS0pixycg92VQZrIaH3fKTO/cV1HkubyNEwCF6EwSyOvmyXUr4WqOHzeg+ikPufH1nQvdsudjAv1DN7be65oz7AgMBAAECggEAakL19U+0QXUNUOYqLnk416B7sVaIgOwoNtyIHJnybC2GjKtMjGXHSxNTYy798X9TxLc2V7ghu6lvvaC2gX8EM5ke8NbqFe9dfWbgtwS+AqXtezBy1NjSKTxw2g1M9VTXwCMX/5O7eXrzeWLjaR6d7YP7YF+z6HqIV5bFq9GpSPKGjaiYlZ5rRf0nwen0+BI2wvIRxglvpHvB0zUK3r330Z2gNQvnM2R7YW6Y0zIb3O7ASu+Qh2nGyI4J+OayP1bBohSyZ8KVHc+rDZ3lZRF9Tsj9p9A+JcDS2cLosVRfnVefhRn1356noEB8uR3zNhLHAgEJ3ddZM6DB0u3aKMmIYQKBgQDByH0e8mR3yoFnf6XG2qzflIxwvRPZx7EUhfGby3FlpbN1d3a3yTIt5vyrXRxbFwhdhGOFHJuqhK8+oR/DBTGB+tMNuQh5pdj4D4DW5kfyeOmeNRVQCJ0s5KqmB9GpGD2h49R6k0np3qWp3rtpamPXF8sT22Gp3dP5dYS39KE1dQKBgQC5WU8MuRMHkyhhFSZ12v8blZKeJdSEnlbbmxtB8mXWNpr/C3+bhurn97dz4kx6Od0OBrG6TS0uPhwtM9gPO4q3i0SHF0MWRXS63r08tKyztTOF/fMD0UMoOaQLduQ/uKZnJuLJnrQO7lRjIQQ+KOFFzGJE6CEgSRcsQCFNuOy6rwKBgGXqsAOqsDRgiRaKCAJB2FHuqr5QczRC1ltY5u1tXkJ7l5rcLdATPRTvO0xVOCigQIIOsti7ZxOTnSdvTmkfPh6CcKXy/wYbt7UfUj+z9XsNJLFUcdUZ8rA9w5J24knwudl/Ha0p8eHSe4aP4jla/w+NL/1NkFvqkyXMLPUi7/ZRAoGAbwzlYfgZQLaYwOINMxvNMVfCiuKbnAHKhLU/9ZkoDtqUry7Se/qwD9/JmLMDo0+79EVqgvbulQA9nY+saiQAjsvweQgk99kRgU0nEJInz1xHzIZE7gqZNCak9QF86/jUKoWP58EgnLmK8gG8KwoPPuSgFC0Ie/GO4sJhsdGUdJ0CgYEApuMUHLIuO/ABwfs/r0KsiJzbgvd7QLGhgjjmIW2x7U3um0JMz7zYJRSKENK9ACOGWoTtRjO5e/7ox1LeGvEzgJ7nSXn+ALW3HvknpvgQrXeCnyQ5UPRYjMP1mnILEgs/LL5vXjofyQWJNULU6q+FkVVjvkKyFUQQ3HI0KUyVlfk='
        )
        res = client.post_json(api, params, credentials)
        if 'qa' == client.env and '40020' != res.get('code'):
            assertion.success(res)

    def test_post_json_failed(self, client):
        """
        Test that POST request succeeds when JSON is not successful.

        Args:
            self: write your description
            client: write your description
        """
        api = '/rest/v1.0/std/eaccount/topupquery1'
        params = {
            'parentMerchantNo': '10000470992',
            'merchantNo': '10000470992',
            'orderId': ['苹果', '香蕉', '草莓']
        }
        res = client.post_json(api, params)
        assertion.failure(res, '40042')

    def test_post_json_failed(self, client):
        """
        Test that POST request with json fails.

        Args:
            self: write your description
            client: write your description
        """
        api = '/rest/v1.0/std/eaccount/topupquery'
        params = {
            'parentMerchantNo':
            '10000470992',
            'merchantNo':
            '10000470992',
            'orderId': ['苹果', '香蕉', '草莓'],
            'productInfo':
            '[{\"productCode\":\"MERCHANT_SCAN_ALIPAY_OFFLINE\",\"rateType\":\"SINGLE_PERCENT\",\"percentRate\":\"0.1\"},{\"productCode\":\"MERCHANT_SCAN_UNIONPAY_CREDIT\",\"rateType\":\"SINGLE_FIXED\",\"fixedRate\":\"1\"}]'
        }
        res = client.post_json(api, params)
        assertion.failure(res, '40020')

    def test_post_json_with_http_param(self, client):
        """
        Test POST JSON response with http parameters.

        Args:
            self: write your description
            client: write your description
        """
        api = '/rest/v1.0/std/eaccount/topupquery'
        params = {
            'parentMerchantNo': '10000470992',
            'merchantNo': '10000470992',
            'orderId': '12345'
        }
        http_param = {'connect_timeout': 1000,
                      'read_timeout': 1000}
        res = client.post_json(api, params, http_param=http_param)
        if 'qa' == client.env and '40020' != res.get('code'):
            assertion.success(res)

    def test_post_form_v3(self, client):
        """
        Test POST JSON response with http parameters.

        Args:
            self: write your description
            client: write your description
        """
        api = '/rest/v1.0/aggpay/pay'
        params = {
            "orderId": "xxxx",
            "orderAmount": 1,
            "payWay": "MERCHANT_SCAN",
            "channel": "WECHAT",
            "authCode": "0.01",
            "userIp": "172.xx.x.xx",
            "terminalId": "terminalId",
            "terminalSceneInfo": "xxx"
        }
        res = client.post(api, params)
        if 'qa' == client.env:
            assert '40020' != res.get('code')

    def test_post_json_v3(self, client):
        """
        Test POST JSON response with http parameters.

        Args:
            self: write your description
            client: write your description
        """
        api = '/rest/v1.0/kj/lp/query'
        params = {
            "sourceCurrency": "xxx"
        }
        res = client.post_json(api, params)
        if 'qa' == client.env:
            assert '40020' != res.get('code')

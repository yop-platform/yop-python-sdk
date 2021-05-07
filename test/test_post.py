# -*- coding: utf-8 -*-

import test.assertion as assertion
from auth.v3signer.credentials import YopCredentials


class Test(object):
    def test_post(self, client):
        api = '/rest/v1.0/trade/order'
        params = {
            'orderId': '140676',
            'orderType': 'REALTIME',
            'salesProductCode': 'DSBZB',
            'bizSystemNo': 'DS',
            'assureType': 'REALTIME',
            'assurePeriod': '30',
            'productVersion': 'DSBZB',
            'goodsParamExt': '{\"goodsDesc\":\"微商平台H5订单:2020112719083965\", \"goodsName\":\"kk\"}',
            'orderAmount': '898.00',
            'notifyUrl': 'http://apitest.gouwu.cn/pay/yop/notify',
            'timeoutExpressType': 'MINUTE',
            'timeoutExpress': '30',
            'parentMerchantNo': '10000466938',
            'merchantNo': '10000466938'
        }
        res = client.post(api, params)
        if 'prod' == client.env:
            if 'sm' == client.cert_type:
                assertion.failure(res, '40029')
            else:
                assert 'OPR10008' == res['result']['code']
            # assertion.success(res)
        else:
            assertion.failure(res, '40042')

    def test_post_with_credentials(self, client):
        if 'sm' == client.cert_type:
            return

        api = '/rest/v1.0/trade/order'
        params = {
            'orderId': '140676',
            'orderType': 'REALTIME',
            'salesProductCode': 'DSBZB',
            'bizSystemNo': 'DS',
            'assureType': 'REALTIME',
            'assurePeriod': '30',
            'productVersion': 'DSBZB',
            'goodsParamExt': '{\"goodsDesc\":\"微商平台H5订单:2020112719083965\", \"goodsName\":\"kk\"}',
            'orderAmount': '898.00',
            'notifyUrl': 'http://apitest.gouwu.cn/pay/yop/notify',
            'timeoutExpressType': 'MINUTE',
            'timeoutExpress': '30',
            'parentMerchantNo': '10000466938',
            'merchantNo': '10000466938'
        }
        credentials = YopCredentials(appKey='OPR:10000470992',
                                     priKey='MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCMTXz1XQeTx+Eq/Zom7RQeam15IZ23CNCgxl/lG93JFQlGNszQn9yaXlrD4BH99tN6816Ven0pi3+NN0oiunwqfAAiRrxBPXmZKRCjQRKqzAiBYcGZsW9kmzDoCfBLGmmHSWxs58Z3+iAU6RrHLJ5BPhSxpEzed8h5d0pNe8ltDlS9fTr9IvWpVkLKKAPdAmUbRZlbUm/sabdkB9fXGK+dSee+tTJ8lzW2UeSLHeZKKeCbkNckmlD8K+Fgk3N3uEoS0pixycg92VQZrIaH3fKTO/cV1HkubyNEwCF6EwSyOvmyXUr4WqOHzeg+ikPufH1nQvdsudjAv1DN7be65oz7AgMBAAECggEAakL19U+0QXUNUOYqLnk416B7sVaIgOwoNtyIHJnybC2GjKtMjGXHSxNTYy798X9TxLc2V7ghu6lvvaC2gX8EM5ke8NbqFe9dfWbgtwS+AqXtezBy1NjSKTxw2g1M9VTXwCMX/5O7eXrzeWLjaR6d7YP7YF+z6HqIV5bFq9GpSPKGjaiYlZ5rRf0nwen0+BI2wvIRxglvpHvB0zUK3r330Z2gNQvnM2R7YW6Y0zIb3O7ASu+Qh2nGyI4J+OayP1bBohSyZ8KVHc+rDZ3lZRF9Tsj9p9A+JcDS2cLosVRfnVefhRn1356noEB8uR3zNhLHAgEJ3ddZM6DB0u3aKMmIYQKBgQDByH0e8mR3yoFnf6XG2qzflIxwvRPZx7EUhfGby3FlpbN1d3a3yTIt5vyrXRxbFwhdhGOFHJuqhK8+oR/DBTGB+tMNuQh5pdj4D4DW5kfyeOmeNRVQCJ0s5KqmB9GpGD2h49R6k0np3qWp3rtpamPXF8sT22Gp3dP5dYS39KE1dQKBgQC5WU8MuRMHkyhhFSZ12v8blZKeJdSEnlbbmxtB8mXWNpr/C3+bhurn97dz4kx6Od0OBrG6TS0uPhwtM9gPO4q3i0SHF0MWRXS63r08tKyztTOF/fMD0UMoOaQLduQ/uKZnJuLJnrQO7lRjIQQ+KOFFzGJE6CEgSRcsQCFNuOy6rwKBgGXqsAOqsDRgiRaKCAJB2FHuqr5QczRC1ltY5u1tXkJ7l5rcLdATPRTvO0xVOCigQIIOsti7ZxOTnSdvTmkfPh6CcKXy/wYbt7UfUj+z9XsNJLFUcdUZ8rA9w5J24knwudl/Ha0p8eHSe4aP4jla/w+NL/1NkFvqkyXMLPUi7/ZRAoGAbwzlYfgZQLaYwOINMxvNMVfCiuKbnAHKhLU/9ZkoDtqUry7Se/qwD9/JmLMDo0+79EVqgvbulQA9nY+saiQAjsvweQgk99kRgU0nEJInz1xHzIZE7gqZNCak9QF86/jUKoWP58EgnLmK8gG8KwoPPuSgFC0Ie/GO4sJhsdGUdJ0CgYEApuMUHLIuO/ABwfs/r0KsiJzbgvd7QLGhgjjmIW2x7U3um0JMz7zYJRSKENK9ACOGWoTtRjO5e/7ox1LeGvEzgJ7nSXn+ALW3HvknpvgQrXeCnyQ5UPRYjMP1mnILEgs/LL5vXjofyQWJNULU6q+FkVVjvkKyFUQQ3HI0KUyVlfk=',
                                     cert_type='RSA2048')
        res = client.post(api, params, credentials)
        if 'prod' == client.env:
            assert 'OPR10008' == res['result']['code']
            assertion.success(res)
        else:
            assertion.failure(res, '40042')

    def test_post_failed(self, client):
        api = '/rest/v1.0/trade/order'
        params = {
            'parentMerchantNo': '10000470992',
            'merchantNo': '10000470992',
            'orderId': '123',
            'orderAmount': '0.01',
            'notifyUrl': 'https://test.com',
        }
        res = client.post(api, params)
        # assert 'OPR00058' == res['result']['code']
        if 'prod' == client.env:
            if 'sm' == client.cert_type:
                assertion.failure(res, '40029')
            else:
                assert 'OPR10008' == res['result']['code']
        else:
            assertion.failure(res, '40042')

    def test_post_404(self, client):
        api = '/rest/v1.0/bank/xxx'
        params = {
            'name': '张三',
            'bankCardNo': '6214830128005989',
            'goods': ['苹果', '香蕉', '草莓']
        }
        res = client.post(api, params)
        assertion.failure(res, '40042')

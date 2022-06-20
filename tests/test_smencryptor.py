# -*- coding: utf-8 -*-

import yop_python_sdk.utils.yop_logger as yop_logger
from yop_python_sdk.auth.v3signer.credentials import YopCredentials

logger = yop_logger.get_logger()

text = b"yop-auth-v3/app_100800095600038/2021-04-23T10:35:23Z/1800\nPOST\n/rest/file/upload\n\ncontent-type:application%2Fx-www-form-urlencoded\nx-yop-appkey:app_100800095600038\nx-yop-request-id:c81634dc-9404-4cbe-8ccb-27269a7ced55"


class Test(object):
    # def test_sign_self(self):
    #     credentials = YopCredentials(
    #         appKey='OPR:10000470992',
    #         priKey='ME0CAQAwEwYHKoZIzj0CAQYIKoEcz1UBgi0EMzAxAgEBBCCSY5qqLNmqfx3/6levxQka50cIGTTny495Pk+rS3A3o6AKBggqgRzPVQGCLQ==',
    #         cert_type='SM')
    #     encryptor = credentials.encryptor

    #     signature, a, ha = encryptor.signature(text)
    #     logger.debug("signature:{}".format(signature))

    #     result = encryptor.verify_signature(text, signature)
    #     assert result

    def test_sign_yop(self, client):
        """
        Verify the signature of the text.

        Args:
            self: write your description
            client: write your description
        """
        # QA
        if 'qa' == client.env:
            sign_2 = "pEUtFQeSbFaZs1qd8h4AopxwDMOOEUpX4k58zwQQHNcTznTs0U-GLaxsh9OPFCcn_gDgf2jMiC2Fa_5a5B2Fhw"
            result = client.yop_encryptor_dict['SM2'].verify_signature(
                text, sign_2, serial_no='275568425014')
            assert result

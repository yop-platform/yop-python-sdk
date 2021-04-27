# -*- coding: utf-8 -*-

import utils.yop_logging_utils as yop_logging_utils
import utils.security.smencryptor as SmEncryptor
import sys
sys.path.append("./")

logger = yop_logging_utils.get_logger()

text = b"yop-auth-v3/app_100800095600038/2021-04-23T10:35:23Z/1800\nPOST\n/rest/file/upload\n\ncontent-type:application%2Fx-www-form-urlencoded\nx-yop-appkey:app_100800095600038\nx-yop-request-id:c81634dc-9404-4cbe-8ccb-27269a7ced55"


class Test(object):
    def test_sign_self(self):
        privateKey = "00B9AB0B828FF68872F21A837FC303668428DEA11DCD1B24429D0C99E24EED83D5"
        publicKey = "B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A83081A6994B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E24620207"

        encryptor = SmEncryptor.SmEncryptor(publicKey, privateKey)

        signature = encryptor.signature(text)
        logger.debug("signature:{}".format(signature))

        result = encryptor.verify_signature(text, signature)
        assert result

    def test_sign_yop(self):
        privateKey = "92639aaa2cd9aa7f1dffea57afc5091ae747081934e7cb8f793e4fab4b7037a3"
        publicKey = "a52b1da90d07177e074265bf04f066565292079040609119f1fb9b6e797c1c68c275a26d2abf56f18f12d4c878951b718e0b442bd66dbead4fb69554d66303f8"

        encryptor = SmEncryptor.SmEncryptor(publicKey, privateKey)

        signature_16 = encryptor.signature(text)
        result = encryptor.verify_signature(text, signature_16)
        # assert result

        # QA
        sign_2 = "TQQ2QyArDmhPUmFdX5rmKgOnX7rbtWNV1ZqpzyIE1oWoTeH7LOxKSZPYpK1MmAiF4GXdSAXo7ffEuvb5i-iPeg"
        result = encryptor.verify_signature(text, sign_2)
        assert result

# -*- coding: utf-8 -*-

import utils.yop_security_utils as yop_security_utils
from utils.yop_config_utils import YopClientConfig
import sys
sys.path.append("./")

clientConfig = YopClientConfig()
private_key = clientConfig.get_credentials().get_priKey()
public_key = clientConfig.get_yop_public_key()
public_key = yop_security_utils.parse_pri_key(
    'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAjE189V0Hk8fhKv2aJu0UHmpteSGdtwjQoMZf5RvdyRUJRjbM0J/cml5aw+AR/fbTevNelXp9KYt/jTdKIrp8KnwAIka8QT15mSkQo0ESqswIgWHBmbFvZJsw6AnwSxpph0lsbOfGd/ogFOkaxyyeQT4UsaRM3nfIeXdKTXvJbQ5UvX06/SL1qVZCyigD3QJlG0WZW1Jv7Gm3ZAfX1xivnUnnvrUyfJc1tlHkix3mSingm5DXJJpQ/CvhYJNzd7hKEtKYscnIPdlUGayGh93ykzv3FdR5Lm8jRMAhehMEsjr5sl1K+Fqjh83oPopD7nx9Z0L3bLnYwL9Qze23uuaM+wIDAQAB')


def test_envelope():
    content = '{"date":"20181014000000","aaa":"","boolean":true,"SIZE":-14,"name":"易宝支付","dou":12.134}'
    print('content:{}'.format(content))

    enc = yop_security_utils.envelope_encrypt(content, private_key, public_key)
    print('enc:{}'.format(enc))

    plain = yop_security_utils.envelope_decrypt(enc, private_key, public_key)
    print('plain:{}'.format(plain))

    assert plain == content


test_envelope()

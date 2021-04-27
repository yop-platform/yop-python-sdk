# -*- coding: utf-8 -*-

def success(res):
    if res.__contains__('code'):
        code = res['code']
        assert '40020' != code
        assert '40021' != code
        assert '40029' != code
        assert '40041' != code
        assert '40042' != code
        assert '40044' != code
        assert '40047' != code
        assert '40049' != code


def failure(res, exceptCode, key='code'):
    if res.__contains__(key):
        code = res[key]
        assert exceptCode == code
        return

    assert False

# -*- coding: utf-8 -*-

import pytest

if __name__ == '__main__':
    pytest.main(["-s", "test/"])
    # pytest.main(["-s", "test/", "--env", "qa"])  # upload & download
    # pytest.main(["-s", "test/", "--cert-type", "sm"])
    # pytest.main(["-s", "test/", "--env", "qa", "--cert-type", "sm"])

    # pytest.main(["-s", "test/test_get.py"])
    # pytest.main(["-s", "test/test_get.py", "--cert-type", "sm"])
    # pytest.main(["-s", "test/test_get.py", "--env", "qa"])
    # pytest.main(["-s", "test/test_get.py", "--env", "qa", "--cert-type", "sm"])

    # pytest.main(["-s", "test/test_post.py"])
    # pytest.main(["-s", "test/test_post.py", "--cert-type", "sm"])
    # pytest.main(["-s", "test/test_post.py", "--env", "qa"])  # 40042
    # pytest.main(["-s", "test/test_post.py", "--env", "qa", "--cert-type", "sm"])

    # pytest.main(["-s", "test/test_post_json.py"])
    # pytest.main(["-s", "test/test_post_json.py", "--cert-type", "sm"])  # ???
    # pytest.main(["-s", "test/test_post_json.py", "--env", "qa"])  # 40042
    # pytest.main(["-s", "test/test_post_json.py", "--env", "qa", "--cert-type", "sm"]) #40020

    # pytest.main(["-s", "test/test_upload.py"])
    # pytest.main(["-s", "test/test_upload.py", "--cert-type", "sm"])  # ???
    # pytest.main(["-s", "test/test_upload.py", "--env", "qa"])  # 40042
    # pytest.main(["-s", "test/test_upload.py", "--env", "qa", "--cert-type", "sm"]) # 40042

    # pytest.main(["-s", "test/test_rsa_envelope.py"])
    # pytest.main(["-s", "test/test_rsa_envelope.py", "--env", "qa"])

    # pytest.main(["-s", "test/test_rsaencryptor.py"])  # 测试用例只适用于生产环境
    # pytest.main(["-s", "test/test_rsaencryptor.py", "--env", "qa"])

    # pytest.main(["-s", "test/test_smencryptor.py", "--cert-type", "sm"])
    # pytest.main(["-s", "test/test_smencryptor.py", "--env", "qa", "--cert-type", "sm"])

    # 尚未通过的：

    # pytest.main(["-s", "test/test_get.py", "--cert-type", "sm"])  # 生产的测试账号是否正确？

    # pytest.main(["-s", "test/test_download.py"])
    # pytest.main(["-s", "test/test_download.py", "--env", "qa"])
    # pytest.main(["-s", "test/test_download.py", "--cert-type", "sm"])
    # pytest.main(["-s", "test/test_download.py", "--env", "qa", "--cert-type", "sm"])

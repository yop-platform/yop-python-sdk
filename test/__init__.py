# -*- coding: utf-8 -*-

import pytest

if __name__ == '__main__':
    # pytest.main(["-s", "test/"])
    # pytest.main(["-s", "test/test_get.py"])
    # pytest.main(["-s", "test/test_post.py"])
    # pytest.main(["-s", "test/test_post_json.py"])
    # pytest.main(["-s", "test/test_upload.py"])
    # pytest.main(["-s", "test/test_download.py"])
    # pytest.main(["-s", "test/test_post_json.py"])
    # pytest.main(["-s", "test/test_rsa_envelope.py"])
    pytest.main(["-s", "test/test_smencryptor.py", "--env", "qa", "--cert-type", "sm"])
    # pytest.main(["-s", "test/test_rsaencryptor.py", "--env", "qa", "--cert-type", "rsa"])

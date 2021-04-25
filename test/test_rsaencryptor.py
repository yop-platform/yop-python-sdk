# -*- coding: utf-8 -*-

import sys
sys.path.append("./")
import utils.yop_security_utils as yop_security_utils
import utils.security.rsaencryptor as RsaEncryptor
import utils.yop_logging_utils as yop_logging_utils

logger = yop_logging_utils.get_logger()

text = b"yop-auth-v3/OPR:10012481831/20170124T021133Z/1800\nPOST\n/rest/v2.0/opr/queryorder\nparentCustomerNo=10012481831&requestId=requestId1480392119078&uniqueOrderNo=1001201611290000000000000808\nx-yop-appkey:OPR%3A10012481831\nx-yop-date:20170124T021133Z\nx-yop-request-id:01e447af-9749-4075-8e6c-17df519f2720"


class Test(object):
    def test_sign_self(self):
        isv_private_key = yop_security_utils.parse_pri_key(
            'MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQChnRCVXUj+zLgJyeskNhflb7Go67dmkOSoXCYIklAYpcRC1+3Mbh4Ju3Qb0y3X92XPir3tk8aXurkuk93PFig582BSPKixBSASXLLGiwBiK3pyBuJoabHvIAZuAFXYDPaXQJE2HAtrADYGcbWvsdc94umihQU67XImjgOiBj0ZgeIhsjcsCEFgmzAw4xNW1dqza8grzcvBmmqyYUig5yS5IywciHtPYG+0FiLzjT+o6LoaMoaF/IAYq8EkbPC8Jra3IFqvZsR8Krr5DipCs87NRb3SILjUCTZyaaeKMf73m1grnYyP9CcBlwaQydKxnM0tDu3Xnm8FKiIK95Oz31U1AgMBAAECggEAMhOr9sw/+QvQHuBdJwxH3UT9xLy9SF+vKmfbNR65CNocdSXZPlYEorld4d1OwDOdbXCtJzd5+rvV85PH0AoqjsJV30WCc8+Fv4rPrmuVw9V7DGgLsZTGmLTQqTcbYmWp5vYPyLdp5k7bbqW/SWCOtFNiV4RmOXsnusCYaZULS6KPXpjpnpt4shesK1SdVC2uCO7eUKf4aN8kKSaGA6rKK9aiBwuiwnqAc5Z0++HxnTu3zjbrfmUVchFCLPU31zXlfzFfZW5hUu7whUcj7914V8q5AkuEEoqpFxAcirsH0ZQE7xtPFez+00OZU42NtyqlieUSE8zYglxVRjZ9pa4GwQKBgQDkNYmzCISJXbAqcNJCY9Og/tMBaZNrYh3Z51eENxxARoVD3jj462hsZMLd+ZH6AuerT7xEHgd4QxtLDVzMpXF4wwlZydu8DrTr7KZPliHFTWPs1ntOnsCeWhFnIHcKVnay9YkiMT+WqTwpGXTkpo68oI+vu3EKY9DSPp+di0CeEQKBgQC1S2WREQHOGnzQL2vqPZA45BL0k6F/KPgb2gTF4sRTkOZr4mnb/vmTt1E+xRKwTBCzsnzk4x2DFgMtYr9ZODtg9egmfd7BdjFzXw7f+ACoDE4SHtl2YqHqbnt6qDAwY6Ahz+0hmjG/2xD4lK5h0yDDh2iwoQnAKdQnaam3ZsLw5QKBgQDSsot7/LVBjnqD9L5sBXbzAdMXTr6JOoGNGga3T5qJzZJk4tt/FvnGehFgmHeqeNwkUu3jhkYnRu4AEUpIt8dYU9piR/jUXE+2Mzwp5tcvLxC/LheSswfsLAQ9TsAZj1LwT7pZE1c+ZungmFxQb2cByMxg15K6oQW/14nPDy6NwQKBgBV/MjToWllxBJm+9cHZuO82BBViKAUm+3x59pTsVbE+/kOOnlTKwBdG5mhV/+hNrLFSGcMeNxKjGo9YJS5UH55YqkVeKXqxJB31CJOAGbvTcbJuXATQnzhoD1Y0+TnTplo8CHcyjHGebT28i4zn9vuYY86F2d0iWJivy8MGeVkNAoGADUAug8jLk19hyejyvHK+nuQJ3gnbdSaUE3uTF5YbVxMhXuKq/Q8lkx74p8mc5x+NkzwrcpSL7YQ9Px4BopU9kvYHVChNVMVCnYRJ16MmEws2N9L4qdsmVKX8j0n+55DZsTPZfhPxP/Yuj6indAq7om+wbkuVTuPDhtDyHcfjHd8=')
        isv_public_key = yop_security_utils.parse_pub_key(
            'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAoZ0QlV1I/sy4CcnrJDYX5W+xqOu3ZpDkqFwmCJJQGKXEQtftzG4eCbt0G9Mt1/dlz4q97ZPGl7q5LpPdzxYoOfNgUjyosQUgElyyxosAYit6cgbiaGmx7yAGbgBV2Az2l0CRNhwLawA2BnG1r7HXPeLpooUFOu1yJo4DogY9GYHiIbI3LAhBYJswMOMTVtXas2vIK83LwZpqsmFIoOckuSMsHIh7T2BvtBYi840/qOi6GjKGhfyAGKvBJGzwvCa2tyBar2bEfCq6+Q4qQrPOzUW90iC41Ak2cmmnijH+95tYK52Mj/QnAZcGkMnSsZzNLQ7t155vBSoiCveTs99VNQIDAQAB')

        encryptor = RsaEncryptor.RsaEncryptor(isv_private_key, isv_public_key)
        signature = encryptor.signature(text)
        logger.debug("signature:{}".format(signature))

        result = encryptor.verify_signature(signature, text)
        assert result

    def test_sign_yop(self, clientConfig):
        yop_public_key = clientConfig.get_yop_public_key()
        isv_private_key = clientConfig.get_credentials().get_priKey()
        encryptor = RsaEncryptor.RsaEncryptor(isv_private_key, yop_public_key)
        # signature_16 = smEncryptor.signature(text)
        # result = smEncryptor.verify_signature(signature_16, text)
        # assert result

        sign_2 = "PDuHKHjR2M1AvelHN1ARtKwN0zFLPsPqL4YkNCUEQq_-mbdWgjv8yU0hKjnI6_pUwT_xY4ocaMY6oeNpBodbrQ"
        result = encryptor.verify_signature(sign_2, text)
        assert result

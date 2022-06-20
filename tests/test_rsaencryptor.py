# -*- coding: utf-8 -*-

import yop_python_sdk.utils.yop_logger as yop_logger
import yop_python_sdk.security.encryptor.rsaencryptor as RsaEncryptor
import yop_python_sdk.utils.yop_security_utils as yop_security_utils

logger = yop_logger.get_logger()

text = u'{\"result\":{\"code\":\"99999\",\"message\":\"\u8c03\u7528NCPay\u67e5\u8be2\u94f6\u884c\u5217\u8868\u5931\u8d25\"}}'


class Test(object):
    # def test_sign_self(self, client):
    #     if 'sm' == client.cert_type:
    #         return

    #     isv_private_key = yop_security_utils.parse_rsa_pri_key(
    #         'MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQChnRCVXUj+zLgJyeskNhflb7Go67dmkOSoXCYIklAYpcRC1+3Mbh4Ju3Qb0y3X92XPir3tk8aXurkuk93PFig582BSPKixBSASXLLGiwBiK3pyBuJoabHvIAZuAFXYDPaXQJE2HAtrADYGcbWvsdc94umihQU67XImjgOiBj0ZgeIhsjcsCEFgmzAw4xNW1dqza8grzcvBmmqyYUig5yS5IywciHtPYG+0FiLzjT+o6LoaMoaF/IAYq8EkbPC8Jra3IFqvZsR8Krr5DipCs87NRb3SILjUCTZyaaeKMf73m1grnYyP9CcBlwaQydKxnM0tDu3Xnm8FKiIK95Oz31U1AgMBAAECggEAMhOr9sw/+QvQHuBdJwxH3UT9xLy9SF+vKmfbNR65CNocdSXZPlYEorld4d1OwDOdbXCtJzd5+rvV85PH0AoqjsJV30WCc8+Fv4rPrmuVw9V7DGgLsZTGmLTQqTcbYmWp5vYPyLdp5k7bbqW/SWCOtFNiV4RmOXsnusCYaZULS6KPXpjpnpt4shesK1SdVC2uCO7eUKf4aN8kKSaGA6rKK9aiBwuiwnqAc5Z0++HxnTu3zjbrfmUVchFCLPU31zXlfzFfZW5hUu7whUcj7914V8q5AkuEEoqpFxAcirsH0ZQE7xtPFez+00OZU42NtyqlieUSE8zYglxVRjZ9pa4GwQKBgQDkNYmzCISJXbAqcNJCY9Og/tMBaZNrYh3Z51eENxxARoVD3jj462hsZMLd+ZH6AuerT7xEHgd4QxtLDVzMpXF4wwlZydu8DrTr7KZPliHFTWPs1ntOnsCeWhFnIHcKVnay9YkiMT+WqTwpGXTkpo68oI+vu3EKY9DSPp+di0CeEQKBgQC1S2WREQHOGnzQL2vqPZA45BL0k6F/KPgb2gTF4sRTkOZr4mnb/vmTt1E+xRKwTBCzsnzk4x2DFgMtYr9ZODtg9egmfd7BdjFzXw7f+ACoDE4SHtl2YqHqbnt6qDAwY6Ahz+0hmjG/2xD4lK5h0yDDh2iwoQnAKdQnaam3ZsLw5QKBgQDSsot7/LVBjnqD9L5sBXbzAdMXTr6JOoGNGga3T5qJzZJk4tt/FvnGehFgmHeqeNwkUu3jhkYnRu4AEUpIt8dYU9piR/jUXE+2Mzwp5tcvLxC/LheSswfsLAQ9TsAZj1LwT7pZE1c+ZungmFxQb2cByMxg15K6oQW/14nPDy6NwQKBgBV/MjToWllxBJm+9cHZuO82BBViKAUm+3x59pTsVbE+/kOOnlTKwBdG5mhV/+hNrLFSGcMeNxKjGo9YJS5UH55YqkVeKXqxJB31CJOAGbvTcbJuXATQnzhoD1Y0+TnTplo8CHcyjHGebT28i4zn9vuYY86F2d0iWJivy8MGeVkNAoGADUAug8jLk19hyejyvHK+nuQJ3gnbdSaUE3uTF5YbVxMhXuKq/Q8lkx74p8mc5x+NkzwrcpSL7YQ9Px4BopU9kvYHVChNVMVCnYRJ16MmEws2N9L4qdsmVKX8j0n+55DZsTPZfhPxP/Yuj6indAq7om+wbkuVTuPDhtDyHcfjHd8=')
    #     isv_public_key = yop_security_utils.parse_rsa_pub_key(
    #         'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAoZ0QlV1I/sy4CcnrJDYX5W+xqOu3ZpDkqFwmCJJQGKXEQtftzG4eCbt0G9Mt1/dlz4q97ZPGl7q5LpPdzxYoOfNgUjyosQUgElyyxosAYit6cgbiaGmx7yAGbgBV2Az2l0CRNhwLawA2BnG1r7HXPeLpooUFOu1yJo4DogY9GYHiIbI3LAhBYJswMOMTVtXas2vIK83LwZpqsmFIoOckuSMsHIh7T2BvtBYi840/qOi6GjKGhfyAGKvBJGzwvCa2tyBar2bEfCq6+Q4qQrPOzUW90iC41Ak2cmmnijH+95tYK52Mj/QnAZcGkMnSsZzNLQ7t155vBSoiCveTs99VNQIDAQAB')

    #     encryptor = RsaEncryptor.RsaEncryptor(isv_private_key, isv_public_key)
    #     signature, algorithm, hash_algorithm = encryptor.signature(text)
    #     logger.debug("signature:{}".format(signature))

    #     result = encryptor.verify_signature(text, signature)
    #     assert result

    def test_sign_yop(self, client):
        """
        Verify the sign of the yop certificate

        Args:
            self: write your description
            client: write your description
        """
        if 'sm' == client.cert_type or 'qa' == client.env:
            return

        clientConfig = client.clientConfig
        yop_public_key = list(
            clientConfig.get_yop_public_key().get('RSA2048').values())[0]
        isv_private_key = clientConfig.get_credentials().get_priKey()
        encryptor = RsaEncryptor.RsaEncryptor(isv_private_key, yop_public_key)
        # signature_16, algorithm, hash_algorithm = encryptor.signature(text)
        # result = encryptor.verify_signature(text, signature_16)
        # assert result

        sign_2 = "5vAp3cvQMNep9KQFfDMDEpRRJxN5CQsdGPVgSAWJU+wQJYEfQpVI3gbcD+ltOISJayt+C0xOF7FM4EaQqwvg8x5jKJf3M45mvdoHvpDsfVx6ENY+khS/d0brOtPVtC+NEs4/xto+w749p+C0ZqqIEa1S/n0SmzlQXTKOb3csH1ChO7CX9cazfolrySOB/Yo6EPNWJZkkXU3jbMgjtvCYNf9KYowox1dznkdY0phN8N/tTf7F2+BVFdMe8LCEeImn1neTvmrU3/qg+BXU8UNKFk219476fpn9TIqERzZBZ4SnqkUsU6ycDX14n2BfBqVP9zCsOqMgKd6IV4r52cp62g=="
        result = encryptor.verify_signature(text, sign_2)
        assert result

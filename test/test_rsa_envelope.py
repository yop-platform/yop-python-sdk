# -*- coding: utf-8 -*-

import utils.yop_security_utils as yop_security_utils
from client.yop_client_config import YopClientConfig
from security.encryptor.rsaencryptor import RsaEncryptor
import sys
sys.path.append("./")

clientConfig = YopClientConfig(config_file='config/yop_sdk_config_rsa_qa.json')
# isv_private_key = clientConfig.get_credentials().get_priKey()

# yop_public_key = yop_security_utils.parse_pub_key()
isv_private_key = yop_security_utils.parse_rsa_pri_key(
    'MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQChnRCVXUj+zLgJyeskNhflb7Go67dmkOSoXCYIklAYpcRC1+3Mbh4Ju3Qb0y3X92XPir3tk8aXurkuk93PFig582BSPKixBSASXLLGiwBiK3pyBuJoabHvIAZuAFXYDPaXQJE2HAtrADYGcbWvsdc94umihQU67XImjgOiBj0ZgeIhsjcsCEFgmzAw4xNW1dqza8grzcvBmmqyYUig5yS5IywciHtPYG+0FiLzjT+o6LoaMoaF/IAYq8EkbPC8Jra3IFqvZsR8Krr5DipCs87NRb3SILjUCTZyaaeKMf73m1grnYyP9CcBlwaQydKxnM0tDu3Xnm8FKiIK95Oz31U1AgMBAAECggEAMhOr9sw/+QvQHuBdJwxH3UT9xLy9SF+vKmfbNR65CNocdSXZPlYEorld4d1OwDOdbXCtJzd5+rvV85PH0AoqjsJV30WCc8+Fv4rPrmuVw9V7DGgLsZTGmLTQqTcbYmWp5vYPyLdp5k7bbqW/SWCOtFNiV4RmOXsnusCYaZULS6KPXpjpnpt4shesK1SdVC2uCO7eUKf4aN8kKSaGA6rKK9aiBwuiwnqAc5Z0++HxnTu3zjbrfmUVchFCLPU31zXlfzFfZW5hUu7whUcj7914V8q5AkuEEoqpFxAcirsH0ZQE7xtPFez+00OZU42NtyqlieUSE8zYglxVRjZ9pa4GwQKBgQDkNYmzCISJXbAqcNJCY9Og/tMBaZNrYh3Z51eENxxARoVD3jj462hsZMLd+ZH6AuerT7xEHgd4QxtLDVzMpXF4wwlZydu8DrTr7KZPliHFTWPs1ntOnsCeWhFnIHcKVnay9YkiMT+WqTwpGXTkpo68oI+vu3EKY9DSPp+di0CeEQKBgQC1S2WREQHOGnzQL2vqPZA45BL0k6F/KPgb2gTF4sRTkOZr4mnb/vmTt1E+xRKwTBCzsnzk4x2DFgMtYr9ZODtg9egmfd7BdjFzXw7f+ACoDE4SHtl2YqHqbnt6qDAwY6Ahz+0hmjG/2xD4lK5h0yDDh2iwoQnAKdQnaam3ZsLw5QKBgQDSsot7/LVBjnqD9L5sBXbzAdMXTr6JOoGNGga3T5qJzZJk4tt/FvnGehFgmHeqeNwkUu3jhkYnRu4AEUpIt8dYU9piR/jUXE+2Mzwp5tcvLxC/LheSswfsLAQ9TsAZj1LwT7pZE1c+ZungmFxQb2cByMxg15K6oQW/14nPDy6NwQKBgBV/MjToWllxBJm+9cHZuO82BBViKAUm+3x59pTsVbE+/kOOnlTKwBdG5mhV/+hNrLFSGcMeNxKjGo9YJS5UH55YqkVeKXqxJB31CJOAGbvTcbJuXATQnzhoD1Y0+TnTplo8CHcyjHGebT28i4zn9vuYY86F2d0iWJivy8MGeVkNAoGADUAug8jLk19hyejyvHK+nuQJ3gnbdSaUE3uTF5YbVxMhXuKq/Q8lkx74p8mc5x+NkzwrcpSL7YQ9Px4BopU9kvYHVChNVMVCnYRJ16MmEws2N9L4qdsmVKX8j0n+55DZsTPZfhPxP/Yuj6indAq7om+wbkuVTuPDhtDyHcfjHd8=')
isv_public_key = yop_security_utils.parse_rsa_pub_key(
    'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAoZ0QlV1I/sy4CcnrJDYX5W+xqOu3ZpDkqFwmCJJQGKXEQtftzG4eCbt0G9Mt1/dlz4q97ZPGl7q5LpPdzxYoOfNgUjyosQUgElyyxosAYit6cgbiaGmx7yAGbgBV2Az2l0CRNhwLawA2BnG1r7HXPeLpooUFOu1yJo4DogY9GYHiIbI3LAhBYJswMOMTVtXas2vIK83LwZpqsmFIoOckuSMsHIh7T2BvtBYi840/qOi6GjKGhfyAGKvBJGzwvCa2tyBar2bEfCq6+Q4qQrPOzUW90iC41Ak2cmmnijH+95tYK52Mj/QnAZcGkMnSsZzNLQ7t155vBSoiCveTs99VNQIDAQAB')


class Test(object):
    def test_envelope_self(self, client):
        if 'sm' == client.cert_type:
            return

        content = '{"orderId": "SP213142141", "status": "SUCCESS", "uniqueOrderNo": "", "parentMerchantNo": "10085864877", "merchantNo": "10085864877"}'

        encryptor = RsaEncryptor(
            clientConfig.get_credentials().get_priKey(),
            clientConfig.get_yop_public_key().get('default'))

        enc = encryptor.envelope_encrypt(content, isv_private_key, isv_public_key)
        print('enc:{}'.format(enc))

        plain = encryptor.envelope_decrypt(enc, isv_private_key, isv_public_key)
        print('plain:{}'.format(plain))

        assert plain == content

    def test_envelope_notify(self, client):
        if 'sm' == client.cert_type:
            return

        content = '{"date":"20181014000000","aaa":"","boolean":true,"SIZE":-14,"name":"易宝支付","dou":12.134}'
        response = 'EJSkBOwrHduycpFOvg9rJAoC_HE4_ZBLCiZJuvJGm2fgqr7TU9L56qjNkU3bWdZRwtQBMulMq6JokW4ZNglNIAYBysJrHHXF68BP1ohuFC5kfJXzvya4UXBdHFHgtT7vJUsvxUCOANwR36NOhK1kzmGiuLDiaXGtXquo5p-H9JDSIXY7ZcDf6P0WdZ8BG2_TR34sbTGDW73m-4vnw3lCPWGhxlgnW_6CxRVWpl-iXIfMBl52DcPCa9i1-HhLb1-_g8Rf6-Trm4ahMi-dNJok71XK-gNIYbJRNhdMfFfT2cC_tXjK76zfEu94LkHbFJZkflmlH6iVy6y3aPpJL49_cg$FBa72nweVtKsfXawN9BTR6AOEeSxWygcUyP_WKGvqKvVF6vOeAY7P4NYTTgojtnL9H4Pr6zmKbXgJI0GKHRjfSHoLTDf5z2qxIfD1Cd8f443PUpL7PCpPEduNSTuIx2Je5uhCtJ6Sdglp5pw8kRDNx2E2Mz0fgbBaCuatLtJmr62aiUQAlfDVoXbdcFv-5lES00KAP9S1nU8phBnQhJt2V76x-alH_rq13Pf3F_Xo6wZDAFhzrmlWVlh3jmbMDGwsBSWf1j0iIZpbsS3Vd4-UO6RO_52Hb1ZsMhZl3fMzzBIx1-Qc7w2pWlsVrYbymWGlNZukeir0RMT9I72VUqGVoMh9U5Qnw7DZssvwyjLPLjmx54vDHTxE3EXV70heccs0p5wI7gomeO8u-Szpx4CiBkeMUTtaXdtDmqrxnVnx6C4wVFSeXMSHn9RF35GrRZlOSSWVNKh1AMC57m0cJXk0NfTvl9eDkx5TmHBIrbrZ3Xfi_ZHILUjwc4A87KOeSwJW-C3OWnAN1QsDCgxZsaPdGh8O0y3Y6Wr1sEWUMV5nwH4eS_a2G6rZUswN3LJ6iro2lhLrcteIYK4QYzh8nRu5g$AES$SHA256'

        encryptor = RsaEncryptor(
            isv_private_key,
            clientConfig.get_yop_public_key().values()[0])

        plain = encryptor.envelope_decrypt(response)  # , isv_private_key, yop_public_key)
        print('plain:{}'.format(plain))

        assert plain == content
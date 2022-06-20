# -*- coding: utf-8 -*-

from sys import version_info as pyVersion
import yop_python_sdk.utils.yop_security_utils as yop_security_utils
from yop_python_sdk.client.yop_client_config import YopClientConfig
from yop_python_sdk.security.encryptor.rsaencryptor import RsaEncryptor
import sys

sys.path.append("./")

clientConfig = YopClientConfig(config_file='config/yop_sdk_config_rsa_qa.json')
# isv_private_key = clientConfig.get_credentials().get_priKey()

# yop_public_key = yop_security_utils.parse_pub_key()
isv_private_key = yop_security_utils.parse_rsa_pri_key(
    'MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQChnRCVXUj+zLgJyeskNhflb7Go67dmkOSoXCYIklAYpcRC1+3Mbh4Ju3Qb0y3X92XPir3tk8aXurkuk93PFig582BSPKixBSASXLLGiwBiK3pyBuJoabHvIAZuAFXYDPaXQJE2HAtrADYGcbWvsdc94umihQU67XImjgOiBj0ZgeIhsjcsCEFgmzAw4xNW1dqza8grzcvBmmqyYUig5yS5IywciHtPYG+0FiLzjT+o6LoaMoaF/IAYq8EkbPC8Jra3IFqvZsR8Krr5DipCs87NRb3SILjUCTZyaaeKMf73m1grnYyP9CcBlwaQydKxnM0tDu3Xnm8FKiIK95Oz31U1AgMBAAECggEAMhOr9sw/+QvQHuBdJwxH3UT9xLy9SF+vKmfbNR65CNocdSXZPlYEorld4d1OwDOdbXCtJzd5+rvV85PH0AoqjsJV30WCc8+Fv4rPrmuVw9V7DGgLsZTGmLTQqTcbYmWp5vYPyLdp5k7bbqW/SWCOtFNiV4RmOXsnusCYaZULS6KPXpjpnpt4shesK1SdVC2uCO7eUKf4aN8kKSaGA6rKK9aiBwuiwnqAc5Z0++HxnTu3zjbrfmUVchFCLPU31zXlfzFfZW5hUu7whUcj7914V8q5AkuEEoqpFxAcirsH0ZQE7xtPFez+00OZU42NtyqlieUSE8zYglxVRjZ9pa4GwQKBgQDkNYmzCISJXbAqcNJCY9Og/tMBaZNrYh3Z51eENxxARoVD3jj462hsZMLd+ZH6AuerT7xEHgd4QxtLDVzMpXF4wwlZydu8DrTr7KZPliHFTWPs1ntOnsCeWhFnIHcKVnay9YkiMT+WqTwpGXTkpo68oI+vu3EKY9DSPp+di0CeEQKBgQC1S2WREQHOGnzQL2vqPZA45BL0k6F/KPgb2gTF4sRTkOZr4mnb/vmTt1E+xRKwTBCzsnzk4x2DFgMtYr9ZODtg9egmfd7BdjFzXw7f+ACoDE4SHtl2YqHqbnt6qDAwY6Ahz+0hmjG/2xD4lK5h0yDDh2iwoQnAKdQnaam3ZsLw5QKBgQDSsot7/LVBjnqD9L5sBXbzAdMXTr6JOoGNGga3T5qJzZJk4tt/FvnGehFgmHeqeNwkUu3jhkYnRu4AEUpIt8dYU9piR/jUXE+2Mzwp5tcvLxC/LheSswfsLAQ9TsAZj1LwT7pZE1c+ZungmFxQb2cByMxg15K6oQW/14nPDy6NwQKBgBV/MjToWllxBJm+9cHZuO82BBViKAUm+3x59pTsVbE+/kOOnlTKwBdG5mhV/+hNrLFSGcMeNxKjGo9YJS5UH55YqkVeKXqxJB31CJOAGbvTcbJuXATQnzhoD1Y0+TnTplo8CHcyjHGebT28i4zn9vuYY86F2d0iWJivy8MGeVkNAoGADUAug8jLk19hyejyvHK+nuQJ3gnbdSaUE3uTF5YbVxMhXuKq/Q8lkx74p8mc5x+NkzwrcpSL7YQ9Px4BopU9kvYHVChNVMVCnYRJ16MmEws2N9L4qdsmVKX8j0n+55DZsTPZfhPxP/Yuj6indAq7om+wbkuVTuPDhtDyHcfjHd8='
)
isv_public_key = yop_security_utils.parse_rsa_pub_key(
    'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAoZ0QlV1I/sy4CcnrJDYX5W+xqOu3ZpDkqFwmCJJQGKXEQtftzG4eCbt0G9Mt1/dlz4q97ZPGl7q5LpPdzxYoOfNgUjyosQUgElyyxosAYit6cgbiaGmx7yAGbgBV2Az2l0CRNhwLawA2BnG1r7HXPeLpooUFOu1yJo4DogY9GYHiIbI3LAhBYJswMOMTVtXas2vIK83LwZpqsmFIoOckuSMsHIh7T2BvtBYi840/qOi6GjKGhfyAGKvBJGzwvCa2tyBar2bEfCq6+Q4qQrPOzUW90iC41Ak2cmmnijH+95tYK52Mj/QnAZcGkMnSsZzNLQ7t155vBSoiCveTs99VNQIDAQAB'
)


class Test(object):

    def test_envelope_self(self, client):
        """
        Encrypts and decrypts the given envelope.

        Args:
            self: write your description
            client: write your description
        """
        if 'sm' == client.cert_type or pyVersion.major == 2:
            # TODO python2 下面ECB pad有问题
            return

        content = '{"orderId": "SP213142141", "status": "SUCCESS", "uniqueOrderNo": "", "parentMerchantNo": "10085864877", "merchantNo": "10085864877"}'

        encryptor = RsaEncryptor(
            clientConfig.get_credentials().get_priKey(),
            clientConfig.get_yop_public_key().get('default'))

        enc = encryptor.envelope_encrypt(content, isv_private_key,
                                         isv_public_key)
        print('enc:{}'.format(enc))

        plain = encryptor.envelope_decrypt(enc, isv_private_key,
                                           isv_public_key)
        print('plain:{}'.format(plain))

        assert plain == content

    def test_envelope_notify_16(self, client):
        """
        Decrypt response with isv_private_key and yop_public_key

        Args:
            self: write your description
            client: write your description
        """
        if 'sm' == client.cert_type:
            return

        # 16/32 pad 一致的情况
        content = '{"date":"20181014000000","aaa":"","boolean":true,"SIZE":-14,"name":"易宝支付","dou":12.134}'
        response = 'EJSkBOwrHduycpFOvg9rJAoC_HE4_ZBLCiZJuvJGm2fgqr7TU9L56qjNkU3bWdZRwtQBMulMq6JokW4ZNglNIAYBysJrHHXF68BP1ohuFC5kfJXzvya4UXBdHFHgtT7vJUsvxUCOANwR36NOhK1kzmGiuLDiaXGtXquo5p-H9JDSIXY7ZcDf6P0WdZ8BG2_TR34sbTGDW73m-4vnw3lCPWGhxlgnW_6CxRVWpl-iXIfMBl52DcPCa9i1-HhLb1-_g8Rf6-Trm4ahMi-dNJok71XK-gNIYbJRNhdMfFfT2cC_tXjK76zfEu94LkHbFJZkflmlH6iVy6y3aPpJL49_cg$FBa72nweVtKsfXawN9BTR6AOEeSxWygcUyP_WKGvqKvVF6vOeAY7P4NYTTgojtnL9H4Pr6zmKbXgJI0GKHRjfSHoLTDf5z2qxIfD1Cd8f443PUpL7PCpPEduNSTuIx2Je5uhCtJ6Sdglp5pw8kRDNx2E2Mz0fgbBaCuatLtJmr62aiUQAlfDVoXbdcFv-5lES00KAP9S1nU8phBnQhJt2V76x-alH_rq13Pf3F_Xo6wZDAFhzrmlWVlh3jmbMDGwsBSWf1j0iIZpbsS3Vd4-UO6RO_52Hb1ZsMhZl3fMzzBIx1-Qc7w2pWlsVrYbymWGlNZukeir0RMT9I72VUqGVoMh9U5Qnw7DZssvwyjLPLjmx54vDHTxE3EXV70heccs0p5wI7gomeO8u-Szpx4CiBkeMUTtaXdtDmqrxnVnx6C4wVFSeXMSHn9RF35GrRZlOSSWVNKh1AMC57m0cJXk0NfTvl9eDkx5TmHBIrbrZ3Xfi_ZHILUjwc4A87KOeSwJW-C3OWnAN1QsDCgxZsaPdGh8O0y3Y6Wr1sEWUMV5nwH4eS_a2G6rZUswN3LJ6iro2lhLrcteIYK4QYzh8nRu5g$AES$SHA256'

        encryptor = RsaEncryptor(
            isv_private_key,
            list(clientConfig.get_yop_public_key().get('RSA2048').values())[0])

        # , isv_private_key, yop_public_key)
        plain = encryptor.envelope_decrypt(response)
        print('plain:{}'.format(plain))

        assert plain == content

    def test_envelope_notify_32(self, client):
        """
         16/32 pad  的 的 RsaEncrypt

        Args:
            self: write your description
            client: write your description
        """
        if 'sm' == client.cert_type:
            return

        # 16/32 pad 不一致的情况
        content = '{"date":"20181014000000","aaa":"","boolean":true,"SIZE":-14,"name":"易宝支付","dou":12.34}'
        response = 'AT320grqREB__reG5un3QbzBWQ0QfHzdHkHJW4_GmMzY4Qeg-ud_xLhCucVVxLGZQlKiJoH6BS26fVz47r49S6o_6OTUPMoxCdy-mqhPx0mF3LAvmQNV8v_bKingnMM--LiW6z8OE9i_e8-sJ2YrlmhI99AAVqpC-9Kdn_Mx1x0-i6ojv7TO0foUN3RjPomvX_43Vc2xJdJIWmYx18Z5aOrlz1Z8MiEXntx-W7cBI9veC9k3tb_Jkoc1QyyhyAU6za4sCjQq5InvhUUljN62dgHbEIiS8Jp3YOOy3bf0xy9eotKsybpGr63ZPpukdAYUGJVPfAqOXxMdokbxLGvSag$6DjZHtBf9YTJcPeQ6HmNEGSMuRMVRn1idDS18MweFPUrkCd-iBq06b6HDh0oG4ZSqW2ef_64MSOMKCnNWtFreuXpvVtlYikCZV7Tr_vYagaJ8tq3TGMlpZPuUGKmKSGpXS4V5zrzN9OTWUEQejqVoxQhPriKERXsl34ceS9Em_AHqPgWzeV5Cgfsn2it6SnOGMVTRNMB-G61m7J7rVjDlGLatMzGOPpjraj2iwTmkwFD7PQOhlHg4rPr17vdsJQOBvhAtGCrTp5pqLABRDOQefQCQ3P2z_BPg_GC3F44Osd_EzZ-PIXAha3ULFWM6g6iY8g88h0aCEZBrt0qmfjzDnl6seyuaeah6wC1hCVYmC6tWUfbW_2QIfkRMtxwGsfF7QXo2IplfkYbEdfIZoNejpBCA72RLKU6ApNiBSKQGvV4MT8IhbHlyMNjm4zCiAc5hvqy15z2pMM1CaKpKtU8jxq03H0sZvzr749dCPh5-O0BgoZST_D3eOlu7usjlKstxmIcBUYymbv0XgsNOEbzqzpQgc1-IkMdG_k17H33JXmi9Kxp1ezRjER9sqoG_oZEzjL7KP_PIFvUtAeJ5e4pdA$AES$SHA256'

        clientConfig = YopClientConfig(
            config_file='config/yop_sdk_config_rsa_prod.json')
        encryptor = RsaEncryptor(
            isv_private_key,
            list(clientConfig.get_yop_public_key().get('RSA2048').values())[0])

        # , isv_private_key, yop_public_key)
        plain = encryptor.envelope_decrypt(response)
        print('plain:{}'.format(plain))

        assert plain == content

    def test_envelope_notify_unpad(self, client):
        """
        Decrypts the response and verifies that it looks like an envelope with a public key.

        Args:
            self: write your description
            client: write your description
        """
        if 'sm' == client.cert_type:
            return

        content = '{"date":"20181014000000","aaa":"","boolean":true,"SIZE":-14,"name":"易宝支付","dou":12.134}'
        response = 'ftjjTgrMrdS3aovlxxRa1GQiEuh4VUw8UhfhtV1yahhfvmpoVpn56wjMSW_Hr5BcXFylw08oBxRkHw0QgltrNGuzcmoyXhcP3LJUYcypMjf24YVryOtxdaAqsuTdhcsb6nBpvPfWTPvQiQ0QNmB_cCZSqaHNlj7iq3MtGnO6e5xFZNs4aUc9C1NtWNZc-NMTJaKV9XYVUD0UTmRZeGio8kD7BkcNGMwmLv32FEUzqFFVKXURXRikFVWLZ_d0gw1k8ewvblJM_OFL7SZYMy8uPxFLKX8qGTWZhOdgnZX1T3Pzkf-C34yA8oVcUaSkCFMgsSt9SfK8y-mvOgamylNdow$oIQRJRwIeMNYBbI1EQKqlfly0KD1PV-oyN4IXkVl6iJ_xkjorLoLgykDcCtkVPJaPid-GIei1Px3uBE3TeGxxm06D1uzlGTpPgoaBB71dQ-efWGIJ2OLB7L25Y4IQlMXcQG11tR7GDGu7EvVI9SP52_mQxYqxh7dZBPz-Mqs11H3HqJSN7sJvh727ksRAuIv5TRI2EONoahvRENZ2diqC1sU0Tsl2FvDcKkkDU-e5O6jP8sYAbY0KBrCS_Cf40jay9MrM2knKHU6e0EvPRlkx9jqtzhUOpFS_wvbVdHRkKMFvGANhqa3rWdrMPOzKRiRRmLFUd5htoeYcdod002EJ_ltDRG-cueLXddKiJVCmWdOTGjY2OYQhVZ8N1-Y9eiRVsi0twKkPKHh0AnEPiR6KLhu0ds_pNWcheFox1N4KYqrRvObPc1AR5-4uzfIhOsaqiAmuBlMGX45LH9IvY0qwUun0oFHwtIt_PAyCQiCb47kaBf-zAbbPss0dEsGjGMZT1gO2TzBE1D6rBN3GHH_ye8WgefbGXgSZaKlvVy0mdoVNEtwyeJkFswpMNc7UlXT42yZkZIBLSziORZEFUmhrPNh5hIsxLxRR5-JKG0C8yiAjZNxjUkXCZ9UUSWwoVphrLJtyF2eee5RecMMyfYE8lO3jU47DF66Ol3c1WO2FWcIdgkHomhEMttDxsAn3kbrEwUCrfn8Bf4rvNv-R1j2aM9lkk30Amc7sMcjRTBXNfuuwCGtCNXRBONWqVclhIW8V2EuRFztPx3o7aby7zDMMrHhs3i-zT9tFQvwj2us3oxD_lM9hKCH2RVrNa-BCwxXqM7a6do5Yp-0vi0g_IvVkOBX0JFm9cAmix4Dx1yxa7SRukxOLT-EVefpLTsdXfrxZSSTxjdjk9jancfIeETmFyPsJdIJgETYLzrYF6SqOw-lyklsX1kM6_uxj0keKC3ZLkJXic5NhDM2yDQSsbD-Ru36FYyjqg5-VuUBKXubkEtUH4LYIlXQzrrDZ92wurlxrJnlVMrHpDI7Y1LQW1QXDVduETqo8A1-dlGDWmL1EWHiwI9fx0vWpaHe9j5ByilnxJli82LkstPjAA5Do5_my1adhD1UrljLv7BpISicU8MRHIt7t533nvKLLGvlCDLhHP15BI9lSerbL4NOaArJoQ$AES$SHA256'

        encryptor = RsaEncryptor(
            isv_private_key,
            list(
                clientConfig.get_yop_public_key().get(u'RSA2048').values())[0])

        try:
            # , isv_private_key, yop_public_key)
            plain = encryptor.envelope_decrypt(response)
            print('plain:{}'.format(plain))

            assert plain == content
        except Exception as e:
            assert repr(e).find(u'isv private key is illegal!') > 0

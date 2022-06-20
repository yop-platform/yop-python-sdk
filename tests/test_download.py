# -*- coding: utf-8 -*-

from yop_python_sdk.auth.v3signer.credentials import YopCredentials
import tests.assertion as assertion
import os
import sys

sys.path.append("./")


class Test(object):

    def test_download(self, client):
        """
        Test download functionality.

        Args:
            self: write your description
            client: write your description
        """
        if 'sm' == client.cert_type:
            return

        api = '/yos/v1.0/balance/yop-simple-remit/download-electronic-receipt'
        params = {
            'batchNo': '000000005499580',
            'orderId': 'YB654db6376fd04045a6abd82f055f6e04',
        }
        credentials = YopCredentials(
            appKey='OPR:10012413438',
            cert_type='RSA2048',
            priKey=
            'MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCcKXb/SKitY30pWKON9ra84xcgiRu8kN4z+jvxqyyKpIx6gnNLQE4+6wp5C9LviF3o7rqPFXDSifHLz94AVVKCT7a2mvx7lGk+y56p3GJzrvahjyxbaBMRyDI76tdOvl1T1qFRWFv4OXagDawUcUCKSrxlRej7uALSdeyKaoKnqC0eR2fpuFNbz6NxIqRREIUZiSqmehjUPgBidJuOPJ1/HGkzZhmWBB46QxvermojqoxHEsLi0NakfX/rW3GQC1I1KY58e9ukTnZ2lo8j8gZrbPuY/1WM2Q3pzPGd5OPdtcZGtaHKIrzHupf+Et6EDU8IbZFIDJ/1qQ0JXYpBODVNAgMBAAECggEAOY40zBkhBirNdiAzw76DEnIWU4kFHoY8R2b6kfM3avAD0KFk0f7k996UERIRD/SwPApE2ziZSRfLdQVreq73xoyPuJS96uRDt/+/Pja6WI3LW7dTr2rX4G1rSlcfPOf/qMdJ1Jve5cl0FcCERFKLaYzrC95s5N2ouJ367PcdqaHIHsOUetqHoOH6Z9VCmpHPpX/+RfdXkFS1XfenAPW1x90e1u9e7jWbPfYVhwzjegYyp1KzJsPavs3BwQvu2J4tFq7THKtjA31BelX133kuv3oFeq2J5dFnFfpe3s/p9HtHRGLSKt9Sf/Zy13uFw4kjZCwGnVFZr68LaifPsyJMpwKBgQC6D1yjPNfb7QMLBQZlWEx0ATqYLXbUes6ZdM88Qd/nd1HrweLtAdptofHVXdE4FKIQ75yt7pKKYj0sURhzhM13wchwjXUhBzZYUjOQ9YcUd1f9eaMheZoE149P+pwKB3Yck/hBIJk6W20fMr6vucroA4vbvnvaAmwrR3nNdRKX8wKBgQDW3QBoXnALNTC0iAe5B8z49CYcFqyGFDwtflXulSvRYlxpl4mRAOA+P2oQtaaElZre8LSlC6e93J4VxfvLDeVzFer+g8JuQNJDhvPsoYmT29s+A1kqicE6SU+KAFoMoubuHAClM0elle202IJqdWt/pt/Yl+Z44MBvFzsrvLiNvwKBgQCJIql053Nydc64YIvGRr6TAhTd9SSQl7OPB7l3AFa3lAqdadqINcV46NQGH5AFda++K92flSgNNzs/XsZW3ptSmVHTI3AhV9+GWZAIV++n9g60lOLX2Xjb+MV4fY5lFfrINYfU+OH3UUusowpJGvei6no7DLrchMyVWak89f0uYQKBgHNXTfm5AHKzygKPp32nd1wJTE/1yAVt5WQSlrSttUkAgVVZuMpzau1fg2OW793qpamaE48p85ETVnWfw2wceJjQIkcgmgYvm/AOCPF1QfJyqn3etEYGjwjoA9+0EqMH6+nUdHA6V/LGykUzmMbnY56yCSYvXNR06jh4gxYWiAfnAoGAXh30ObSnOrf3befSF6qAHtEWBAf3oAXnpVKdqNaAy+Py/myJ6fvjENY3ZfzROkZqu5BSyuqiUw+V50WFM6hDgbEXJoRXdm41M9S8JwFBl5qAe1e3BZdbxbUK7G/qM4PQuTaArkvuz0wbJiZ2soFzi6S2ktDraafk+ErRgJx+q1k='
        )
        file_path = os.environ['HOME']
        res = client.download(api, params, credentials, file_path=file_path)
        assertion.failure(res, '40047')
        # assert 0 == res

    def test_download_with_credentials(self, client):
        """
        Test downloading with credentials.

        Args:
            self: write your description
            client: write your description
        """
        if 'sm' == client.cert_type:
            return

        api = '/yos/v1.0/balance/yop-simple-remit/download-electronic-receipt'
        params = {
            'batchNo': '000000005499580',
            'orderId': 'YB654db6376fd04045a6abd82f055f6e04',
        }
        credentials = YopCredentials(
            appKey='OPR:10012413438',
            cert_type='RSA2048',
            priKey=
            'MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCcKXb/SKitY30pWKON9ra84xcgiRu8kN4z+jvxqyyKpIx6gnNLQE4+6wp5C9LviF3o7rqPFXDSifHLz94AVVKCT7a2mvx7lGk+y56p3GJzrvahjyxbaBMRyDI76tdOvl1T1qFRWFv4OXagDawUcUCKSrxlRej7uALSdeyKaoKnqC0eR2fpuFNbz6NxIqRREIUZiSqmehjUPgBidJuOPJ1/HGkzZhmWBB46QxvermojqoxHEsLi0NakfX/rW3GQC1I1KY58e9ukTnZ2lo8j8gZrbPuY/1WM2Q3pzPGd5OPdtcZGtaHKIrzHupf+Et6EDU8IbZFIDJ/1qQ0JXYpBODVNAgMBAAECggEAOY40zBkhBirNdiAzw76DEnIWU4kFHoY8R2b6kfM3avAD0KFk0f7k996UERIRD/SwPApE2ziZSRfLdQVreq73xoyPuJS96uRDt/+/Pja6WI3LW7dTr2rX4G1rSlcfPOf/qMdJ1Jve5cl0FcCERFKLaYzrC95s5N2ouJ367PcdqaHIHsOUetqHoOH6Z9VCmpHPpX/+RfdXkFS1XfenAPW1x90e1u9e7jWbPfYVhwzjegYyp1KzJsPavs3BwQvu2J4tFq7THKtjA31BelX133kuv3oFeq2J5dFnFfpe3s/p9HtHRGLSKt9Sf/Zy13uFw4kjZCwGnVFZr68LaifPsyJMpwKBgQC6D1yjPNfb7QMLBQZlWEx0ATqYLXbUes6ZdM88Qd/nd1HrweLtAdptofHVXdE4FKIQ75yt7pKKYj0sURhzhM13wchwjXUhBzZYUjOQ9YcUd1f9eaMheZoE149P+pwKB3Yck/hBIJk6W20fMr6vucroA4vbvnvaAmwrR3nNdRKX8wKBgQDW3QBoXnALNTC0iAe5B8z49CYcFqyGFDwtflXulSvRYlxpl4mRAOA+P2oQtaaElZre8LSlC6e93J4VxfvLDeVzFer+g8JuQNJDhvPsoYmT29s+A1kqicE6SU+KAFoMoubuHAClM0elle202IJqdWt/pt/Yl+Z44MBvFzsrvLiNvwKBgQCJIql053Nydc64YIvGRr6TAhTd9SSQl7OPB7l3AFa3lAqdadqINcV46NQGH5AFda++K92flSgNNzs/XsZW3ptSmVHTI3AhV9+GWZAIV++n9g60lOLX2Xjb+MV4fY5lFfrINYfU+OH3UUusowpJGvei6no7DLrchMyVWak89f0uYQKBgHNXTfm5AHKzygKPp32nd1wJTE/1yAVt5WQSlrSttUkAgVVZuMpzau1fg2OW793qpamaE48p85ETVnWfw2wceJjQIkcgmgYvm/AOCPF1QfJyqn3etEYGjwjoA9+0EqMH6+nUdHA6V/LGykUzmMbnY56yCSYvXNR06jh4gxYWiAfnAoGAXh30ObSnOrf3befSF6qAHtEWBAf3oAXnpVKdqNaAy+Py/myJ6fvjENY3ZfzROkZqu5BSyuqiUw+V50WFM6hDgbEXJoRXdm41M9S8JwFBl5qAe1e3BZdbxbUK7G/qM4PQuTaArkvuz0wbJiZ2soFzi6S2ktDraafk+ErRgJx+q1k='
        )
        file_path = os.environ['HOME']
        res = client.download(api, params, credentials, file_path=file_path)
        assertion.failure(res, '40047')
        # assert 0 == res

    def test_download_failed(self, client):
        """
        Test that downloading a file fails.

        Args:
            self: write your description
            client: write your description
        """
        if 'sm' == client.cert_type:
            return

        api = '/yos/v1.0/balance/yop-simple-remit/download-electronic-receipt'
        params = {
            'batchNo': '000000005499580',
            'orderId': 'YB654db6376fd04045a6abd82f055f6e042',
        }
        credentials = YopCredentials(
            appKey='OPR:10012413438',
            cert_type='RSA2048',
            priKey=
            'MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCcKXb/SKitY30pWKON9ra84xcgiRu8kN4z+jvxqyyKpIx6gnNLQE4+6wp5C9LviF3o7rqPFXDSifHLz94AVVKCT7a2mvx7lGk+y56p3GJzrvahjyxbaBMRyDI76tdOvl1T1qFRWFv4OXagDawUcUCKSrxlRej7uALSdeyKaoKnqC0eR2fpuFNbz6NxIqRREIUZiSqmehjUPgBidJuOPJ1/HGkzZhmWBB46QxvermojqoxHEsLi0NakfX/rW3GQC1I1KY58e9ukTnZ2lo8j8gZrbPuY/1WM2Q3pzPGd5OPdtcZGtaHKIrzHupf+Et6EDU8IbZFIDJ/1qQ0JXYpBODVNAgMBAAECggEAOY40zBkhBirNdiAzw76DEnIWU4kFHoY8R2b6kfM3avAD0KFk0f7k996UERIRD/SwPApE2ziZSRfLdQVreq73xoyPuJS96uRDt/+/Pja6WI3LW7dTr2rX4G1rSlcfPOf/qMdJ1Jve5cl0FcCERFKLaYzrC95s5N2ouJ367PcdqaHIHsOUetqHoOH6Z9VCmpHPpX/+RfdXkFS1XfenAPW1x90e1u9e7jWbPfYVhwzjegYyp1KzJsPavs3BwQvu2J4tFq7THKtjA31BelX133kuv3oFeq2J5dFnFfpe3s/p9HtHRGLSKt9Sf/Zy13uFw4kjZCwGnVFZr68LaifPsyJMpwKBgQC6D1yjPNfb7QMLBQZlWEx0ATqYLXbUes6ZdM88Qd/nd1HrweLtAdptofHVXdE4FKIQ75yt7pKKYj0sURhzhM13wchwjXUhBzZYUjOQ9YcUd1f9eaMheZoE149P+pwKB3Yck/hBIJk6W20fMr6vucroA4vbvnvaAmwrR3nNdRKX8wKBgQDW3QBoXnALNTC0iAe5B8z49CYcFqyGFDwtflXulSvRYlxpl4mRAOA+P2oQtaaElZre8LSlC6e93J4VxfvLDeVzFer+g8JuQNJDhvPsoYmT29s+A1kqicE6SU+KAFoMoubuHAClM0elle202IJqdWt/pt/Yl+Z44MBvFzsrvLiNvwKBgQCJIql053Nydc64YIvGRr6TAhTd9SSQl7OPB7l3AFa3lAqdadqINcV46NQGH5AFda++K92flSgNNzs/XsZW3ptSmVHTI3AhV9+GWZAIV++n9g60lOLX2Xjb+MV4fY5lFfrINYfU+OH3UUusowpJGvei6no7DLrchMyVWak89f0uYQKBgHNXTfm5AHKzygKPp32nd1wJTE/1yAVt5WQSlrSttUkAgVVZuMpzau1fg2OW793qpamaE48p85ETVnWfw2wceJjQIkcgmgYvm/AOCPF1QfJyqn3etEYGjwjoA9+0EqMH6+nUdHA6V/LGykUzmMbnY56yCSYvXNR06jh4gxYWiAfnAoGAXh30ObSnOrf3befSF6qAHtEWBAf3oAXnpVKdqNaAy+Py/myJ6fvjENY3ZfzROkZqu5BSyuqiUw+V50WFM6hDgbEXJoRXdm41M9S8JwFBl5qAe1e3BZdbxbUK7G/qM4PQuTaArkvuz0wbJiZ2soFzi6S2ktDraafk+ErRgJx+q1k='
        )
        file_path = os.environ['HOME']
        res = client.download(api, params, credentials, file_path=file_path)
        assertion.failure(res, '40047')
        # assertion.failure(res, 'isp.code.data-not-fund', 'subCode')

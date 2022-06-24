import os
import json
import time
from urllib.parse import quote
from client.yop_client_config import YopClientConfig

from auth.v3signer.credentials import YopCredentials
from client.yopclient import YopClient

# 请修改为自己的商编
DEFAULT_YOP_MCH_NO = "10087090001"

PAY_URL = "https://cash.yeepay.com/cashier/std"


class YopCashierUtil(object):

    def __init__(self, mch_no=DEFAULT_YOP_MCH_NO):
        """_summary_

        Args:
            mch_no (_type_, optional): 商编. Defaults to YOP_MCH_NO.
        """
        src_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        config_path = os.path.join(src_path,
                                   "config/yop_sdk_config_rsa_qa.json")
        self.client = YopClient(YopClientConfig(config_path))
        self.mch_no = mch_no

    def direct_pay(self, send_data, notify_url=None):
        """_summary_

        Args:
            send_data (_type_): 支付参数
            notify_url (_type_, optional): 支付结果的回调地址. Defaults to None.

        Returns:
            _type_: 支付结果
        """
        api = '/rest/v1.0/std/trade/order'
        product = {
            "goodsName": send_data['subject'],
            "goodsDesc": send_data['subject_desc']
        }
        params = {
            'parentMerchantNo': self.mch_no,
            'merchantNo': self.mch_no,
            'orderId': send_data['order_sn'],
            'orderAmount': send_data['pay_amount'],
            'notifyUrl': notify_url,
            'goodsParamExt': json.dump(product),
            'timeoutExpress': send_data['expire_second'],
            'timeoutExpressType': 'SECOND',
            'redirectUrl': send_data['front_url'],
            'assureType': 'REALTIME',
            'fundProcessType': 'REAL_TIME',
            'assurePeriod': '30',
            'queryParamsExt': 'queryParamsExt_example'
        }
        res = self.client.get(api=api, params=params)
        return res

    def generate_url_str(self, token, userid):
        """构造支付链接

        Args:
            token (_type_): token
            userid (_type_): 用户编号

        Returns:
            _type_: 支付链接
        """
        params = {
            "appKey": self.appKey,
            "merchantNo": self.mch_no,
            "token": token,
            "timestamp": time.time(),
            "directPayType": "CTL",
            "cardType": "",
            "userNo": str(userid),
            "userType": "USER_ID",
            "ext": ""
        }
        unsigned_string = self.get_query_str(params)
        sign = self.credentials.encryptor.signature(unsigned_string)
        url = PAY_URL + "?" + unsigned_string + "&sign=" + sign
        return url

    def get_query_str(self, items, t1='=', t2='&'):
        """构造待签名的支付参数字符串

        Args:
            items (_type_): 键值对
            t1 (str, optional): 键值之间的间隔符. Defaults to '='.
            t2 (str, optional): 键值对之间的间隔符. Defaults to '&'.

        Returns:
            _type_: 待签名的支付参数字符串
        """
        lt = []
        sorted_items = sorted(items)
        self.logger.debug("sorted_items:{}".format(sorted_items))
        for k, v in sorted_items:
            if isinstance(v, tuple):
                continue
            elif isinstance(v, list):
                sorted_sub_items = sorted(v)
                for sub_v in sorted_sub_items:
                    lt.append(k + t1 + quote(str(sub_v), 'utf-8'))
            else:
                lt.append(k + t1 + quote(str(v), 'utf-8'))
        return t2.join(lt)

    def verify_sand_data(self, verify_data, verify_sign):
        verify_data = verify_data.encode("utf-8")
        return False, str("error")

    def query_order_yop(self):
        return False, str("error")


if __name__ == "__main__":
    sand_data = {
        #user_id, order_sn, pay_amount:decimal, subject, subject_desc, front_url
        'user_id': "1",
        'order_sn': "RD202208100000101",
        'pay_amount': "0.01",
        'subject': '潮流商品',
        'subject_desc': '潮流商品',
        'front_url': 'https://trade.me/sand/result?type=2',
    }
    ada_pay = YopCashierUtil()
    ada_pay.direct_pay(sand_data)

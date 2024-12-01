import hmac
import hashlib
import time

import requests

from conf import api_key as apikey, api_secret as apisecret


class Q :
    def __init__(self, api_key , api_secret):
        self.api_key = api_key
        self.secret = api_secret

    def timestamp(self):
        timestamp = str(int(time.time() * 1000))
        return timestamp

    def bapi_sign(self, params, recv_window):
        message = f"{self.timestamp()}{self.api_key}{recv_window}{params}"
        signature = hmac.new(self.secret.encode("utf-8"), message.encode("utf-8"), hashlib.sha256).hexdigest()
        return signature

    def get_balance(self,account_type,coin,recv_window="5000"):
        params = f"accountType={account_type}&coin={coin}"
        url = f"https://api.bybit.com/v5/account/wallet-balance?{params}"

        headers = {
            'X-BAPI-API-KEY': self.api_key,
            'X-BAPI-TIMESTAMP': self.timestamp(),
            'X-BAPI-RECV-WINDOW': recv_window,
            'X-BAPI-SIGN': self.bapi_sign(params,recv_window)
        }

        response = requests.get(url, headers=headers)
        return response


q = Q(apikey, apisecret)

print(q.get_balance("UNIFIED","BTC").json())


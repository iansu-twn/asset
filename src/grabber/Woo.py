import argparse
import configparser
import datetime
import hashlib
import hmac
import logging

import pandas as pd
import requests


class Woo:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://api.woo.org"

    def _generate_signature(self, data):
        key = self.api_secret
        key_bytes = bytes(key, "utf-8")
        data_bytes = bytes(data, "utf-8")
        return hmac.new(key_bytes, data_bytes, hashlib.sha256).hexdigest()

    def _generate_headers(self, method, endpoint):
        timestamp = str(round(datetime.datetime.now().timestamp() * 1000))
        return {
            "x-api-timestamp": timestamp,
            "x-api-key": self.api_key,
            "x-api-signature": self._generate_signature(
                f"{timestamp}{method}{endpoint}"
            ),
            "Content-Type": "application/json",
        }

    def getBalance(self):
        method = "GET"
        endpoint = "/v3/balances"
        res = requests.request(
            method,
            self.base_url + "/v3/balances",
            headers=self._generate_headers(method, endpoint),
        )
        data = res.json().get("data").get("holding")
        rows = []
        for row in data:
            holding = row["holding"] + row["staked"]
            dt = {
                "token": row["token"],
                "holding": holding,
                "price": row["markPrice"],
                "usdt_value": round(holding * row["markPrice"], 3),
            }
            rows.append(dt)
        df = pd.DataFrame(rows)
        return df


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO
    )
    exchange = "WOO"
    parser = argparse.ArgumentParser(exchange)
    args = parser.parse_args()
    cfg = configparser.ConfigParser()
    cfg.read("./config/info.ini")
    info = {}
    for option in cfg.options(exchange):
        info[option] = cfg.get(exchange, option)
    api_key = info.get("api_key")
    api_secret = info.get("api_secret")
    client = Woo(api_key, api_secret)
    df = client.getBalance()
    print(f"Asset on WOOX: {df.usdt_value.sum()}")

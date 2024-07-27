import argparse
import datetime
import hashlib
import hmac
import logging

import pandas as pd
import requests
from Asset import Asset


class Woox(Asset):
    def __init__(self, exchange):
        super().__init__(exchange)

    def _generate_signature(self, data):
        return hmac.new(
            self.api_secret.encode("utf-8"),
            data.encode("utf-8"),
            hashlib.sha256,  # noqa:E501
        ).hexdigest()

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

    def info(self):
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
        # return df # write into db later
        return round(df.usdt_value.sum(), 3)


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO
    )
    exchange = "WOOX"
    parser = argparse.ArgumentParser(exchange)
    args = parser.parse_args()
    client = Woox(exchange)
    asset = client.info()
    print(f"Asset on {exchange}: {asset}")

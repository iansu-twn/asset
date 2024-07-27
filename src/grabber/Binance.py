import argparse
import datetime
import hashlib
import hmac
import logging

import pandas as pd
import requests
from Asset import Asset


class Binance(Asset):
    def __init__(self, exchange):
        super().__init__(exchange)

    def _request(self, method, endpoint, params=None, signature=True):
        if params is None:
            params = {}
        query_string = self._generate_signature(params)
        if signature:
            url = f"{self.base_url}{endpoint}?{query_string}"
        else:
            url = f"{self.base_url}{endpoint}"
        res = requests.request(method, url, headers=self._generate_headers())
        if res.status_code == 200:
            return res.json()
        else:
            logging.error(f"Error: {res.raise_for_status()}")

    def _generate_headers(self):
        return {
            "X-MBX-APIKEY": self.api_key,
            "Content-Type": "application/josn",
        }  # noqa:E501

    def _generate_signature(self, params):
        params["timestamp"] = round(
            datetime.datetime.now().timestamp() * 1000
        )  # noqa:E501
        query_string = "&".join(
            [f"{key}={value}" for key, value in params.items()]
        )  # noqa:E501
        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        return query_string + f"&signature={signature}"

    def getSpotHolding(self):
        endpoint = "/api/v3/account"
        res = self._request("GET", endpoint)
        if res:
            data = res.get("balances")
            rows = []
            for row in data:
                balances = float(row["free"]) + float(row["locked"])
                if balances > 0:
                    dt = {"ccy": row["asset"], "balance": balances}
                    rows.append(dt)
            df = pd.DataFrame(rows)
        return df

    def getSimpleEarn(self):
        endpoint = "/sapi/v1/simple-earn/account"
        res = self._request("GET", endpoint)
        return res

    def getMarginHolding(self):
        endpoint = "/sapi/v1/margin/account"
        res = self._request("GET", endpoint)
        if res:
            data = res.get("userAssets")
            rows = []
            for row in data:
                if float(row["netAsset"]) > 0:
                    dt = {
                        "ccy": row["asset"],
                        "balance": float(row["netAsset"]),
                    }  # noqa:E501
                    rows.append(dt)
            df = pd.DataFrame(rows)
        return df

    def getPrice(self):
        endpoint = "/api/v3/ticker/price"
        res = self._request("GET", endpoint, signature=False)
        price = pd.DataFrame(res)
        price["price"] = price["price"].astype("float")
        return price

    def info(self):
        price = self.getPrice()
        spot_holding = self.getSpotHolding()
        margin_holding = self.getMarginHolding()

        df = pd.concat([spot_holding, margin_holding])
        df["ccy"] = df["ccy"].str.lstrip("LD")
        df["symbol"] = df["ccy"] + "USDT"
        df = df.groupby(["ccy"]).sum().reset_index()
        asset = df.merge(price, how="inner", on=["symbol"])
        asset["usdt_value"] = round(asset["balance"] * asset["price"], 3)
        # return asset.drop(["symbol"], axis=1) # write into db later
        return round(asset.usdt_value.sum(), 3)


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s:%(message)s", level=logging.INFO
    )
    exchange = "BINANCE"
    parser = argparse.ArgumentParser(exchange)
    args = parser.parse_args()
    client = Binance(exchange)
    asset = client.info()
    print(f"Asset on {exchange}: {asset}")

import argparse
import configparser
import logging


class Binance:
    def __init__(self, api_key, api_secret):
        self.base_url = "https://api.binance.com"
        self.api_key = api_key
        self.api_secret = api_secret


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s:%(message)s", level=logging.INFO
    )
    exchange = "BINANCE"
    parser = argparse.ArgumentParser(exchange)
    args = parser.parse_args()
    cfg = configparser.ConfigParser()
    cfg.read("./config/info.ini")
    info = {}
    for option in cfg.options(exchange):
        info[option] = cfg.get(exchange, option)
    api_key = info.get("api_key")
    api_secret = info.get("api_secret")
    client = Binance(api_key, api_secret)

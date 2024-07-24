import argparse
import configparser
import logging


class Woo:
    def __init__(self):
        self.base_url = "https://api.woo.org"


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
    client = Woo()

import argparse
import configparser
import logging

from selenium import webdriver


class Taishin:
    def __init__(self, id, uid, pwd):
        self.driver = webdriver.Chrome()
        self.id = id
        self.uid = uid
        self.pwd = pwd


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO
    )
    exchange = "TAISHIN"
    parser = argparse.ArgumentParser(exchange)
    args = parser.parse_args()
    cfg = configparser.ConfigParser()
    cfg.read("./config/info.ini")
    info = {}
    for option in cfg.options(exchange):
        info[option] = cfg.get(exchange, option)
    id = info.get("id")
    uid = info.get("uid")
    pwd = info.get("pwd")
    client = Taishin(id, uid, pwd)

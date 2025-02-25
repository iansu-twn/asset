import configparser
import importlib
import logging
import os
import sys

import requests
import telebot

exchange_list = [
    "Ipost",
    "Ctbc",
    "Cathy",
    "Taishin",
    "Woox",
    "Firstrade",
    "FF",
    "Allianz",
    # "Binance",
]  # noqa:E501

hardcoded_asset = {
    "FF": 18400,
    "Allianz": 800000,
}


class Main:
    def __init__(
        self,
        item="TELEGRAM",
        config_path="./asset/src/grabber/config/info.ini",  # noqa:E501
    ):
        # get token and chat id
        info = self._getInfo(item, config_path)
        for key, value in info.items():
            setattr(self, key, value)

        self.bot = telebot.TeleBot(self.token)

    def _getInfo(self, item, config_path):
        cfg = configparser.ConfigParser()
        cfg.read(config_path)
        info = {}
        for option in cfg.options(item):
            info[option] = cfg.get(item, option)
        return info

    def getAsset(self):
        total_asset = 0
        msg = []
        for exchange_name in exchange_list:
            if exchange_name in ["FF", "Allianz"]:
                asset = hardcoded_asset.get(exchange_name)
                msg.append(f"Asset on {exchange_name.upper()}: {asset}")
                total_asset += (
                    asset * self._getExchangeRate()
                    if exchange_name == "FF"
                    else float(asset)
                )
            else:
                module = importlib.import_module(f"grabber.{exchange_name}")
                exchange_class = getattr(module, exchange_name)
                exchange_instance = exchange_class(exchange_name.upper())

                if hasattr(exchange_instance, "login"):
                    exchange_instance.login()

                if hasattr(exchange_instance, "info"):
                    if exchange_name == "Cathy":
                        asset = 0
                        for idx in ["cash", "stock"]:
                            assets = exchange_instance.info(idx)
                            msg.append(
                                f"Asset on {exchange_name.upper()}_{idx.upper()}: {assets}"  # noqa:E501
                            )
                            asset += assets
                    else:
                        asset = exchange_instance.info()
                        msg.append(
                            f"Asset on {exchange_name.upper()}: {asset}"
                        )  # noqa:E501

                if hasattr(exchange_instance, "logout"):
                    exchange_instance.logout()

                total_asset += (
                    asset * self._getExchangeRate()
                    if exchange_name in ["Binance", "Firstrade", "Woox"]
                    else float(asset)
                )
        msg.append(f"Total Asset: {round(total_asset, 3)}")
        messages = "\n".join(msg)
        self.bot.send_message(self.chat_id, messages)
        logging.info("Message sent!")

    def _getExchangeRate(self):
        res = requests.get("https://tw.rter.info/capi.php")
        currency = res.json()
        return currency.get("USDTWD").get("Exrate")


if __name__ == "__main__":
    sys.path.append(os.path.join(os.path.dirname(__file__), "grabber"))
    logging.basicConfig(
        format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO
    )  # noqa:E501
    client = Main()
    client.getAsset()

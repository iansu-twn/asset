import configparser
import importlib
import logging
import os
import sys

import telebot

exchange_list = [
    "Firstrade",
    # "Binance",
    "Cathy",
    "Ctbc",
    "Ipost",
    "Taishin",
    "Woox",
]  # noqa:E501


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
            module = importlib.import_module(f"grabber.{exchange_name}")
            exchange_class = getattr(module, exchange_name)
            exchange_instance = exchange_class(exchange_name.upper())

            if hasattr(exchange_instance, "login"):
                exchange_instance.login()

            if hasattr(exchange_instance, "info"):
                asset = exchange_instance.info()
                msg.append(f"Asset on {exchange_name.upper()}: {asset}")

            if hasattr(exchange_instance, "logout"):
                exchange_instance.logout()

            total_asset += (
                asset * 32
                if exchange_name in ["Binance", "Firstrade", "Woox"]
                else float(asset)
            )
        msg.append(f"Total Asset: {round(total_asset, 3)}")
        messages = "\n".join(msg)
        self.bot.send_message(self.chat_id, messages)
        logging.info("Message sent!")


if __name__ == "__main__":
    sys.path.append(os.path.join(os.path.dirname(__file__), "grabber"))
    logging.basicConfig(
        format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO
    )  # noqa:E501
    client = Main()
    client.getAsset()

import importlib
import logging
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "grabber"))
logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO
)  # noqa:E501

exchange_list = [
    "Firstrade",
    "Binance",
    "Cathy",
    "Ctbc",
    "Ipost",
    "Taishin",
    "Woox",
]  # noqa:E501

total_asset = 0
for exchange_name in exchange_list:
    module = importlib.import_module(f"grabber.{exchange_name}")
    exchange_class = getattr(module, exchange_name)
    exchange_instance = exchange_class(exchange_name.upper())

    if hasattr(exchange_instance, "login"):
        exchange_instance.login()

    if hasattr(exchange_instance, "info"):
        asset = exchange_instance.info()
        logging.info(f"Asset on {exchange_name.upper()}: {asset}")

    if hasattr(exchange_instance, "logout"):
        exchange_instance.logout()

    total_asset += (
        asset * 32
        if exchange_name in ["Binance", "Firstrade", "Woox"]
        else float(asset)
    )
logging.info(f"Total Asset: {round(total_asset, 3)}")

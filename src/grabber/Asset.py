import configparser
import logging

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Asset:
    def __init__(self, exchange, config_path="./config/info.ini"):
        self.exchange = exchange
        info = self._getInfo(self.exchange, config_path)
        for key, value in info.items():
            setattr(self, key, value)

        # configure chrome options
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-blink-features")
        self.driver = webdriver.Chrome(options=options)

    def _getInfo(self, exchange, config_path):
        cfg = configparser.ConfigParser()
        try:
            cfg.read(config_path)
            if exchange not in cfg.sections():
                logging.error(f"Configuration section {exchange} not found")
            info = {}
            for option in cfg.options(exchange):
                info[option] = cfg.get(exchange, option)
            return info
        except Exception as e:
            logging.error(f"Error reading configuration: {e}")

    def _close_driver(self):
        self.driver.close()
        logging.info(f"{self.exchange} LOGOUT SUCCESSFUL")

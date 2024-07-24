import argparse
import configparser
import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Ctbc:
    def __init__(self, id, uid, pwd):
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")  # Run in headless mode
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-blink-features")
        self.driver = webdriver.Chrome(options=options)
        self.id = id
        self.uid = uid
        self.pwd = pwd

    def login(self, url):
        self.driver.get(url)
        id = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "/html/body/app/div[1]/div[2]/twrbc-general-ot001-010/div/div[2]/div[3]/div[1]/div/nav-tabs/div/div[1]/div[2]/form/div/div[1]/div/input",  # noqa:E501
                )
            )
        )
        id.send_keys(self.id)

        uid = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "/html/body/app/div[1]/div[2]/twrbc-general-ot001-010/div/div[2]/div[3]/div[1]/div/nav-tabs/div/div[1]/div[2]/form/div/div[2]/div/input",  # noqa:E501
                )
            )
        )
        uid.send_keys(self.uid)

        pwd = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "/html/body/app/div[1]/div[2]/twrbc-general-ot001-010/div/div[2]/div[3]/div[1]/div/nav-tabs/div/div[1]/div[2]/form/div/div[3]/div/input",  # noqa:E501
                )
            )
        )
        pwd.send_keys(self.pwd)

        btn_login = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "/html/body/app/div[1]/div[2]/twrbc-general-ot001-010/div/div[2]/div[3]/div[1]/div/nav-tabs/div/div[1]/div[2]/div[1]/a[1]",  # noqa:E501
                )
            )
        )
        btn_login.click()
        logging.info("LOGIN SUCCESSFUL")


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO
    )
    exchange = "CTBC"
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
    url = "https://www.ctbcbank.com/twrbc/twrbc-general/ot001/010"
    client = Ctbc(id, uid, pwd)
    client.login(url)

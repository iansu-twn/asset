import argparse
import configparser
import logging

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Cathy:
    def __init__(self, id, uid, pwd):
        self.driver = webdriver.Chrome()
        self.id = id
        self.uid = uid
        self.pwd = pwd

    def login(self, url):
        self.driver.get(url)
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//*[@id='divSystemLoginMsg']/div/div/div[2]/div[2]/button",  # noqa:E501
                    )
                )
            ).click()
        except TimeoutException:
            pass

        id = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='CustID']"))
        )
        id.send_keys(self.id)

        uid = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[@id='UserIdKeyin']")
            )  # noqa:E501
        )
        uid.send_keys(self.uid)

        pwd = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[@id='PasswordKeyin']")
            )  # noqa:E501
        )
        pwd.send_keys(self.pwd)

        btn_login = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[@id='divCUBNormalLogin']/div[2]/button")
            )
        )
        btn_login.click()
        logging.info("LOGIN SUCCESSFUL")

    def info(self):
        info = (
            WebDriverWait(self.driver, 10)
            .until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//*[@id='TD-balance']")
                )  # noqa:E501
            )
            .text
        )
        cash = float(info.strip().replace(",", ""))
        return cash

    def logout(self):
        btn_logout = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='m-nav-logout']"))
        )
        btn_logout.click()
        self.driver.close()
        logging.info("LOGOUT SUCCESSFUL")


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO
    )
    exchange = "CATHY"
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
    url = "https://www.cathaybk.com.tw/mybank/"
    client = Cathy(id, uid, pwd)
    client.login(url)
    cash = client.info()
    print(f"cash: {cash}")
    client.logout()

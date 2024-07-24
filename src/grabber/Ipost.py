import argparse
import configparser
import logging
import re

import ddddocr
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Ipost:
    def __init__(self, id, uid, pwd):
        self.driver = webdriver.Chrome()
        self.id = id
        self.uid = uid
        self.pwd = pwd

    def login(self, url):
        self.driver.get(url)
        flag = True
        while flag:
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//*[@id='modal']/div[2]/button")
                    )
                ).click()
            except TimeoutException:
                pass

            # change login method
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//*[@id='content_wh']/div[1]/div/ul/li[1]/a")
                )
            ).click()

            id = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='cifID']"))
            )
            id.send_keys(self.id)

            uid = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//*[@id='userID_1_Input']")
                )  # noqa:E501
            )
            uid.send_keys(self.uid)

            pwd = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//*[@id='userPWD_1_Input']")
                )  # noqa:E501
            )
            pwd.send_keys(self.pwd)

            # ocr verification
            captcha_image = self.driver.find_element(
                By.XPATH, "//*[@id='tab1']/div[14]/img"
            )
            captcha_image.screenshot("code.png")
            ocr = ddddocr.DdddOcr(show_ad=False)
            with open("code.png", "rb") as fp:
                img = fp.read()
            captcha_node = ocr.classification(img)
            code = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//*[@id='tab1']/div[11]/input")
                )
            )
            code.send_keys(captcha_node)

            btn_login = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//*[@id='tab1']/div[12]/a")
                )  # noqa:E501
            )
            btn_login.click()
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.alert_is_present()
                ).accept()  # noqa:E501
            except TimeoutException:
                flag = False

            if flag:
                self.driver.refresh()

        # confirm login success
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//*[@id='wrapper']/div/div/div/ng-include/div/div[1]/div/div[1]",  # noqa:E501
                )
            )
        )
        logging.info("LOGIN SUCCESSFUL")

    def info(self):
        elem = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[@id='css_table2']/div[2]/div[3]/span")
            )
        )
        cash = re.sub(r"[^\d.-]", "", elem.text.strip())
        return cash

    def logout(self):
        btn_logout = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='nav']/ul/li[7]/a"))
        )
        btn_logout.click()
        btn_confirm = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[3]/div/div/div[3]/button[1]")
            )
        )
        btn_confirm.click()
        self.driver.close()
        logging.info("LOGOUT SUCCESSFUL")


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO
    )
    exchange = "IPOST"
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
    url = "https://ipost.post.gov.tw/pst/home.html"
    client = Ipost(id, uid, pwd)
    client.login(url)
    cash = client.info()
    print(f"cash: {cash}")
    client.logout()

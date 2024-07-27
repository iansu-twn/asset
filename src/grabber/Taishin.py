import argparse
import logging
import re

import ddddocr
from Asset import Asset
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Taishin(Asset):
    def __init__(self, exchange):
        super().__init__(exchange)

    def login(self):
        self.driver.get(self.base_url)
        id = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[@id='userId']/input")
            )  # noqa:E501
        )
        id.send_keys(self.id)

        uid = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[@id='userName']/input")
            )  # noqa:E501
        )
        uid.send_keys(self.uid)

        pwd = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//*[@id='setLoginData']/div[1]/form/div[1]/div/div[3]/div/input",  # noqa:E501
                )
            )
        )
        pwd.send_keys(self.pwd)

        # ocr verification
        flag = True
        while flag:
            captcha_image = self.driver.find_element(
                By.XPATH,
                "//*[@id='setLoginData']/div[1]/form/div[1]/div/div[4]/div/div[2]",  # noqa:E501
            )
            captcha_image.screenshot("code.png")
            ocr = ddddocr.DdddOcr(show_ad=False)
            with open("code.png", "rb") as fp:
                img = fp.read()
            captcha_node = ocr.classification(img)
            code = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//*[@id='setLoginData']/div[1]/form/div[1]/div/div[4]/div/div[1]/div/input",  # noqa:E501
                    )
                )
            )
            code.send_keys(captcha_node)
            btn_login = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//*[@id='setLoginData']/div[1]/form/div[2]/button",
                    )  # noqa:E501
                )
            )
            btn_login.click()
            try:
                btn_error = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            "/html/body/ngb-modal-window/div/div/app-modal/div[2]/div/button",  # noqa:E501
                        )
                    )
                )
                btn_error.click()
            except TimeoutException:
                flag = False
        logging.info(f"{self.exchange} LOGIN SUCCESSFUL")

    def info(self):
        # scam message confirm
        try:
            btn_scam = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//*[@id='jqBtnCloseCookie']")
                )  # noqa: E501
            )
            btn_scam.click()
        except TimeoutException:
            pass

        btn_unhidden = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[@id='toggleShowAmount']/i[1]")
            )  # noqa:E501
        )
        btn_unhidden.click()
        elem = (
            WebDriverWait(self.driver, 10)
            .until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "//*[@id='first-element-introduction']/div[1]/div[2]/div",  # noqa:E501
                    )
                )
            )
            .text
        )
        cash = float(re.sub(r"[^\d.-]", "", elem.strip()))
        return cash

    def logout(self):
        btn_logout = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "/html/body/app-root/div/app-dashboard/richart-header/header/div/div/nav/div[2]/div/a",  # noqa:E501
                )
            )
        )
        btn_logout.click()
        btn_confirm = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "/html/body/ngb-modal-window/div/div/app-modal/div[2]/div[2]/button",  # noqa:E501
                )
            )
        )
        btn_confirm.click()
        self._close_driver()


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO
    )
    exchange = "TAISHIN"
    parser = argparse.ArgumentParser(exchange)
    args = parser.parse_args()
    client = Taishin(exchange)
    client.login()
    cash = client.info()
    logging.info(f"Asset on {exchange}: {cash}")
    client.logout()

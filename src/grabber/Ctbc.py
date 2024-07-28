import argparse
import logging
import re

from Asset import Asset
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Ctbc(Asset):
    def __init__(self, exchange):
        super().__init__(exchange)

    def login(self):
        self.driver.get(self.base_url)
        try:
            btn_message = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "/html/body/app/modal-text/div/div/div/div[1]/a",
                    )  # noqa:E501
                )
            )
            btn_message.click()
        except TimeoutException:
            pass

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
        logging.info(f"{self.exchange} LOGIN SUCCESSFUL")

    def info(self):
        elem = (
            WebDriverWait(self.driver, 10)
            .until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "/html/body/app/div[1]/div[2]/twrbc-home-qu000-010/div/div/nav-tabs-overview/div/div[1]/span/span",  # noqa:E501
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
                (By.XPATH, "//*[@id='btnHeaderLogout']")
            )  # noqa:E501
        )
        btn_logout.click()
        btn_confirm = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "/html/body/app/modal-confirm[2]/div/div/div/div[3]/a[1]",
                )  # noqa:E501
            )
        )
        btn_confirm.click()
        self._close_driver()


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO
    )
    exchange = "CTBC"
    parser = argparse.ArgumentParser(exchange)
    args = parser.parse_args()
    client = Ctbc(exchange)
    client.login()
    cash = client.info()
    logging.info(f"Asset on {exchange}: {cash}")
    client.logout()

import argparse
import logging
import time

import pandas as pd
from Asset import Asset
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Firstrade(Asset):
    def __init__(self, exchange):
        super().__init__(exchange)

    def login(self):
        self.driver.get(self.base_url)

        uid = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='username']"))
        )
        uid.send_keys(self.uid)

        pwd = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='password']"))
        )
        pwd.send_keys(self.pwd)

        btn_login = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[@id='loginButton']")
            )  # noqa:E501
        )
        btn_login.click()

        btn_check = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body/div/main/div/div/div[3]/a")
            )
        )
        btn_check.click()

        code = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='pin']"))
        )
        code.send_keys(self.code)

        btn_continue = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[@id='form-pin']/div[2]/button")
            )
        )
        btn_continue.click()

        logging.info(f"{self.exchange} LOGIN SUCCESSFUL")

    def info(self):
        cash_info = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[@id='myaccount_link']/a")
            )  # noqa:E501
        )
        cash_info.click()

        cash_text = (
            WebDriverWait(self.driver, 10)
            .until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "//*[@id='maincontent']/div/table/tbody/tr/td[1]/div/div[2]/table[1]/tbody/tr[1]/td[1]",  # noqa:E501
                    )
                )
            )
            .text
        )
        cash = float(cash_text.replace(",", "").strip()[1:])

        stock_info = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[@id='myaccount_menu']/li[2]/a/span")
            )
        )
        stock_info.click()
        time.sleep(3)
        html = self.driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        elem = soup.find("table", {"id": "positiontable"})
        data = elem.find("tbody").find_all("tr")
        rows = []
        for row in data:
            cols = row.find_all("td")
            dt = {
                "symbol": cols[0].text.strip(),
                "qty": cols[1].text,
                "price": cols[2].text,
                "cap": float(cols[5].text.replace(",", "")),
                "unit_cost": float(cols[6].text.replace(",", "")),
                "total_cost": float(cols[7].text.replace(",", "")),
                "pnl": float(cols[8].text.replace(",", "").strip()[1:])
                * (1 if (cols[8].text)[0] == "+" else -1),
                "pnl_%": float(cols[9].text.replace(",", "").strip()[1:])
                * (1 if (cols[9].text)[0] == "+" else -1),
            }
            rows.append(dt)
        df = pd.DataFrame(rows)
        return cash, df

    def logout(self):
        btn_logout = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[@id='head']/ul/li[8]/a")
            )  # noqa:E501
        )
        btn_logout.click()
        self._close_driver()


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO
    )
    exchange = "FIRSTRADE"
    parser = argparse.ArgumentParser(exchange)
    args = parser.parse_args()
    client = Firstrade(exchange)
    client.login()
    cash, stock = client.info()
    logging.info(f"cap: {round(stock.cap.sum(), 3)}")
    logging.info(f"total_cost: {round(stock.total_cost.sum(), 3)}")
    logging.info(f"pnl: {round(stock.pnl.sum(), 3)}")
    logging.info(f"Asset on {exchange}: {round(cash + stock.cap.sum(), 3)}")
    client.logout()

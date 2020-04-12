from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import atexit
import time
import os

BASEURL = "https://www.bigbasket.com/"
LOGIN_URL = "auth/login/"
BASKET_URL = "basket/?ver=1"
BB_LOGO_LOCATOR = (By.XPATH, "//a[@title='Bigbasket']")
CHKOUT_BTN_LOCATOR = (By.XPATH, "//button[@id = 'checkout']")


class Try_BB_Checkout:
    def __init__(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.get(f"{BASEURL}{LOGIN_URL}")
        self.driver.maximize_window()
        print("Please login")
        WebDriverWait(self.driver, 60).until(
            lambda driver: self.driver.current_url == f"{BASEURL}"
        )
        print("Logged In")
        atexit.register(self._quit)

    def try_checkout(self):
        while True:
            try:
                print("Trying to find a slot.")
                self.driver.get(f"{BASEURL}{BASKET_URL}")
                WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located(CHKOUT_BTN_LOCATOR)
                )
                self.driver.find_element(*CHKOUT_BTN_LOCATOR).click()
                WebDriverWait(self.driver, 10).until(EC.title_contains("checkout"))
                self.__class__.notify()
                break

            except TimeoutException:
                print("No slots found. Retrying")
                time.sleep(30)
            except Exception as e:
                raise

    @staticmethod
    def notify():
        msg = "BigBasket Slots Available!"
        print(f"{msg}")
        os_specific_cmds = {
            "posix": f"""osascript -e 'display notification "{msg}" with title "{msg}"'""",
            "Linux": f'spd-say "{msg}',
        }
        for _ in range(3):
            try:
                os_specific_cmds[os.name]
            except KeyError:
                from win10toast import ToastNotifier

                toaster = ToastNotifier()
                toaster.show_toast(f"{msg}")
            time.sleep(5)

    def _quit(self):
        self.driver.quit()


b = Try_BB_Checkout()
b.try_checkout()

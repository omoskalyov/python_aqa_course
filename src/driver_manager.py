import platform
import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from src.constants import *


class DriverManager:

    def init_driver(self, browser):
        def chrome():
            chrome_options = Options()
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-infobars")
            #chrome_options.add_argument("--incognito")
            chrome_options.headless = BROWSER_HEADLESS_MODE
            driver = webdriver.Chrome(executable_path=self._get_driver_path(browser), chrome_options=chrome_options)
            driver.implicitly_wait(SELENIUM_DEFAULT_IMPLICIT_TIMEOUT)
            driver.maximize_window()
            return driver

        def firefox():
            return None

        switcher = {
            "chrome": chrome,
            "firefox": firefox,
        }

        return switcher.get(browser, None)()

    def _get_driver_path(self, browser):

        os_name = platform.system().lower()
        root_dir = sys.path[0]

        def chrome():
            return os.path.join(root_dir,"drivers",os_name,"chromedriver"+("", ".exe")["win" in os_name])

        def firefox():
            return None

        switcher = {
            'chrome': chrome,
            'firefox': firefox,
        }

        return switcher.get(browser, None)()


import platform
import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Driver:

    def init_browser(self, browser):
        def chrome():
            chrome_options = Options()
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-infobars")
            chrome_options.headless = False
            driver = webdriver.Chrome(executable_path=self._get_driver_path(browser), chrome_options=chrome_options)
            driver.implicitly_wait(10)
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
        #root_dir = os.path.dirname(sys.modules['__main__'].__file__)
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


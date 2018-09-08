import platform
import os
import sys
from selenium import webdriver


class BrowserFactory:

    def init_browser(self, browser):
        def chrome():
            return driver

        def firefox():
            return None

        switcher = {
            1: chrome,
            2: firefox,
        }


        return switcher.get(browser, None)


    def _get_driver_path(self, browser):

        os = platform.system().lower()
        root_dir = os.path.dirname(sys.modules['__main__'].__file__)

        def chrome():
            return os.join(root_dir,os)

        def firefox():
            return None

        switcher = {
            1: chrome,
            2: firefox,
        }

        return switcher.get(browser, None)


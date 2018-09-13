from time import sleep

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.constants import *


class BasePage():
    def __init__(self, driver):
        self.driver = driver

    def wait_till_element_is_ready(self, locator, timeout=SELENIUM_DEFAULT_EXPLICIT_TIMEOUT, wait_attempts=1):
        for _ in range(wait_attempts):
            try:
                wait = WebDriverWait(self.driver, timeout)
                wait.until(EC.presence_of_element_located((locator[0], locator[1])))
            except StaleElementReferenceException:  # repeat wait if element is stale
                pass  # do nothing

    def wait_till_element_disappears(self, locator, timeout=SELENIUM_DEFAULT_EXPLICIT_TIMEOUT):
        self.driver.implicitly_wait(0) # remove implicit timeout to speed up waiting
        wait = WebDriverWait(self.driver, timeout)
        wait.until_not(EC.presence_of_element_located((locator[0], locator[1])))
        self.driver.implicitly_wait(SELENIUM_DEFAULT_IMPLICIT_TIMEOUT)
        return

    def is_element_exists(self, locator):
        elements = self.driver.find_elements(locator[0], locator[1])
        if len(elements):
            return True
        else:
            return False

    def _get_web_element(self, locator, explicit_timeout=0):
        if explicit_timeout != 0:
            self.wait_till_element_is_ready(locator, explicit_timeout)
        return self.driver.find_element(locator[0], locator[1])

    def try_command(self, *args, command, attempts=5, delay=1):
        for _ in range(attempts):
            try:
                command(*args)
            except:
                sleep(delay)
                continue
            return
        command()

    def wait_till_element_is_invisible(self, locator, timeout=SELENIUM_DEFAULT_EXPLICIT_TIMEOUT):
        self.driver.implicitly_wait(0) # remove implicit timeout to speed up waiting
        wait = WebDriverWait(self.driver, timeout)
        wait.until(EC.invisibility_of_element((locator[0], locator[1])))
        self.driver.implicitly_wait(SELENIUM_DEFAULT_IMPLICIT_TIMEOUT)
        return



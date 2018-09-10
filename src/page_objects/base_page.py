from selenium import webdriver as driver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import *
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from src.constants import *

class BasePage():
    def __init__(self, driver):
        self.driver = driver

    def wait_till_element_is_ready(self, locator, timeout = SELENIUM_DEFAULT_EXPLICIT_TIMEOUT, wait_attempts = 1):
        for _ in range(wait_attempts):
            try:
                wait = WebDriverWait(self.driver, timeout)
                wait.until(EC.presence_of_element_located((locator[0], locator[1])))
            except StaleElementReferenceException as e: # repeat wait if element is stale
                pass # do nothing

    def is_element_exists(self, locator, timeout = SELENIUM_DEFAULT_EXPLICIT_TIMEOUT, interval = 1):

        # if timeout >= 10:
        #
        #     attempts = timeout / 10
        #
        #     for _ in range(attempts):

                elements = self.driver.find_elements(locator[0], locator[1])
                if len(elements):
                    return True
                else:
                    return False

    def _get_web_element(self, locator, explicit_timeout=0):
        if explicit_timeout != 0:
            self.wait_till_element_is_ready(locator,explicit_timeout)
        return self.driver.find_element(locator[0], locator[1])

        # wait = driver.WebDriverWait(driver, 10).until(EC.presence_of_element_located(By.CLASS_NAME, 'x'))

        # try:
        #     element = driver.WebDriverWait(driver, 10).until(
        #         EC.presence_of_element_located((By.ID, "myDynamicElement"))
        #     )


from selenium import webdriver as driver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import *
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from src.constants import *
from src.page_objects.base_page import BasePage


class MainPage(BasePage):

    _user_profile_popup_menu_locator = (By.ID, "header-details-user-fullname")

    _logout_menu_item_locator = (By.ID, "log_out")



    def is_open(self):

        return self.is_element_exists(__class__._user_profile_popup_menu_locator)


    def logout(self):
        self.user_profile_popup_menu = self._get_web_element(__class__._user_profile_popup_menu_locator)
        self.user_profile_popup_menu.click()

        self.logout_menu_item = self._get_web_element(__class__._logout_menu_item_locator)
        self.logout_menu_item.click()

        #self.wait_till_element_is_ready(__class__._login_button_locator)



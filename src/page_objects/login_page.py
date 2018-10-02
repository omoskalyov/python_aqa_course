import allure
from selenium.webdriver.common.by import *

from src.page_objects.base_page import BasePage
from src.page_objects.main_page import MainPage
import types


class LoginPage(BasePage):
    _user_name_edit_field_locator = (By.ID, "login-form-username")
    _user_password_edit_field_locator = (By.ID, "login-form-password")
    _login_button_locator = (By.ID, "login")
    _user_profile_popup_menu_locator = (By.ID, "header-details-user-fullname")
    _login_failed_err_msg_locator = (By.CSS_SELECTOR, ".aui-message.error")
    _top_right_login_button_locator = (By.CSS_SELECTOR, "a.aui-nav-link.login-link")

    @allure.step
    def login(self, username, password):
        self.user_name_edit_field = self._get_web_element(__class__._user_name_edit_field_locator)
        self.user_name_edit_field.send_keys(username)

        self.user_password_edit_field = self._get_web_element(__class__._user_password_edit_field_locator)
        if isinstance(password, types.FunctionType):
            password = password()
        self.user_password_edit_field.send_keys(password)

        self.login_button = self._get_web_element(__class__._login_button_locator)
        self.login_button.click()

        return MainPage(self.driver)

    @allure.step
    def is_failed_login_error_message_exists(self, error_message_text):
        self.login_failed_err_msg = self._get_web_element(__class__._login_failed_err_msg_locator)
        return error_message_text in self.login_failed_err_msg.text

    @allure.step
    def is_open(self):
        return self.is_element_exists(__class__._top_right_login_button_locator)

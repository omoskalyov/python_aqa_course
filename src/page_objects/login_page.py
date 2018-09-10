from selenium import webdriver as driver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import *
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from src.constants import *
from src.page_objects.base_page import BasePage
from src.page_objects.main_page import MainPage

# class BasePage():
#     def __init__(self, driver):
#         self.driver = driver
#
#     def wait_till_element_is_ready(self, locator, timeout = SELENIUM_DEFAULT_EXPLICIT_TIMEOUT, wait_attempts = 1):
#         for _ in range(wait_attempts):
#             try:
#                 WebDriverWait(driver, timeout).until(EC.presence_of_element_located((locator[0], locator[1])))
#             except StaleElementReferenceException as e: # repeat wait if element is stale
#                 pass # do nothing
#
#     def _get_web_element(self, locator, explicit_timeout=0):
#         if explicit_timeout != 0:
#             self.wait_till_element_is_ready(locator,explicit_timeout)
#         return self.driver.find_element(locator[0], locator[1])
#
#         # wait = driver.WebDriverWait(driver, 10).until(EC.presence_of_element_located(By.CLASS_NAME, 'x'))
#
#         # try:
#         #     element = driver.WebDriverWait(driver, 10).until(
#         #         EC.presence_of_element_located((By.ID, "myDynamicElement"))
#         #     )



class LoginPage(BasePage):

    # @FindBy(id = "login-form-username")
    # private WebElement userNameEditField;
    #
    # @FindBy(id = "login-form-password")
    # private WebElement userPasswordEditField;
    #
    # @FindBy(id = "login")
    # private WebElement loginButton;

    _user_name_edit_field_locator = (By.ID, "login-form-username")
    #user_name_edit_field = WebElement(None,None)

    _user_password_edit_field_locator = (By.ID, "login-form-password")
    #user_password_edit_field = WebElement(None,None)

    _login_button_locator = (By.ID, "login")
    #login_button = WebElement(None,None)

    _user_profile_popup_menu_locator = (By.ID, "header-details-user-fullname")

    _login_failed_err_msg_locator = (By.CSS_SELECTOR, ".aui-message.error")

    _login_button_locator = (By.CSS_SELECTOR, "a.aui-nav-link.login-link")


    #def __init__(self):
    #    user_name_edit_field = LoginPage.web_element(self.driver, LoginPage.user_name_edit_field_locator)

    def login(self, username, password):

        self.user_name_edit_field = self._get_web_element(__class__._user_name_edit_field_locator)
        self.user_name_edit_field.send_keys(username)

        self.user_password_edit_field = self._get_web_element(__class__._user_password_edit_field_locator)
        self.user_password_edit_field.send_keys(password)

        self.login_button = self._get_web_element(__class__._login_button_locator)
        self.login_button.click()

        #self.wait_till_element_is_ready(__class__._user_profile_popup_menu_locator)

        return MainPage(self.driver)

    def is_failed_login_error_message_exists(self, error_message_text):
        self.login_failed_err_msg = self._get_web_element(__class__._login_failed_err_msg_locator)
        return error_message_text in self.login_failed_err_msg.text

    def is_open(self):
        return self.is_element_exists(__class__._login_button_locator)




    # def is_title_matches(self):
    #     """Verifies that the hardcoded text "Python" appears in page title"""
    #     return "Python" in self.driver.title
    #
    # def click_go_button(self):
    #     """Triggers the search"""
    #     element = self.driver.find_element(*MainPageLocators.GO_BUTTON)
    #     element.click()





# class SearchResultsPage(BasePage):
#     """Search results page action methods come here"""
#
#     def is_results_found(self):
#         # Probably should search for this text in the specific page
#         # element, but as for now it works fine
#         return "No results found." not in self.driver.page_source


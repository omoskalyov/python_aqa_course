from selenium import webdriver as driver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import *
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from src.constants import *
from src.page_objects.base_page import BasePage
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.keys import Keys

from src.page_objects.search_page import SearchPage


class MainPage(BasePage):

    _user_profile_popup_menu_locator = (By.ID, "header-details-user-fullname")

    _logout_menu_item_locator = (By.ID, "log_out")

    _create_issue_main_form_button_locator = (By.ID, "create_link")

    _summary_edit_field_locator = (By.ID, "summary")

    _issue_type_field_locator = (By.ID, "issuetype-field")

    _project_type_field_locator = (By.ID, "project-field")

    _create_button_locator = (By.ID, "create-issue-submit")

    _error_message_locator = (By.CSS_SELECTOR, ".error")

    _cancel_button_locator = (By.CSS_SELECTOR, "a.cancel")

    _created_issue_notification_locator = (By.CSS_SELECTOR, "a.issue-created-key.issue-link")

    def is_open(self):

        return self.is_element_exists(__class__._user_profile_popup_menu_locator)

    def wait_till_page_is_open(self):
        self.wait_till_element_is_ready(__class__._user_profile_popup_menu_locator)
        return

    def logout(self):
        self.user_profile_popup_menu = self._get_web_element(__class__._user_profile_popup_menu_locator)
        self.try_command(command = self.user_profile_popup_menu.click)
        #self.user_profile_popup_menu.click()

        self.logout_menu_item = self._get_web_element(__class__._logout_menu_item_locator)
        self.logout_menu_item.click()

        #self.wait_till_element_is_ready(__class__._login_button_locator)


    def create_issue(self, project, issue_type, summary):
        self.create_issue_main_form_button = self._get_web_element(__class__._create_issue_main_form_button_locator)
        self.create_issue_main_form_button.click()

        self.project_type_field = self._get_web_element(__class__._project_type_field_locator)
        self.project_type_field.send_keys(project)
        self.project_type_field.send_keys(Keys.RETURN)

        self.try_command(issue_type, command = self._enter_issue_type)
        #self.issue_type_field = self._get_web_element(__class__._issue_type_field_locator)
        #self.try_command(issue_type, command = self.issue_type_field.send_keys)
        #self.issue_type_field.send_keys(Keys.RETURN)

        self.try_command(summary, command = self._enter_summary_field)
        #self.summary_field = self._get_web_element(__class__._summary_edit_field_locator)
        #self.summary_field.send_keys(summary)

        self.create_button = self._get_web_element(__class__._create_button_locator)
        self.create_button.click()

        self.wait_till_element_disappears(__class__._create_button_locator)

    def get_created_issue_id(self):
        self.created_issue_notification = self._get_web_element(__class__._created_issue_notification_locator)
        return self.created_issue_notification.get_attribute("data-issue-key")


    def _enter_issue_type(self, issue_type):
        self.issue_type_field = self._get_web_element(__class__._issue_type_field_locator)
        self.issue_type_field.send_keys(issue_type)
        self.issue_type_field.send_keys(Keys.RETURN)

    def _enter_summary_field(self, summary):
        self.summary_field = self._get_web_element(__class__._summary_edit_field_locator)
        self.summary_field.send_keys(summary)


    def create_issue_with_missing_summary_field(self):
        self.create_issue_main_form_button = self._get_web_element(__class__._create_issue_main_form_button_locator)
        self.create_issue_main_form_button.click()

        self.create_button = self._get_web_element(__class__._create_button_locator)
        self.create_button.click()


    def create_issue_with_not_supported_text_length(self):
        self.create_issue_main_form_button = self._get_web_element(__class__._create_issue_main_form_button_locator)
        self.create_issue_main_form_button.click()

        self.summary_field = self._get_web_element(__class__._summary_edit_field_locator)
        self.summary_field.send_keys(SUMMARY_TEXT_LONGER_THAN_SUPPORTED)

        self.create_button = self._get_web_element(__class__._create_button_locator)
        self.create_button.click()


    def is_error_message_exists(self, error_message):
        self.error_message = self._get_web_element(__class__._error_message_locator)
        return error_message in self.error_message.text


    def close_create_issue_dialog_if_exists(self):
        if self.is_element_exists(__class__._cancel_button_locator):
            self.cancel_button = self._get_web_element(__class__._cancel_button_locator)
            if self.cancel_button.is_displayed():
                self.cancel_button.click()
                try:
                    wait = WebDriverWait(self.driver, SELENIUM_DEFAULT_EXPLICIT_TIMEOUT)
                    wait.until(EC.alert_is_present())
                    alert = self.driver.switch_to.alert
                    alert.accept()
                finally:
                    pass

    def open_search_page(self):
        self.driver.get(JIRA_HOST_URL + "/issues/")

        return SearchPage(self.driver)


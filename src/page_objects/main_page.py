from selenium.webdriver.common.by import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.constants import *
from src.page_objects.base_page import BasePage
from src.page_objects.search_page import SearchPage


class MainPage(BasePage):
    _user_profile_popup_menu_locator = (By.ID, "header-details-user-fullname")

    _logout_menu_item_locator = (By.ID, "log_out")

    _create_issue_main_form_button_locator = (By.ID, "create_link")

    _summary_edit_field_locator = (By.ID, "summary")

    _issue_type_field_locator = (By.ID, "issuetype-field")

    _project_type_field_locator = (By.ID, "project-field")

    _priority_field_locator = (By.ID, "priority-field")

    _create_button_locator = (By.ID, "create-issue-submit")

    _error_message_locator = (By.CSS_SELECTOR, ".error")

    _cancel_button_locator = (By.CSS_SELECTOR, "a.cancel")

    _created_issue_notification_locator = (By.CSS_SELECTOR, "a.issue-created-key.issue-link")

    _edit_button_locator = (By.ID, "edit-issue")

    _assignee_field_locator = (By.ID, "assignee-field")

    _update_button_locator = (By.ID, "edit-issue-submit")

    _issue_priority_label_locator = (By.ID, "priority-val")

    _summary_text_locator = (By.ID, "summary-val")

    _assignee_label_locator = (By.ID, "assignee-val")

    _new_issue_popup_close_button_locator = (By.CSS_SELECTOR, ".aui-icon.icon-close")

    _blanket_locator = (By.CSS_SELECTOR, ".aui-blanket")

    def is_open(self):
        return self.is_element_exists(__class__._user_profile_popup_menu_locator)

    def wait_till_page_is_open(self, timeout):
        self.wait_till_element_is_ready(__class__._user_profile_popup_menu_locator, timeout=timeout)
        return

    def logout(self):
        self.user_profile_popup_menu = self._get_web_element(__class__._user_profile_popup_menu_locator)
        self.try_command(command=self.user_profile_popup_menu.click)

        self.logout_menu_item = self._get_web_element(__class__._logout_menu_item_locator)
        self.logout_menu_item.click()

        return

    def create_issue(self, project, issue_type, summary):

        if self.is_element_exists(__class__._blanket_locator):
            self.wait_till_element_is_invisible(__class__._blanket_locator)

        self.create_issue_main_form_button = self._get_web_element(__class__._create_issue_main_form_button_locator)
        self.create_issue_main_form_button.click()

        self.project_type_field = self._get_web_element(__class__._project_type_field_locator)
        self.project_type_field.send_keys(project)
        self.project_type_field.send_keys(Keys.RETURN)

        self.try_command(issue_type, command=self._enter_issue_type)

        self.try_command(summary, command=self._enter_summary)

        self.create_button = self._get_web_element(__class__._create_button_locator)
        self.create_button.click()

        self.wait_till_element_disappears(__class__._create_button_locator)

        return

    def get_created_issue_id(self):
        self.created_issue_notification = self._get_web_element(__class__._created_issue_notification_locator)
        return self.created_issue_notification.get_attribute("data-issue-key")

    def _enter_issue_type(self, issue_type):
        self.issue_type_field = self._get_web_element(__class__._issue_type_field_locator)
        self.issue_type_field.send_keys(issue_type)
        self.issue_type_field.send_keys(Keys.RETURN)
        return

    def _enter_summary(self, summary):
        self.summary_field = self._get_web_element(__class__._summary_edit_field_locator)
        self.summary_field.clear()
        self.summary_field.send_keys(summary)
        return

    def _enter_assignee_name(self, assignee_name):
        self.assignee_field = self._get_web_element(__class__._assignee_field_locator)
        self.assignee_field.send_keys(assignee_name)
        self.assignee_field.send_keys(Keys.RETURN)
        return

    def _enter_priority(self, priority):
        self.priority_field = self._get_web_element(__class__._priority_field_locator)
        self.priority_field.send_keys(priority)
        self.priority_field.send_keys(Keys.RETURN)
        return

    def create_issue_with_missing_summary_field(self):
        self.create_issue_main_form_button = self._get_web_element(__class__._create_issue_main_form_button_locator)
        self.create_issue_main_form_button.click()

        self.create_button = self._get_web_element(__class__._create_button_locator)
        self.create_button.click()
        return

    def create_issue_with_not_supported_text_length(self):
        self.create_issue_main_form_button = self._get_web_element(__class__._create_issue_main_form_button_locator)
        self.create_issue_main_form_button.click()

        self.summary_field = self._get_web_element(__class__._summary_edit_field_locator)
        self.summary_field.send_keys(SUMMARY_TEXT_LONGER_THAN_SUPPORTED)

        self.create_button = self._get_web_element(__class__._create_button_locator)
        self.create_button.click()
        return

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

    def open_issue_by_id(self, id):
        self.driver.get(JIRA_HOST_URL + "/browse/" + id)
        return

    def open_edit_issue_dialog(self):
        self.edit_button = self._get_web_element(__class__._edit_button_locator)
        self.edit_button.click()
        return

    def update_issue(self, summary, priority, assignee_name):
        self.try_command(summary, command=self._enter_summary)
        self.try_command(priority, command=self._enter_priority)
        self.try_command(assignee_name, command=self._enter_assignee_name)

        self.update_button = self._get_web_element(__class__._update_button_locator)
        self.update_button.click()

        self.wait_till_element_disappears(__class__._update_button_locator)

        return

    def get_issue_summary(self):
        summary_text = self._get_web_element(__class__._summary_text_locator)
        return summary_text.text

    def get_issue_priority(self):
        issue_priority = self._get_web_element(__class__._issue_priority_label_locator)
        return issue_priority.text

    def get_issue_assignee(self):
        assignee_name = self._get_web_element(__class__._assignee_label_locator)
        return assignee_name.text

    def close_new_issue_created_popup_if_exists(self):
        if self.is_element_exists(__class__._new_issue_popup_close_button_locator):
            self.new_issue_popup_close_button = self._get_web_element(__class__._new_issue_popup_close_button_locator)
            self.new_issue_popup_close_button.click()
        return



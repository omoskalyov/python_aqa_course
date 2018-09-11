from selenium import webdriver as driver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import *
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from src.constants import *
from src.page_objects.base_page import BasePage
from selenium.common.exceptions import NoAlertPresentException


class SearchPage(BasePage):

    _amount_of_found_issues_label_locator = (By.CSS_SELECTOR, ".showing")

    def search_issue_by_summary(self, summary):
        self.driver.get(JIRA_HOST_URL + "/?jql=" + JQL_QUERY + summary)

        self.amount_of_found_issues_label = self._get_web_element(__class__._amount_of_found_issues_label_locator)
        return str(self.amount_of_found_issues_label.text).split(" ")[2]



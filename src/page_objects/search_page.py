from selenium import webdriver as driver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import *
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from src.constants import *
from src.page_objects.base_page import BasePage
from selenium.common.exceptions import NoAlertPresentException

#import urllib.parse


class SearchPage(BasePage):

    _amount_of_found_issues_label_locator = (By.CSS_SELECTOR, ".showing")

    _search_results_list_locator = (By.CSS_SELECTOR, ".search-results")



    def search_issue_by_summary(self, summary):
        #encoded_query_string = urllib.parse.quote_plus("/?jql=" + JQL_QUERY + '"' + summary + '"')
        #self.driver.get(JIRA_HOST_URL + encoded_query_string)

        self.driver.get(JIRA_HOST_URL + "/issues/?jql=" + JQL_QUERY + summary)

        if self.is_element_exists(__class__._amount_of_found_issues_label_locator):
            self.amount_of_found_issues_label = self._get_web_element(__class__._amount_of_found_issues_label_locator)
            return int(self.amount_of_found_issues_label.text.split(" ")[2])
        else:
            return

    def is_search_results_list_exists(self):
        return self.is_element_exists(__class__._search_results_list_locator)


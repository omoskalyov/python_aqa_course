import allure
from selenium.webdriver.common.by import *

from src.constants import *
from src.page_objects.base_page import BasePage


class SearchPage(BasePage):
    _amount_of_found_issues_label_locator = (By.CSS_SELECTOR, ".showing")
    _search_results_list_locator = (By.CSS_SELECTOR, ".search-results")

    @allure.step
    def search_issue_by_summary(self, summary):

        self.driver.get(JIRA_HOST_URL + "/issues/?jql=" + JQL_QUERY + summary)

        if self.is_element_exists(__class__._amount_of_found_issues_label_locator):
            self.amount_of_found_issues_label = self._get_web_element(__class__._amount_of_found_issues_label_locator)
            return int(self.amount_of_found_issues_label.text.split(" ")[2])
        else:
            return

    @allure.step
    def is_search_results_list_exists(self):
        return self.is_element_exists(__class__._search_results_list_locator)


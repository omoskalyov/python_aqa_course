import pytest
import requests
from http import HTTPStatus
from src.jira_api import ApiSession, ApiIssue

from src.driver_manager import *
from src.page_objects.login_page import LoginPage

@pytest.fixture(scope="session", autouse=True)
def jira_session_fixture():

    created_issues_list = []

    yield created_issues_list

    # login using api
    api_session = ApiSession()
    r = requests.get(api_session.endpoint_url, auth=(USERNAME, DECODED_PASSWORD))
    assert HTTPStatus.OK == r.status_code

    # create session in jira
    s = requests.session()
    s.cookies = r.cookies

    # delete created issues
    for issue_id in created_issues_list:
        r = s.delete(ApiIssue.endpoint_url + "/" + issue_id)
        assert (HTTPStatus.OK == r.status_code) or (HTTPStatus.NO_CONTENT == r.status_code)

    # logout once the pytest session ends
    r = s.delete(api_session.endpoint_url)
    assert (HTTPStatus.OK == r.status_code) or (HTTPStatus.NO_CONTENT == r.status_code)



@pytest.fixture()
def driver():

    driver_manager = DriverManager()
    driver = driver_manager.init_driver("chrome")
    driver.get(JIRA_HOST_URL)
    yield driver
    driver.quit()


@pytest.fixture()
def web_tests_fixture(jira_session_fixture):
    created_issues_list = jira_session_fixture

    # open jira login page
    driver_manager = DriverManager()
    driver = driver_manager.init_driver("chrome")
    driver.get(JIRA_HOST_URL)

    # login
    login_page = LoginPage(driver)
    main_page = login_page.login(USERNAME,DECODED_PASSWORD)
    main_page.wait_till_page_is_open()

    yield main_page, created_issues_list

    # logout
    main_page.close_create_issue_dialog_if_exists()
    main_page.logout()
    driver.quit()


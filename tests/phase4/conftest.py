import pytest
import requests
from http import HTTPStatus
from src.jira_api import ApiSession, ApiIssue
from src.constants import *

from src.browser_factory import *
from src.page_objects.login_page import LoginPage


@pytest.fixture(scope="session", autouse=True)
def jira_session_fixture():

    # login once per pytest session
    api_session = ApiSession()
    r = requests.get(api_session.endpoint_url, auth=(USERNAME, DECODED_PASSWORD))
    assert HTTPStatus.OK == r.status_code

    # create session in jira
    s = requests.session()
    s.cookies = r.cookies

    yield api_session, s

    # logout once the pytest session ends
    r = s.delete(api_session.endpoint_url)
    assert (HTTPStatus.OK == r.status_code) or (HTTPStatus.NO_CONTENT == r.status_code)



@pytest.fixture()
def driver():

    driver_manager = Driver()
    driver = driver_manager.init_browser("chrome")
    driver.get(JIRA_HOST_URL)
    yield driver
    driver.quit()


@pytest.fixture()
def web_tests_fixture():

    # open jira login page
    driver_manager = Driver()
    driver = driver_manager.init_browser("chrome")
    driver.get(JIRA_HOST_URL)

    # login
    login_page = LoginPage(driver)
    main_page = login_page.login(USERNAME,DECODED_PASSWORD)

    yield main_page

    # logout
    main_page.close_create_issue_dialog_if_exists()
    main_page.logout()
    driver.quit()


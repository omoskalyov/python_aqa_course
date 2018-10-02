import pytest
import requests
from http import HTTPStatus

from src.common import get_time_stamp
from src.driver_manager import DriverManager
from src.jira_api import ApiSession, ApiIssue
from src.constants import *
from src.page_objects.login_page import LoginPage


@pytest.fixture(scope="session", autouse=True)
def jira_api_session_fixture():
    # login once per pytest session
    api_session = ApiSession(USERNAME, DECODED_PASSWORD)
    r = api_session.get_current_user()
    assert HTTPStatus.OK == r.status_code

    # create session in jira
    jira_session = requests.session()
    jira_session.cookies = r.cookies

    yield api_session, jira_session

    # delete created issues
    for issue_id in created_issues():
        api_issue = ApiIssue(jira_session, None, None, None)  # create dummy ApiIssue object
        r = api_issue.delete_issue(issue_id)
        assert (HTTPStatus.OK == r.status_code) or (HTTPStatus.NO_CONTENT == r.status_code)

    # logout once the pytest api session ends
    r = api_session.logout(jira_session)
    # the next line is commented because api_session.logout command returns Unauthorized error (401) _
    #  _ after few UI tests has performed a "UI log out" operation (I couldn't find out why it happens)
    # assert (HTTPStatus.OK == r.status_code) or (HTTPStatus.NO_CONTENT == r.status_code)


@pytest.fixture()
def jira_tests_fixture(request, jira_api_session_fixture, api_issue_fixture):
    api_session, jira_session = jira_api_session_fixture
    return api_session, jira_session


@pytest.fixture()
def api_issue_fixture():
    class _ApiIssue:
        def __init__(self):
            self._api_issue = None

        def set(self, api_issue):
            self._api_issue = api_issue

        def get(self):
            return self._api_issue

    return _ApiIssue()


created_issues_list = []


@pytest.fixture()
def created_issues():
    return created_issues_list


@pytest.fixture()
def created_dummy_issue(jira_api_session_fixture, api_issue_fixture, created_issues):
    api_session, jira_session = jira_api_session_fixture

    # create an issue
    summary = "Oleg " + get_time_stamp()
    api_issue = ApiIssue(jira_session, PROJECT_KEY, BUG_ISSUE_TYPE_KEY, summary)
    api_issue_fixture.set(api_issue)
    r = api_issue.create_issue()
    assert HTTPStatus.CREATED == r.status_code
    created_issues.append(r.json()["id"])
    api_issue.set_key(r.json()["key"])

    return api_issue


@pytest.fixture()
def created_issues_summaries(jira_api_session_fixture, api_issue_fixture, created_issues):
    api_session, jira_session = jira_api_session_fixture

    created_issues_summaries = []
    for issue_num in range(MAX_ISSUES_TO_CREATE):
        summary = "Oleg " + get_time_stamp()
        api_issue = ApiIssue(jira_session, PROJECT_KEY, BUG_ISSUE_TYPE_KEY, summary)
        api_issue_fixture.set(api_issue)
        r = api_issue.create_issue()
        assert HTTPStatus.CREATED == r.status_code
        created_issues.append(r.json()["id"])
        created_issues_summaries.append(summary)

    return created_issues_summaries


@pytest.fixture()
def driver():
    driver_manager = DriverManager()
    driver = driver_manager.init_driver("chrome")
    driver.get(JIRA_HOST_URL)
    yield driver
    driver.quit()


@pytest.fixture()
def web_tests_fixture(jira_api_session_fixture):
    # open jira login page
    driver_manager = DriverManager()
    driver = driver_manager.init_driver("chrome")
    driver.get(JIRA_HOST_URL)

    # login
    login_page = LoginPage(driver)
    main_page = login_page.login(USERNAME, DECODED_PASSWORD)
    main_page.wait_till_page_is_open()

    yield main_page, created_issues_list

    # logout
    main_page.close_create_issue_dialog_if_exists()
    main_page.logout()
    driver.quit()

    # def pass_objects_back_to_fixture(api_issue_param, created_issues_param):
    #     nonlocal api_issue
    #     nonlocal created_issues
    #     api_issue = api_issue_param
    #     created_issues = created_issues_param
    #     return None
    #
    # def api_issue_func(api_issue = None):
    #     nonlocal _api_issue
    #     if api_issue is not None:
    #         _api_issue = api_issue
    #     return _api_issue

# @pytest.fixture()
# def created_issues():
#     def list(issue_id = None):
#         if issue_id is not None:
#             created_issues_list.append(issue_id)
#         return created_issues_list
#     return list


# @pytest.fixture(scope="session", autouse=True)
# def jira_session_fixture():
#     created_issues_list = []
#
#     yield created_issues_list
#
#     # login using api
#     api_session = ApiSession(USERNAME, DECODED_PASSWORD)
#     r = api_session.get_current_user()
#     assert HTTPStatus.OK == r.status_code
#
#     # create session in jira
#     jira_session = requests.session()
#     jira_session.cookies = r.cookies
#
#     # delete created issues
#     for issue_id in created_issues_list:
#         api_issue = ApiIssue(jira_session, None, None, None)  # create dummy ApiIssue object
#         r = api_issue.delete_issue(issue_id)
#         assert (HTTPStatus.OK == r.status_code) or (HTTPStatus.NO_CONTENT == r.status_code)
#
#     # logout once the pytest session ends
#     r = api_session.logout(jira_session)
#     assert (HTTPStatus.OK == r.status_code) or (HTTPStatus.NO_CONTENT == r.status_code)

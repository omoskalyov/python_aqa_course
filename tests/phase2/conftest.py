import pytest
import requests
from http import HTTPStatus

from src.common import get_time_stamp
from src.jira_api import ApiSession, ApiIssue
from src.constants import *


@pytest.fixture(scope="session", autouse=True)
def jira_session_fixture():
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

    # logout once the pytest session ends
    r = api_session.logout(jira_session)
    assert (HTTPStatus.OK == r.status_code) or (HTTPStatus.NO_CONTENT == r.status_code)


@pytest.fixture()
def jira_tests_fixture(request, jira_session_fixture, api_issue_fixture):
    api_session, jira_session = jira_session_fixture
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
def created_dummy_issue(jira_session_fixture, api_issue_fixture, created_issues):
    api_session, jira_session = jira_session_fixture

    # create an issue
    summary = "Oleg " + get_time_stamp()
    api_issue = ApiIssue(jira_session, PROJECT_KEY, BUG_ISSUE_TYPE_KEY, summary)
    api_issue_fixture.set(api_issue)
    r = api_issue.create_issue()
    assert HTTPStatus.CREATED == r.status_code
    created_issues.append(r.json()["id"])

    return api_issue

    # def pass_objects_back_to_fixture(api_issue_param, created_issues_param):
    #     nonlocal api_issue
    #     nonlocal created_issues
    #     api_issue = api_issue_param
    #     created_issues = created_issues_param
    #     return None

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

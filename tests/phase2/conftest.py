import pytest
import requests
from http import HTTPStatus
from src.jira_api import ApiSession, ApiIssue
from src.constants import *


@pytest.fixture(scope="session", autouse=True)
def jira_session():
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
def jira_tests_fixture(request, jira_session, worker_id):
    api_session, s = jira_session

    api_issue = ApiIssue(None, None, None)
    created_issues = []

    def pass_objects_back_to_fixture(api_issue_param, created_issues_param):
        nonlocal api_issue
        nonlocal created_issues
        api_issue = api_issue_param
        created_issues = created_issues_param
        return None

    yield api_session, s, created_issues, pass_objects_back_to_fixture
    # yield api_session, s, created_issues, api_issue

    # delete created issues
    for issue_id in created_issues:
        r = s.delete(api_issue.endpoint_url + "/" + issue_id)
        assert (HTTPStatus.OK == r.status_code) or (HTTPStatus.NO_CONTENT == r.status_code)


#import logging

import pytest
import requests
from http import HTTPStatus
from src.jira_api import ApiSession, ApiIssue
from src.constants import *

#s = None
#api_session = None

@pytest.fixture(scope="session", autouse=True)
def jira_session():
#    logging.basicConfig(format='%(message)s')

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
    #print >> sys.stderr, 'test_a'
    #print(str("bb")) >> sys.stderr
    #sys.stdout.write("gg")
    #print("fatal error", file="z1.txt")
#    logging.warning(str(request.node) + " " + worker_id)

    api_session, s = jira_session

    api_issue = ApiIssue(None, None, None)
    created_issues = []

    def pass_objects_back_to_fixture(api_issue_param, created_issues_param):
        nonlocal api_issue
        nonlocal created_issues
        api_issue = api_issue_param
        created_issues = created_issues_param
        return None

    # # login
    # api_session = ApiSession()
    # r = requests.get(api_session.endpoint_url, auth=(USERNAME, DECODED_PASSWORD))
    # assert HTTPStatus.OK == r.status_code
    #
    # # create issue
    # s = requests.session()
    # s.cookies = r.cookies

    yield api_session, s, created_issues, pass_objects_back_to_fixture
    # yield api_session, s, created_issues, api_issue

    # delete created issues
    for issue_id in created_issues:
        r = s.delete(api_issue.endpoint_url + "/" + issue_id)
        assert (HTTPStatus.OK == r.status_code) or (HTTPStatus.NO_CONTENT == r.status_code)

    # logout
#    r = s.delete(api_session.endpoint_url)
#    assert (HTTPStatus.OK == r.status_code) or (HTTPStatus.NO_CONTENT == r.status_code)





import pytest
import requests
import base64
from http import HTTPStatus

from phase2.tests.common import get_time_stamp
from phase2.tests.jira_api import ApiSession, ApiIssue, ApiSearch

USERNAME = 'Oleg_Moskalyov'
DECODED_PASSWORD = base64.b64decode(b'MzI3Njg=').decode('utf-8')
PROJECT_KEY = "AQAPYTHON"
BUG_ISSUE_TYPE_KEY = "10107"
JQL_SEARCH = "project = AQAPYTHON AND summary ~ Oleg AND issuetype = Bug"


def test_search_one_issue():

    # login
    api_session = ApiSession(USERNAME, DECODED_PASSWORD)
    r = requests.post(api_session.endpoint_url, json=api_session.get_body())
    assert HTTPStatus.OK == r.status_code

    # session setup
    s = requests.session()
    s.cookies = r.cookies

    # create an issue
    api_issue = ApiIssue(PROJECT_KEY, BUG_ISSUE_TYPE_KEY, "Oleg " + get_time_stamp())
    r = s.post(api_issue.endpoint_url, json=api_issue.get_body())
    assert HTTPStatus.CREATED == r.status_code
    issue_id = r.json()["id"]

    # search an issue
    api_search = ApiSearch(JQL_SEARCH,1)
    r = s.post(api_search.endpoint_url, json=api_search.get_body())
    assert HTTPStatus.OK == r.status_code

    # delete created issue
    r = s.delete(api_issue.endpoint_url + "/" + issue_id)

    # logout
    r = s.delete(api_session.endpoint_url)


def test_search_multiple_issues():

    # login
    api_session = ApiSession(USERNAME, DECODED_PASSWORD)
    r = requests.post(api_session.endpoint_url, json=api_session.get_body())
    assert HTTPStatus.OK == r.status_code

    # session setup
    s = requests.session()
    s.cookies = r.cookies

    # create several issues
    created_issues = []
    for issue_num in range(5):
        summary = "Oleg " + get_time_stamp()
        api_issue = ApiIssue(PROJECT_KEY, BUG_ISSUE_TYPE_KEY, summary)
        r = s.post(api_issue.endpoint_url, json=api_issue.get_body())
        assert HTTPStatus.CREATED == r.status_code
        issue_id = r.json()["id"]
        created_issues.append((issue_id, summary))

    # search for multiple issues
    api_search = ApiSearch(JQL_SEARCH,5)
    r = s.post(api_search.endpoint_url, json=api_search.get_body())
    assert HTTPStatus.OK == r.status_code
    assert r.json()["maxResults"] == 5
    for json_issue in r.json()["issues"]:
        #for item in created_issues:
        assert json_issue["fields"]["summary"] == created_issues[0][1]


    # delete created issue
    r = s.delete(api_issue.endpoint_url + "/" + issue_id)

    # logout
    r = s.delete(api_session.endpoint_url)



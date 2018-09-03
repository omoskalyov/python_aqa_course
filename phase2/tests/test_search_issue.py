

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
#JQL_SEARCH = "project = AQAPYTHON AND summary ~ Oleg AND issuetype = Bug"
#project = "AQAPYTHON AND (summary ~ "Oleg 2018-09-03 21:58:47" OR summary ~ "Oleg 2018-09-03 21:58:48") AND issuetype = Bug"
JQL_SEARCH = "project = AQAPYTHON AND issuetype = Bug AND summary ~ "


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
    #api_search = ApiSearch(JQL_SEARCH,1)
    jql_query = JQL_SEARCH + "'Oleg'"
    api_search = ApiSearch(jql_query,1)

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
    jql_search_prepared = JQL_SEARCH + " OR summary ~ ".join(['"' + x[1] + '"' for x in created_issues])
    api_search = ApiSearch(jql_search_prepared,5)
    r = s.post(api_search.endpoint_url, json=api_search.get_body())

    # validate the expected issues found
    assert HTTPStatus.OK == r.status_code
    assert r.json()["maxResults"] == 5
    expected_summary_list = [x[1] for x in created_issues]
    actual_summary_list = [x["fields"]["summary"] for x in r.json()["issues"]]
    for x in expected_summary_list:
        assert (x in actual_summary_list) == True

    # delete created issues
    for x in created_issues:
        issue_id = x[0]
        r = s.delete(api_issue.endpoint_url + "/" + issue_id)

    # logout
    r = s.delete(api_session.endpoint_url)


def test_search_no_results():

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

    # search for multiple issues
    jql_search_prepared = JQL_SEARCH + "'not existing issue !@#$15243'"
    api_search = ApiSearch(jql_search_prepared,1)
    r = s.post(api_search.endpoint_url, json=api_search.get_body())
    assert HTTPStatus.OK == r.status_code
    assert bool(r.json()["issues"]) == False

    # delete created issue
    r = s.delete(api_issue.endpoint_url + "/" + issue_id)

    # logout
    r = s.delete(api_session.endpoint_url)



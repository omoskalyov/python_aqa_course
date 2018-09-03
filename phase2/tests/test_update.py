

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
#JQL_SEARCH = "project = AQAPYTHON AND issuetype = Bug AND summary ~ "


def test_update_issue():

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

    # update issue
    api_issue.set_summary("Hello")
    api_issue.set_assignee("Oleg_Moskalyov")
    api_issue.set_priority("High")
    r = s.put(api_issue.endpoint_url + "/" + issue_id, json=api_issue.get_body())
    assert HTTPStatus.NO_CONTENT == r.status_code

    # validate issue is updated
    r = s.get(api_issue.endpoint_url + "/" + issue_id)
    assert HTTPStatus.OK == r.status_code
    assert r.json()["fields"]["summary"] == api_issue.get_summary()
    assert r.json()["fields"]["assignee"]["name"] == api_issue.get_assignee()
    assert r.json()["fields"]["priority"]["name"] == api_issue.get_priority()

    # delete created issue
    r = s.delete(api_issue.endpoint_url + "/" + issue_id)

    # logout
    r = s.delete(api_session.endpoint_url)


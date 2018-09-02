# from src.fibonacci.fibonacci import generateFibonacci, errText
import pytest
import requests
import base64
from http import HTTPStatus

from phase2.tests.common import get_time_stamp
from phase2.tests.jira_api import ApiSession, ApiIssue

USERNAME = 'Oleg_Moskalyov'
DECODED_PASSWORD = base64.b64decode(b'MzI3Njg=').decode('utf-8')
PROJECT_KEY = "AQAPYTHON"
BUG_ISSUE_TYPE_KEY = "10107"

# url = 'http://jira.hillel.it:8080/rest/auth/1/session'


@pytest.mark.parametrize("username,password,expected_status_code",
                         [
                             ('incorrect', DECODED_PASSWORD, HTTPStatus.UNAUTHORIZED),
                             (USERNAME, "incorrect", HTTPStatus.UNAUTHORIZED),
                             (USERNAME, DECODED_PASSWORD, HTTPStatus.OK),
                         ]
                         )
def test_login_incorrect_username(username, password, expected_status_code):
    api_session = ApiSession(username, password)
    r = requests.post(api_session.endpoint_url, json=api_session.get_body())
    assert expected_status_code == r.status_code


def test_create_issue():

    # login
    api_session = ApiSession(USERNAME, DECODED_PASSWORD)
    r = requests.post(api_session.endpoint_url, json=api_session.get_body())
    assert HTTPStatus.OK == r.status_code

    # create issue
    s = requests.session()
    s.cookies = r.cookies
    api_issue = ApiIssue(PROJECT_KEY, BUG_ISSUE_TYPE_KEY, "Oleg " + get_time_stamp())
    r = s.post(api_issue.endpoint_url, json=api_issue.get_body())
    assert HTTPStatus.CREATED == r.status_code
    issue_id = r.json()["id"]

    # delete created issue
    r = s.delete(api_issue.endpoint_url + "/" + issue_id)

    # logout
    r = s.delete(api_session.endpoint_url)


def test_create_issue_with_missing_required_fields():

    # login
    api_session = ApiSession(USERNAME, DECODED_PASSWORD)
    r = requests.post(api_session.endpoint_url, json=api_session.get_body())
    assert HTTPStatus.OK == r.status_code

    # create issue
    s = requests.session()
    s.cookies = r.cookies
    api_issue = ApiIssue(PROJECT_KEY, BUG_ISSUE_TYPE_KEY, "Oleg " + get_time_stamp())

    #remove a required field from body
    body_missing_fields = api_issue.get_body()
    del body_missing_fields["fields"]["summary"]

    r = s.post(api_issue.endpoint_url, json=api_issue.get_body())
    assert HTTPStatus.BAD_REQUEST == r.status_code

    # logout
    r = s.delete(api_session.endpoint_url)


def test_create_issue_with_summary_text_longer_than_supported():

    # login
    api_session = ApiSession(USERNAME, DECODED_PASSWORD)
    r = requests.post(api_session.endpoint_url, json=api_session.get_body())
    assert HTTPStatus.OK == r.status_code

    # create issue
    s = requests.session()
    s.cookies = r.cookies
    api_issue = ApiIssue(PROJECT_KEY, BUG_ISSUE_TYPE_KEY, "Z"*256)

    r = s.post(api_issue.endpoint_url, json=api_issue.get_body())
    assert HTTPStatus.BAD_REQUEST == r.status_code

    # logout
    r = s.delete(api_session.endpoint_url)





#
#
# def test_login_incorrect_password():
#     body = {'username': USERNAME, 'password': "incorrect"}
#     r = requests.post(url, json=body)
#     assert HTTPStatus.UNAUTHORIZED == r.status_code
#
#
# def test_login():
#     # print(base64.b64encode("".encode('utf-8')))
#
#     body = {'username': USERNAME, 'password': DECODED_PASSWORD}
#     r = requests.post('http://jira.hillel.it:8080/rest/auth/1/session', json=body)
#     assert HTTPStatus.OK == r.status_code
#
#     print(r.status_code)
#
#     s = requests.session()
#     s.cookies = r.cookies
#
#     r = s.get('http://jira.hillel.it:8080/rest/auth/1/session', )
#     print(r.text)
#
#     r = s.delete('http://jira.hillel.it:8080/rest/auth/1/session')
#
#     print(r)


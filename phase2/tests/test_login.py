
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


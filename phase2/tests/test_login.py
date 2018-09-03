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


@pytest.fixture(scope="module",
                params=[
                    ('incorrect', DECODED_PASSWORD, HTTPStatus.UNAUTHORIZED),
                    (USERNAME, "incorrect", HTTPStatus.UNAUTHORIZED),
                    (USERNAME, DECODED_PASSWORD, HTTPStatus.OK),
                ])
def login_fixture(request):
    yield request.param[0], request.param[1], request.param[2]
    r = requests.delete(api_session.endpoint_url)
#    smtp_connection = smtplib.SMTP(request.param, 587, timeout=5)
#    yield smtp_connection
#    print("finalizing %s" % smtp_connection)
#    smtp_connection.close()


# @pytest.mark.parametrize("username,password,expected_status_code",
#                          [
#                              ('incorrect', DECODED_PASSWORD, HTTPStatus.UNAUTHORIZED),
#                              (USERNAME, "incorrect", HTTPStatus.UNAUTHORIZED),
#                              (USERNAME, DECODED_PASSWORD, HTTPStatus.OK),
#                          ]
#                          )
def test_login_incorrect_username(login_fixture):
    api_session = ApiSession(login_fixture[0], login_fixture[1])
    r = requests.post(api_session.endpoint_url, json=api_session.get_body())
    assert login_fixture[2] == r.status_code

 # def test_login_incorrect_username(username, password, expected_status_code):
 #    api_session = ApiSession(username, password)
 #    r = requests.post(api_session.endpoint_url, json=api_session.get_body())
 #    assert expected_status_code == r.status_code
 #
 #


from http import HTTPStatus

import pytest
import requests

from src.constants import *
from src.jira_api import ApiSession


@pytest.mark.parametrize("username,password,expected_status_code",
                         [
                             ('incorrect', DECODED_PASSWORD, HTTPStatus.UNAUTHORIZED),
                             (USERNAME, "incorrect", HTTPStatus.UNAUTHORIZED),
                             (USERNAME, DECODED_PASSWORD, HTTPStatus.OK),
                         ]
                         )
def test_login(username, password, expected_status_code):
    #api_session = ApiSession()
    api_session = ApiSession(username,password)
    r = api_session.get_current_user()
    #r = requests.get(api_session.endpoint_url, auth=(username, password))
    assert expected_status_code == r.status_code

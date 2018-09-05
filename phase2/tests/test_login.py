from base64 import b64encode
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
    api_session = ApiSession()
    r = requests.get(api_session.endpoint_url, auth = (username, password))
    assert expected_status_code == r.status_code




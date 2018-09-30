from http import HTTPStatus

import pytest
import requests

from src.constants import *
from src.jira_api import ApiSession


@pytest.mark.parametrize("username,password,expected_status_code",
                         [
                             ('incorrect', decoded_password, HTTPStatus.UNAUTHORIZED),
                             (USERNAME, incorrect_password, HTTPStatus.UNAUTHORIZED),
                             (USERNAME, decoded_password, HTTPStatus.OK),
                         ]
                         )
def test_login(username, password, expected_status_code):
    api_session = ApiSession(username, password())
    r = api_session.get_current_user()
    assert expected_status_code == r.status_code

import pytest

from src.constants import *


@pytest.mark.parametrize("username,password",
                         [
                             ('incorrect', DECODED_PASSWORD),
                             (USERNAME, "incorrect"),
                         ]
                         )
def test_web_login_negative(username, password, web_test_fixture):


    assert FAILED_AUTH_ERROR_MESSAGE == err_msg


def test_web_login_positive():

    assert expected_status_code == isUserLoggedIn



import pytest
from src.page_objects.login_page import LoginPage
from src.constants import *

#
# @pytest.mark.parametrize("username,password",
#                          [
#                              ('incorrect', DECODED_PASSWORD),
#                              (USERNAME, "incorrect"),
#                          ]
#                          )
# def test_web_login_negative(username, password, driver):
#     login_page = LoginPage(driver)
#     login_page.login(username,password)
#     assert login_page.is_failed_login_error_message_exists(FAILED_AUTH_ERROR_MESSAGE)
#
#
# def test_web_login_positive(driver):
#     login_page = LoginPage(driver)
#     main_page = login_page.login(USERNAME,DECODED_PASSWORD)
#     assert main_page.is_open()
#     main_page.logout()
#     assert login_page.is_open()
#



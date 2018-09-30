import allure
import pytest
from allure_commons.types import AttachmentType

from src.page_objects.login_page import LoginPage
from src.constants import *


@pytest.mark.feature_login
@pytest.mark.parametrize("username,password",
                         [
                             ('incorrect', decoded_password),
                             (USERNAME, incorrect_password),
                         ]
                         )
def test_web_login_negative(username, password, driver):
    login_page = LoginPage(driver)
    login_page.login(username, password())
    is_failed_login_error_message_exists = login_page.is_failed_login_error_message_exists(FAILED_AUTH_ERROR_MESSAGE)
    allure.attach(driver.get_screenshot_as_png(), 'screenshot', attachment_type=AttachmentType.PNG)
    assert is_failed_login_error_message_exists


@pytest.mark.feature_login
def test_web_login_positive(driver):
    login_page = LoginPage(driver)
    main_page = login_page.login(USERNAME, decoded_password)
    main_page.wait_till_page_is_open(timeout=30)
    assert main_page.is_open()
    main_page.logout()
    assert login_page.is_open()


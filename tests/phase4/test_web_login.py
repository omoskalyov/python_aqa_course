import allure
import pytest
from allure_commons.types import AttachmentType

from src.page_objects.login_page import LoginPage
from src.constants import *


@pytest.mark.web_test1
#@allure.tag("web_test1")
@pytest.mark.parametrize("username,password",
                         [
                             ('incorrect', DECODED_PASSWORD),
                             (USERNAME, "incorrect"),
                         ]
                         )
def test_web_login_negative(username, password, driver):
    login_page = LoginPage(driver)
    login_page.login(username, password)
    allure.attach(driver.get_screenshot_as_png(), 'screenshot', attachment_type=AttachmentType.PNG)
    assert login_page.is_failed_login_error_message_exists(FAILED_AUTH_ERROR_MESSAGE)


@allure.tag("web_test2")
def test_web_login_positive(driver):
    login_page = LoginPage(driver)
    main_page = login_page.login(USERNAME, DECODED_PASSWORD)
    main_page.wait_till_page_is_open(timeout=30)
    assert main_page.is_open()
    main_page.logout()
    assert login_page.is_open()

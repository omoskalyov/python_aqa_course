import pytest
import requests
from http import HTTPStatus
from src.jira_api import ApiSession, ApiIssue
from src.constants import *


@pytest.fixture(scope="session", autouse=True)
def jira_session_fixture():

    #browsers = browser_factory(initBrowser)

    # login once per pytest session
    api_session = ApiSession()
    r = requests.get(api_session.endpoint_url, auth=(USERNAME, DECODED_PASSWORD))
    assert HTTPStatus.OK == r.status_code

    # create session in jira
    s = requests.session()
    s.cookies = r.cookies

    yield api_session, s

    # logout once the pytest session ends
    r = s.delete(api_session.endpoint_url)
    assert (HTTPStatus.OK == r.status_code) or (HTTPStatus.NO_CONTENT == r.status_code)



@pytest.fixture()
def web_tests_fixture(jira_session_fixture):

    # login
    driver = browsers.initBrowser(BROWSER)
    get_driver().get()

    setLoginPage(new
    LoginPage(getDriver()))

    yield driver

    # logout


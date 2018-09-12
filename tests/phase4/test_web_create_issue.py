import time

import pytest

from src.common import get_time_stamp
from src.page_objects.login_page import LoginPage
from src.constants import *


# def test1(web_tests_fixture):
#     time.sleep(10)
#     assert True
#
# def test2(web_tests_fixture):
#     time.sleep(10)
#     assert True


def test_create_issue(web_tests_fixture):
    main_page = web_tests_fixture
    summary = "Oleg " + get_time_stamp()
    issue_type = "Bug"
    main_page.create_issue(project=PROJECT_KEY, issue_type = issue_type, summary=summary)
    search_issue_page = main_page.open_search_page()
    found_issues_count = search_issue_page.search_issue_by_summary(summary=summary)
    assert found_issues_count == 1


def test_create_issue_with_missing_required_fields(web_tests_fixture):
    main_page = web_tests_fixture
    main_page.create_issue_with_missing_summary_field()
    assert main_page.is_error_message_exists(MISSING_SUMMARY_FIELD_ERROR_TEXT)


def test_create_issue_with_summary_text_longer_than_supported(web_tests_fixture):
    main_page = web_tests_fixture
    main_page.create_issue_with_not_supported_text_length()
    assert main_page.is_error_message_exists(FIELD_LENGTH_LIMIT_ERROR_TEXT)



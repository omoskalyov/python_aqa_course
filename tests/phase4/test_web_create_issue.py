import pytest

from src.common import get_time_stamp
from src.constants import *


@pytest.mark.feature_issue
def test_create_issue(web_tests_fixture):
    main_page, created_issues_list = web_tests_fixture

    summary = "Oleg " + get_time_stamp()
    issue_type = "Bug"
    main_page.create_issue(project=PROJECT_KEY, issue_type = issue_type, summary=summary)
    issue_id = main_page.get_created_issue_id()
    created_issues_list.append(issue_id)

    # validate created issue
    main_page.open_issue_by_id(issue_id)
    assert main_page.get_issue_summary() == summary


@pytest.mark.feature_issue
def test_create_issue_with_missing_required_fields(web_tests_fixture):
    main_page, created_issues_list = web_tests_fixture
    main_page.create_issue_with_missing_summary_field()
    assert main_page.is_error_message_exists(MISSING_SUMMARY_FIELD_ERROR_TEXT)


@pytest.mark.feature_issue
def test_create_issue_with_summary_text_longer_than_supported(web_tests_fixture):
    main_page, created_issues_list = web_tests_fixture
    main_page.create_issue_with_not_supported_text_length()
    assert main_page.is_error_message_exists(FIELD_LENGTH_LIMIT_ERROR_TEXT)


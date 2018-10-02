import pytest
from src.constants import *


@pytest.mark.feature_issue
def test_search_issue(web_tests_fixture, created_dummy_issue):
    main_page, created_issues_list = web_tests_fixture

    search_issue_page = main_page.open_search_page()
    found_issues_count = search_issue_page.search_issue_by_summary(
        summary='"' + created_dummy_issue.get_summary() + '"')
    assert found_issues_count == 1


@pytest.mark.feature_issue
def test_search_multiple_issues(web_tests_fixture, created_issues_summaries):
    main_page, created_issues_list = web_tests_fixture

    # search for multiple issues
    summaries_jql_string = " OR summary ~ ".join(['"' + x + '"' for x in created_issues_summaries])
    search_issue_page = main_page.open_search_page()
    found_issues_count = search_issue_page.search_issue_by_summary(summary=summaries_jql_string)
    assert found_issues_count == MAX_ISSUES_TO_CREATE


@pytest.mark.feature_issue
def test_search_not_existing_issue(web_tests_fixture):
    main_page, created_issues_list = web_tests_fixture
    summary = 'Not existing summary 312'
    search_issue_page = main_page.open_search_page()
    search_issue_page.search_issue_by_summary(summary='"' + summary + '"')
    assert not search_issue_page.is_search_results_list_exists()

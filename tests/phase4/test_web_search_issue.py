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


def test_search_issue(web_tests_fixture):
    main_page, created_issues_list = web_tests_fixture
    summary = 'Oleg ' + get_time_stamp()
    main_page.create_issue(project=PROJECT_KEY, issue_type = "Bug", summary=summary)
    created_issues_list.append(main_page.get_created_issue_id())
    search_issue_page = main_page.open_search_page()
    found_issues_count = search_issue_page.search_issue_by_summary(summary='"'+summary + '"')
    assert found_issues_count == 1


def test_search_multiple_issues(web_tests_fixture):
    main_page, created_issues_list = web_tests_fixture

    # create several issues
    summaries = []
    for issue_num in range(MAX_ISSUES_TO_CREATE):
        summary = "Oleg " + get_time_stamp()
        main_page.create_issue(project=PROJECT_KEY, issue_type="Bug", summary=summary)
        created_issues_list.append(main_page.get_created_issue_id())
        summaries.append(summary)
        #issue_id = r.json()["id"]
        #created_issues.append((issue_id, summary))

    # search for multiple issues
    summaries_jql_string = " OR summary ~ ".join(['"' + x + '"' for x in summaries])
    search_issue_page = main_page.open_search_page()
    found_issues_count = search_issue_page.search_issue_by_summary(summary=summaries_jql_string)
    assert found_issues_count == MAX_ISSUES_TO_CREATE


def test_not_existing_issue(web_tests_fixture):
    main_page = web_tests_fixture
    summary = 'Not existing summary 312'
    search_issue_page = main_page.open_search_page()
    search_issue_page.search_issue_by_summary(summary='"'+summary + '"')
    assert not search_issue_page.is_search_results_list_exists()



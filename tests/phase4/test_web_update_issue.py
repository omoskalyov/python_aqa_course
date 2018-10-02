import pytest
from src.constants import *


@pytest.mark.feature_issue
def test_update_issue(web_tests_fixture, created_dummy_issue):
    main_page, created_issues_list = web_tests_fixture

    # update issue
    updated_summary = created_dummy_issue.get_summary() + " updated"
    updated_priority = "High"
    main_page.open_issue_by_id(created_dummy_issue.get_key())
    main_page.open_edit_issue_dialog()
    main_page.update_issue(updated_summary, updated_priority, USERNAME)
    main_page.open_issue_by_id(created_dummy_issue.get_key())

    # validate the updated issue
    assert main_page.get_issue_summary() == updated_summary
    assert main_page.get_issue_priority() == updated_priority
    assert main_page.get_issue_assignee() == USERNAME.replace("_", " ")

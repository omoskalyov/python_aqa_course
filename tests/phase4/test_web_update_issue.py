from src.common import get_time_stamp
from src.constants import *


def test_update_issue(web_tests_fixture):
    main_page, created_issues_list = web_tests_fixture

    # create an issue
    summary = 'Oleg ' + get_time_stamp()
    main_page.create_issue(project=PROJECT_KEY, issue_type="Bug", summary=summary)
    issue_id = main_page.get_created_issue_id()
    created_issues_list.append(issue_id)

    # update issue
    updated_summary = summary + " updated"
    updated_priority = "High"
    main_page.open_issue_by_id(issue_id)
    main_page.open_edit_issue_dialog()
    main_page.update_issue(updated_summary, updated_priority, USERNAME)

    # validate the updated issue
    assert main_page.get_issue_summary() == updated_summary
    assert main_page.get_issue_priority() == updated_priority
    assert main_page.get_issue_assignee() == USERNAME.replace("_", " ")


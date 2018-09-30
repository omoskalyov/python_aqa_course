from http import HTTPStatus

from src.common import get_time_stamp
from src.jira_api import ApiIssue
from src.constants import *


def test_update_issue(api_issue_fixture, created_issues, created_dummy_issue):

    # update issue
    created_dummy_issue.set_summary("Hello")
    created_dummy_issue.set_assignee("Oleg_Moskalyov")
    created_dummy_issue.set_priority("High")
    r = created_dummy_issue.update_issue(created_issues[-1])
    assert HTTPStatus.NO_CONTENT == r.status_code

    # validate issue is updated
    r = created_dummy_issue.get_issue(created_issues[-1])
    assert HTTPStatus.OK == r.status_code
    assert r.json()["fields"]["summary"] == created_dummy_issue.get_summary()
    assert r.json()["fields"]["assignee"]["name"] == created_dummy_issue.get_assignee()
    assert r.json()["fields"]["priority"]["name"] == created_dummy_issue.get_priority()


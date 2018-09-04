from http import HTTPStatus

from src.common import get_time_stamp
from src.jira_api import ApiSession, ApiIssue, ApiSearch
from src.constants import *


def test_update_issue(jira_tests_fixture):

    api_session, s, created_issues, pass_objects_back_to_fixture = jira_tests_fixture

    # create an issue
    api_issue = ApiIssue(PROJECT_KEY, BUG_ISSUE_TYPE_KEY, "Oleg " + get_time_stamp())
    r = s.post(api_issue.endpoint_url, json=api_issue.get_body())
    assert HTTPStatus.CREATED == r.status_code
    created_issues.append(r.json()["id"])

    # update issue
    api_issue.set_summary("Hello")
    api_issue.set_assignee("Oleg_Moskalyov")
    api_issue.set_priority("High")
    r = s.put(api_issue.endpoint_url + "/" + created_issues[0], json=api_issue.get_body())
    assert HTTPStatus.NO_CONTENT == r.status_code

    # validate issue is updated
    r = s.get(api_issue.endpoint_url + "/" + created_issues[0])
    assert HTTPStatus.OK == r.status_code
    assert r.json()["fields"]["summary"] == api_issue.get_summary()
    assert r.json()["fields"]["assignee"]["name"] == api_issue.get_assignee()
    assert r.json()["fields"]["priority"]["name"] == api_issue.get_priority()

    pass_objects_back_to_fixture(api_issue, created_issues)


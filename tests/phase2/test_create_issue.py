from http import HTTPStatus

from src.common import get_time_stamp
from src.jira_api import ApiIssue

from src.constants import *


def test_create_issue(jira_tests_fixture, api_issue_fixture, created_issues):
    api_session, jira_session = jira_tests_fixture

    # create issue
    summary = "Oleg " + get_time_stamp()
    api_issue = ApiIssue(jira_session, PROJECT_KEY, BUG_ISSUE_TYPE_KEY, summary)
    api_issue_fixture.set(api_issue)
    r = api_issue.create_issue()
    assert HTTPStatus.CREATED == r.status_code
    created_issues.append(r.json()["id"])

    # validate the issue is really created
    r = api_issue.get_issue(created_issues[-1])
    assert HTTPStatus.OK == r.status_code
    assert summary == r.json()["fields"]["summary"]


def test_create_issue_with_missing_required_fields(jira_tests_fixture, api_issue_fixture):
    api_session, jira_session = jira_tests_fixture

    api_issue = ApiIssue(jira_session, PROJECT_KEY, BUG_ISSUE_TYPE_KEY, "Oleg " + get_time_stamp())
    api_issue_fixture.set(api_issue)

    # remove a required field from body
    body_missing_fields = api_issue.get_body()
    del body_missing_fields["fields"]["summary"]

    # try to create issue
    r = api_issue.create_issue()
    assert HTTPStatus.BAD_REQUEST == r.status_code
    assert MISSING_SUMMARY_FIELD_ERROR_TEXT == r.json()["errors"]["summary"]


def test_create_issue_with_summary_text_longer_than_supported(jira_tests_fixture, api_issue_fixture):
    api_session, jira_session = jira_tests_fixture

    api_issue = ApiIssue(jira_session, PROJECT_KEY, BUG_ISSUE_TYPE_KEY, SUMMARY_TEXT_LONGER_THAN_SUPPORTED)
    api_issue_fixture.set(api_issue)

    # try to create issue
    r = api_issue.create_issue()
    assert HTTPStatus.BAD_REQUEST == r.status_code
    assert FIELD_LENGTH_LIMIT_ERROR_TEXT == r.json()["errors"]["summary"]

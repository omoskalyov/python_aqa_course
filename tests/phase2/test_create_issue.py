from http import HTTPStatus

from src.common import get_time_stamp
from src.jira_api import ApiIssue

from src.constants import *


def test_create_issue(jira_tests_fixture):
    api_session, s, created_issues, pass_objects_back_to_fixture = jira_tests_fixture

    # create issue
    summary = "Oleg " + get_time_stamp()
    api_issue = ApiIssue(PROJECT_KEY, BUG_ISSUE_TYPE_KEY, summary)
    r = s.post(api_issue.endpoint_url, json=api_issue.get_body())
    assert HTTPStatus.CREATED == r.status_code
    created_issues.append(r.json()["id"])

    # validate the issue is really created
    r = s.get(api_issue.endpoint_url + "/" + created_issues[0])
    assert HTTPStatus.OK == r.status_code
    assert summary == r.json()["fields"]["summary"]

    pass_objects_back_to_fixture(api_issue, created_issues)


def test_create_issue_with_missing_required_fields(jira_tests_fixture):
    api_session, s, created_issues, pass_objects_back_to_fixture = jira_tests_fixture

    api_issue = ApiIssue(PROJECT_KEY, BUG_ISSUE_TYPE_KEY, "Oleg " + get_time_stamp())

    # remove a required field from body
    body_missing_fields = api_issue.get_body()
    del body_missing_fields["fields"]["summary"]

    # try to create issue
    r = s.post(api_issue.endpoint_url, json=api_issue.get_body())
    assert HTTPStatus.BAD_REQUEST == r.status_code
    assert MISSING_SUMMARY_FIELD_ERROR_TEXT == r.json()["errors"]["summary"]

    pass_objects_back_to_fixture(api_issue, "")


def test_create_issue_with_summary_text_longer_than_supported(jira_tests_fixture):
    api_session, s, created_issues, pass_objects_back_to_fixture = jira_tests_fixture

    api_issue = ApiIssue(PROJECT_KEY, BUG_ISSUE_TYPE_KEY, SUMMARY_TEXT_LONGER_THAN_SUPPORTED)

    # try to create issue
    r = s.post(api_issue.endpoint_url, json=api_issue.get_body())
    assert HTTPStatus.BAD_REQUEST == r.status_code
    assert FIELD_LENGTH_LIMIT_ERROR_TEXT == r.json()["errors"]["summary"]

    pass_objects_back_to_fixture(api_issue, "")


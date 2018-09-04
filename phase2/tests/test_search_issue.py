from http import HTTPStatus

from src.common import get_time_stamp
from src.jira_api import ApiIssue, ApiSearch

from src.constants import *


def test_search_one_issue(create_issue_fixture):
    api_session, s, created_issues, pass_objects_back_to_fixture = create_issue_fixture

    # create an issue
    summary = "Oleg " + get_time_stamp()
    api_issue = ApiIssue(PROJECT_KEY, BUG_ISSUE_TYPE_KEY, summary)
    r = s.post(api_issue.endpoint_url, json=api_issue.get_body())
    assert HTTPStatus.CREATED == r.status_code
    created_issues.append(r.json()["id"])

    # search for this single issue
    jql_query_prepared = JQL_QUERY + '"' + summary + '"'
    api_search = ApiSearch(jql_query_prepared, 1)
    r = s.post(api_search.endpoint_url, json=api_search.get_body())
    assert HTTPStatus.OK == r.status_code
    assert summary == r.json()["issues"][0]["fields"]["summary"]

    pass_objects_back_to_fixture(api_issue, created_issues)


def test_search_multiple_issues(create_issue_fixture):
    api_session, s, created_issues, pass_objects_back_to_fixture = create_issue_fixture

    # create several issues
    api_issue = None
    for issue_num in range(MAX_ISSUES_TO_CREATE):
        summary = "Oleg " + get_time_stamp()
        api_issue = ApiIssue(PROJECT_KEY, BUG_ISSUE_TYPE_KEY, summary)
        r = s.post(api_issue.endpoint_url, json=api_issue.get_body())
        assert HTTPStatus.CREATED == r.status_code
        issue_id = r.json()["id"]
        created_issues.append((issue_id, summary))

    # search for multiple issues
    jql_search_prepared = JQL_QUERY + " OR summary ~ ".join(['"' + x[1] + '"' for x in created_issues])
    api_search = ApiSearch(jql_search_prepared, MAX_RESULTS)
    r = s.post(api_search.endpoint_url, json=api_search.get_body())

    # validate the expected issues found
    assert HTTPStatus.OK == r.status_code
    assert r.json()["maxResults"] == MAX_RESULTS
    expected_summary_list = [x[1] for x in created_issues]
    actual_summary_list = [x["fields"]["summary"] for x in r.json()["issues"]]
    for x in expected_summary_list:
        assert (x in actual_summary_list) == True

    pass_objects_back_to_fixture(api_issue, [x[0] for x in created_issues])


def test_search_no_results(create_issue_fixture):
    api_session, s, created_issues, pass_objects_back_to_fixture = create_issue_fixture

    # create an issue
    api_issue = ApiIssue(PROJECT_KEY, BUG_ISSUE_TYPE_KEY, "Oleg " + get_time_stamp())
    r = s.post(api_issue.endpoint_url, json=api_issue.get_body())
    assert HTTPStatus.CREATED == r.status_code
    created_issues.append(r.json()["id"])

    # search for multiple issues
    jql_query_prepared = JQL_QUERY + "'not existing issue !@#$15243'"
    api_search = ApiSearch(jql_query_prepared, 1)
    r = s.post(api_search.endpoint_url, json=api_search.get_body())
    assert HTTPStatus.OK == r.status_code
    assert not(bool(r.json()["issues"]))

    pass_objects_back_to_fixture(api_issue, created_issues)


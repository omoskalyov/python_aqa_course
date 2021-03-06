from http import HTTPStatus

from src.jira_api import ApiIssue, ApiSearch

from src.constants import *


def test_search_one_issue(jira_tests_fixture, api_issue_fixture, created_dummy_issue):
    api_session, jira_session = jira_tests_fixture

    # search for a single issue
    jql_query_prepared = JQL_QUERY + '"' + created_dummy_issue.get_summary() + '"'
    api_search = ApiSearch(jira_session, jql_query_prepared, 1)
    r = api_search.search_issue()
    assert HTTPStatus.OK == r.status_code
    assert created_dummy_issue.get_summary() == r.json()["issues"][0]["fields"]["summary"]


def test_search_multiple_issues(jira_tests_fixture, api_issue_fixture, created_issues, created_issues_summaries):
    api_session, jira_session = jira_tests_fixture

    # search for multiple issues
    jql_search_prepared = JQL_QUERY + " OR summary ~ ".join(['"' + x + '"' for x in created_issues_summaries])
    api_search = ApiSearch(jira_session, jql_search_prepared, MAX_RESULTS)
    r = api_search.search_issue()

    # validate the expected issues found
    assert HTTPStatus.OK == r.status_code
    assert r.json()["maxResults"] == MAX_RESULTS
    actual_summary_list = [x["fields"]["summary"] for x in r.json()["issues"]]
    for x in created_issues_summaries:
        assert (x in actual_summary_list) == True


def test_search_no_results(jira_tests_fixture, api_issue_fixture, created_dummy_issue):
    api_session, jira_session = jira_tests_fixture

    # search for multiple issues
    jql_query_prepared = JQL_QUERY + "'not existing issue !@#$15243'"
    api_search = ApiSearch(jira_session, jql_query_prepared, 1)
    r = api_search.search_issue()
    assert HTTPStatus.OK == r.status_code
    assert not (bool(r.json()["issues"]))

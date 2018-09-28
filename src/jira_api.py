from src.constants import *
import requests

class ApiBaseClass():
    #JIRA_HOST_URL = "http://jira.hillel.it:8080"
    jira_host_url = JIRA_HOST_URL

    def get_body(self):
        return self._body


class ApiSession(ApiBaseClass):
    endpoint_url = ApiBaseClass.jira_host_url + "/rest/auth/1/session"

    _body = {
        "username": "$username",
        "password": "$password"
    }

    def __init__(self, username = "", password = ""):
        self._body["username"] = username
        self._body["password"] = password

    def get_current_user(self, username = None, password = None):
        if not username:
            username = self._body["username"]
        if not password:
            password = self._body["password"]
        return requests.get(ApiSession.endpoint_url, auth=(username, password))


class ApiIssue(ApiBaseClass):
    endpoint_url = ApiBaseClass.jira_host_url + "/rest/api/2/issue"

    _body = {
        "fields": {
            "project":
                {
                    "key": ""
                },
            "summary": "",
            "issuetype": {
                "id": ""
            },
            "assignee": {
                "name": ""
            },
            "priority": {
                "name": "Low"
            },

        }
    }

    def __init__(self, session, project_key, issuetype, summary):
        self._body["fields"]["project"]["key"] = project_key
        self._body["fields"]["issuetype"]["id"] = issuetype
        self._body["fields"]["summary"] = summary
        self.session = session

    def set_summary(self, summary):
        self._body["fields"]["summary"] = summary

    def get_summary(self):
        return self._body["fields"]["summary"]

    def set_assignee(self, assignee):
        self._body["fields"]["assignee"]["name"] = assignee

    def get_assignee(self):
        return self._body["fields"]["assignee"]["name"]

    def set_priority(self, priority):
        self._body["fields"]["priority"]["name"] = priority

    def get_priority(self):
        return self._body["fields"]["priority"]["name"]

    def create_issue(self):
        return self.session.post(ApiIssue.endpoint_url, json=self.get_body())


class ApiSearch(ApiBaseClass):
    endpoint_url = ApiBaseClass.jira_host_url + "/rest/api/2/search"

    _body = {
        "jql": "jql",
        "startAt": 0,
        "maxResults": 0,
        "fields": [
            "summary",
            "status",
            "assignee"
        ]
    }

    def __init__(self, jql, max_results):
        self._body["jql"] = jql
        self._body["maxResults"] = max_results

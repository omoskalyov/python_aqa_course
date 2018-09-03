# import json

class ApiBaseClass():
    JIRA_HOST_URL = "http://jira.hillel.it:8080"

    def get_body(self):
        return self._body


class ApiSession(ApiBaseClass):
    endpoint_url = ApiBaseClass.JIRA_HOST_URL + "/rest/auth/1/session"

    _body = {
        "username": "$username",
        "password": "$password"
    }

    def __init__(self, username, password):
        self._body["username"] = username
        self._body["password"] = password

    # def get_body(self):
    #     return self._body


class ApiIssue(ApiBaseClass):

    endpoint_url = ApiBaseClass.JIRA_HOST_URL + "/rest/api/2/issue"

    _body = {
        "fields": {
            "project":
                {
                    "key": "$key"
                },
            "summary": "$summary",
            "issuetype": {
                "id": "$id"
            },
        }
    }


    def __init__(self, project_key, issuetype, summary):
        self._body["fields"]["project"]["key"] = project_key
        self._body["fields"]["issuetype"]["id"] = issuetype
        self._body["fields"]["summary"] = summary


class ApiSearch(ApiBaseClass):

    endpoint_url = ApiBaseClass.JIRA_HOST_URL + "/rest/api/2/search"

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



    # def get_body(self):
    #     return self._body



    # _body = {
    #     "fields": {
    #         "project":
    #             {
    #                 "key": "$key"
    #             },
    #         "summary": "$summary",
    #         "description": "$description",
    #         "assignee": {
    #             "name": "$assignee"
    #         },
    #         "issuetype": {
    #             "id": "$id"
    #         },
    #         "priority": {
    #             "name": "$priority"
    #         }
    #     }
    # }


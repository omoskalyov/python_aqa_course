import base64

USERNAME = 'Oleg_Moskalyov'
DECODED_PASSWORD = base64.b64decode(b'MzI3Njg=').decode('utf-8')
PROJECT_KEY = "AQAPYTHON"
BUG_ISSUE_TYPE_KEY = "10107"
JQL_QUERY = "project = AQAPYTHON AND issuetype = Bug AND summary ~ "
SUMMARY_TEXT_LONGER_THAN_SUPPORTED = "Z" * 256
MAX_RESULTS = MAX_ISSUES_TO_CREATE = 5
MISSING_SUMMARY_FIELD_ERROR_TEXT = "You must specify a summary of the issue."
FIELD_LENGTH_LIMIT_ERROR_TEXT = "Summary must be less than 255 characters."

FAILED_AUTH_ERROR_MESSAGE = "Sorry, your username and password are incorrect - please try again."



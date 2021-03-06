"""A tool to ping JIRA for a search key and sends out a notification"""
import os
import time
import requests
from jira import JIRA

seen_issues = []

iftt_url = os.environ["iftt_url"]
jira_username = os.environ["jira_username"]
jira_password = os.environ["jira_password"]
jira_url = os.environ["jira_url"]
jira_search = os.environ["jira_search"]
ping_duration_seconds = int(os.environ["ping_duration_seconds"])

def send_notification(text):
    """Send Notification via IFTTT webhook"""
    result = requests.post(iftt_url, data={'value1': text})
    result.raise_for_status()
    print(text)


client = JIRA(jira_url, auth=(jira_username, jira_password))

while True:
    interesting_issues = client.search_issues(jira_search)

    for issue in interesting_issues:
        if issue.key in seen_issues:
            continue

        seen_issues.append(issue.key)
        MSG = None
        if issue.fields.assignee is None:
            MSG = "[%s Unassigned] %s" % (issue.key, issue.fields.summary)
        else:
            MSG = "[%s %s] %s" % (issue.key, issue.fields.assignee.displayName, issue.fields.summary)

        send_notification(MSG)
    time.sleep(ping_duration_seconds)

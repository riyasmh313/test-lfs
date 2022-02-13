#!/usr/bin/python3

import sys
import requests

JIRA_URL_RO = 'https://infoblox.atlassian.net/rest/api/3/issue/'

def jira(ticket_id, auth_token):

    headers = {
        "Authorization": "Basic "+auth_token,
        "Accept": "application/json"
    }

    try:
        url = JIRA_URL_RO+ticket_id
        response = requests.request("GET", url, headers=headers)
        if response.status_code == 200:
            print("JIRA Response: ", response.json().get('key'))
            return True
        else:
            print("JIRA error occurred: ", response.text)
            return False
    except Exception as e:
        print("JIRA Exception occurred ", str(e))
        return False

    return False


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: jira_check <JIRA TICKET ID> <JIRA TOKEN>")
        sys.exit(1)

    ticket = sys.argv[1]
    jira_token = sys.argv[2]

    ret = False
    ret = jira(ticket, jira_token)

    if ret:
        sys.exit(0)
    else:
        sys.exit(1)

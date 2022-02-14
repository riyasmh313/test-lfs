#!/usr/bin/python3

import sys
import requests

JIRA_URL_RW = 'https://infoblox.atlassian.net/rest/api/2/issue/'

def jira_comment(ticket_id, auth_token, user, event, branch, repo, pr):

    headers = {
        "Authorization": "Basic "+auth_token,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    try:
        url = JIRA_URL_RW+ticket_id+"/comment"
        data = '{"body":"user: '+user+' completed '+event+' to the branch ['+branch+'] on repo: '+repo+' using PR :'+pr+'"}'
        #data = '{"body":"user: Testing inserting a comment into JIRA"}'
        response = requests.post(url, headers=headers, data=data)
        if response.status_code in [200, 201, 202]:
            print("Posted comment onto JIRA")
            return True
        else:
            print("Failed to post comment: ", response.text)
            return False
    except Exception as e:
        print("JIRA Exception occurred ", str(e))
        return False

if __name__ == '__main__':
    if len(sys.argv) < 8:
        print("Usage: jira_comment <JIRA TICKET ID> <JIRA TOKEN> <User> <Event> <Branch> <Repo> <PR Number>")
        sys.exit(1)

    ticket = sys.argv[1]
    jira_token = sys.argv[2]
    user = sys.argv[3]
    event = sys.argv[4]
    branch = sys.argv[5]
    repo = sys.argv[6]
    pr = sys.argv[7]

    ret = False
    ret = jira_comment(ticket, jira_token, user, event, branch, repo, pr)

    if ret:
        sys.exit(0)
    else:
        sys.exit(1)

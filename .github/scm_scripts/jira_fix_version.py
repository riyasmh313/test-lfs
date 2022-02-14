#!/usr/bin/python3

import sys
import requests

JIRA_URL_RO = 'https://infoblox.atlassian.net/rest/api/3/issue/'

def jira(ticket_id, auth_token, branch):

    headers = {
        "Authorization": "Basic "+auth_token,
        "Accept": "application/json"
    }

    try:
        url = JIRA_URL_RO+ticket_id
        response = requests.request("GET", url, headers=headers)
        if response.status_code == 200:
            jd = response.json()
            fixVersions = [d['name'] for d in jd['fields']['fixVersions']]
            blist = branch.split('/')
            if len(blist) == 1:
                print("Version information not available from base branch in github")
                # TODO: Change this to False
                return True
            gitVersion = blist[1]
            present = [st for st in fixVersions if gitVersion in st]
            if len(present) == 0:
                print("JIRA Fix Version :", fixVersions, " does not match with github branch version :", branch)
                return False
            else:
                return True
        else:
            print("JIRA error occurred: ", response.text)
            return False
    except Exception as e:
        print("JIRA Exception occurred ", str(e))
        return False

    return False


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: jira_fix_version <JIRA TICKET ID> <JIRA TOKEN> <Branch>")
        sys.exit(1)

    ticket = sys.argv[1]
    jira_token = sys.argv[2]
    branch = sys.argv[3]

    ret = False
    ret = jira(ticket, jira_token, branch)

    if ret:
        sys.exit(0)
    else:
        sys.exit(1)

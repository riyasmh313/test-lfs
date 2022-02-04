#!/usr/bin/python3.8

import sys
import requests
import json

JIRA_URL = 'https://infoblox.atlassian.net/rest/api/3/issue/'
V1_URL = 'https://www10.v1host.com/InfobloxNewV1/query.v1'

def jira(ticket_id, auth_token):

    headers = {
        "Authorization": "Basic "+auth_token,
        "Accept": "application/json"
    }

    try:
        url = JIRA_URL+ticket_id
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

def jira_comment(ticket_id, auth_token, email, branch, repo):

    headers = {
        "Authorization": "Basic "+auth_token,
        "Accept": "application/json"
    }

    try:
        url = JIRA_URL+ticket_id+"/comment"
        data = "{'body': 'user: "+email+' pushed the '+branch+' to repo:'+repo+"'}"
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            print("Posted comment onto JIRA")
        else:
            print("Failed to post comment: ", response.text)
    except Exception as e:
        print("JIRA Exception occurred ", str(e))

def versionone(task_id, story_id, token):

    headers = {
        'Authorization': 'Bearer '+token,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    try:
        v1_id = ''
        if task_id:
            data = "{'from':'Task','select':['Number','Team.Name','Owners.Name'],'where':{'Number':'"+task_id+"'}}"
            v1_id = task_id

        if story_id:
            data = "{'from':'Story','select':['Number','Name','Team.Name','Owners.Name'],'where':{'Number':'"+story_id+"'}}"
            v1_id = story_id

        response = requests.post( V1_URL, headers=headers, data=data)
        if response.status_code == 200:
            d =  response.json()
            print("V1 Response: ", d)
            if d[0][0]['Number'] == v1_id:
                return True
            else:
                return False
        else:
            print("V1 error occurred: ",response.text)
    except IndexError as e:
        print("V1 ID not present")
        return False
    except Exception as e:
        print("V1 Exception occurred: ",str(e))
        return False

    return False

if __name__ == '__main__':
    if len(sys.argv) < 7:
        print("Usage: ib_check <Commit Title> <JIRA TOKEN> <V1 Token> <email> <branch> <repo>")
        sys.exit(1)

    title = sys.argv[1]
    jira_token = sys.argv[2]
    v1_token = sys.argv[3]
    email = sys.argv[4]
    branch = sys.argv[5]
    repo = sys.argv[6]

    #Check for non-ascii in The Title
    if not title.isascii():
        print("Commit title contains non-ascii characters")
        sys.exit(1)

    #Check Commit Title Format
    # NIOS-12345 : Some description
    # NIOS-12345: Some description
    ts = title.split(':')
    if len(ts) != 2:
        print("Commit Title Message format: <ticket-id>:<short description>")
        sys.exit(1)

    heads = ts[0].split(' ')
    if len(heads) > 2:
        print("Commit Title Message format: <ticket-id>:<short description>")
        sys.exit(1)

    head = heads[0]
    if len(head) < 3:
        print("Ticket ID INVALID: ", head)
        sys.exit(1)

    #Check JIRA and Version One
    cats = head.split('-')
    if len(cats) != 2:
        print("Ticket ID format: ABC-12345")
        sys.exit(1)

    ret = False
    cat = cats[0]
    if cat == 'TK':
        ret = versionone(head, None, v1_token)
    elif cat == 'B':
        ret = versionone(None, head, v1_token)
    else:
        ret = jira(head, jira_token)
        if ret:
            jira_comment(head, jira_token, email, branch, repo)

    if ret:
        sys.exit(0)
    else:
        sys.exit(1)

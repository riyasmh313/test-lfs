#!/usr/bin/python3

import sys
import requests

V1_URL = 'https://www10.v1host.com/InfobloxNewV1/query.v1'

def v1_check(task_id, story_id, token):

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
        if response.status_code in [200, 201, 202]:
            d =  response.json()
            print("V1 Response: ", d)
            if d[0][0]['Number'] == v1_id:
                return True
            else:
                print("V1 doesn't contain this ID")
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
    if len(sys.argv) < 3:
        print("Usage: versionone_check <Version Ticket ID> <V1 Token>")
        sys.exit(1)

    head = sys.argv[1]
    v1_token = sys.argv[2]

    cats = head.split('-')
    if len(cats) != 2:
        print("Ticket ID format: ABC-12345")
        sys.exit(1)

    ret = False
    cat = cats[0]
    if cat == 'TK':
        ret = v1_check(head, None, v1_token)
    else:
        ret = v1_check(None, head, v1_token)

    if ret:
        sys.exit(0)
    else:
        sys.exit(1)

#!/usr/bin/python3

import sys

def check_title(title):
    #Check for non-ascii in The Title
    if not title.isascii():
        print("Commit title contains non-ascii characters")
        sys.exit(1)

    #Check Commit Title Format
    # NIOS-12345 : Some description
    # NIOS-12345: Some description
    ts = title.split(':')
    if len(ts) < 2:
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

    print(head)
    sys.exit(0)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: title_check <Commit Title>")
        sys.exit(1)

    title = sys.argv[1]
    check_title(title)




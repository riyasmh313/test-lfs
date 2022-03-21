#!/usr/bin/python3

import sys

def check_desc(mesg):
    #Check for non-ascii in The PR desc
    if not mesg.isascii():
        print("PR Description contains non-ascii characters")
        sys.exit(1)

    print(mesg)
    sys.exit(0)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: pr_desc_check <PR Description>")
        sys.exit(1)

    desc = sys.argv[1]
    check_desc(desc)

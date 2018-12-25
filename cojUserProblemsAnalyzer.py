"""
COJ (http://coj.uci.cu) User Problems Analyzer

Inspect several aspects of a given a list of COJ users.

The list of usernames are given from the command line. Example:

    $ python cojUserProblemsAnalizer.py frankr renicom

Author: frankr@coj
"""

import urllib
import sys


def GetUsernameList():
    usernames = sys.argv[1: ]
    return usernames


def ExitWithMessage(message, status):
    print message
    sys.exit(status)


def GetUserProfileUrl(username):
    return 'http://coj.uci.cu/user/useraccount.xhtml?username=' + username


def main():
    usernames = GetUsernameList()
    if not usernames:
        ExitWithMessage("No username provided", 1)

    print 'Downloading user profiles:'
    for username in usernames:
        profileUrl = GetUserProfileUrl(username)
        print 'Downloading ' + profileUrl
        urllib.urlretrieve(profileUrl, username + '.html')


if __name__ == '__main__':
    main()

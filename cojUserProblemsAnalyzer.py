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


def WriteLine(line):
    print line
    sys.stdout.flush()


def DownloadUserProfiles(usernames):
    WriteLine('Downloading user profiles:')
    for username in usernames:
        profileUrl = GetUserProfileUrl(username)
        WriteLine(' * Downloading ' + profileUrl)
        urllib.urlretrieve(profileUrl, username + '.html')


def main():
    usernames = GetUsernameList()
    if not usernames:
        ExitWithMessage("No username provided", 1)

    DownloadUserProfiles(usernames)


if __name__ == '__main__':
    main()

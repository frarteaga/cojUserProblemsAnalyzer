"""
COJ (http://coj.uci.cu) User Problems Analyzer

Inspect several aspects of a given a list of COJ users.

The list of usernames are given from the command line. Example:

    $ python cojUserProblemsAnalizer.py frankr renicom

Author: frankr@coj
"""

import urllib.request, urllib.parse, urllib.error
import sys
from html.parser import HTMLParser


HTMLProfiles = {}
ACCProblems = {}
AttemptedProblems = {}


class CojUserProfileParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.accScope = False
        self.attemptedScope = False
        self.pickProbleId = False
        self.ACCProblems = []
        self.AttemptedProblems = []

    def handle_starttag(self, tag, attrs):
        self.pickProbleId = False
        if ('id', 'probsACC') in attrs:
            self.accScope = True
        elif ('id', 'probsWA') in attrs:
            self.accScope = False
            self.attemptedScope = True
        elif tag == 'span' and (('class', 'badge alert-success') in attrs or ('class', 'badge alert-danger') in attrs):
            self.pickProbleId = True

    def is_valid_pid(self, data):
        try:
            pid = int(data)
            if 1000 <= pid <= 9999:
                return True
            return False
        except:
            return False

    def handle_data(self, data):
        if self.pickProbleId and self.is_valid_pid(data):
            if self.accScope:
                self.ACCProblems.append(data)
            elif self.attemptedScope:
                self.AttemptedProblems.append(data)


def GetUsernameList():
    usernames = sys.argv[1: ]
    return usernames


def ExitWithMessage(message, status):
    print(message)
    sys.exit(status)


def GetUserProfileUrl(username):
    return 'http://coj.uci.cu/user/useraccount.xhtml?username=' + username


def WriteLine(line):
    print(line)
    sys.stdout.flush()


def HasProfileHtmlErrors(html):
    if not html:
        return True
    if 'COJ: Profile of' not in html:
        return True
    return False


def GetFileContent(fileName):
    try:
        File = open(fileName, 'r')
        content = File.read()
        return content
    except:
        return ''


def DownloadUserProfiles(usernames):
    WriteLine('Downloading user profiles:')

    for username in usernames:
        profileUrl = GetUserProfileUrl(username)
        profileHtmlFileName = username + '.html'

        WriteLine(' * Downloading ' + profileUrl)
        urllib.request.urlretrieve(profileUrl, profileHtmlFileName)

        html = GetFileContent(profileHtmlFileName)
        if HasProfileHtmlErrors(html):
            WriteLine('An error occured with ' + profileHtmlFileName + 
                  '. Make sure the user exist or check you internet connection')
        else:
            HTMLProfiles[username] = html
    WriteLine('')


def ExtractProblemListsFrom(htmlProfiles):
    for username in htmlProfiles:
        html = htmlProfiles[username]
        parser = CojUserProfileParser()
        parser.feed(html)
        ACCProblems[username] = set(parser.ACCProblems)
        AttemptedProblems[username] = set(parser.AttemptedProblems)

        
def PrintQuantities(usernames):
    for username in usernames:
        cACC = len(ACCProblems[username])
        cAtt = len(AttemptedProblems[username])
        print(username, 'AC:', cACC, 'Failed:', cAtt)


def main():
    usernames = GetUsernameList()
    if not usernames:
        ExitWithMessage("No username provided", 1)

    DownloadUserProfiles(usernames)
    ExtractProblemListsFrom(HTMLProfiles)
    ValidUsernames = list(HTMLProfiles.keys())
    PrintQuantities(ValidUsernames)


if __name__ == '__main__':
    main()

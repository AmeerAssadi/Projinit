import config
import sys
import os
import argparse
from github import Github, BadCredentialsException
from termcolor import colored


class GithubAccount :
    def __init__(self, username, password) :
        self.username = username
        self.password = password


def parse_args() :
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-r', '--reposiroty',
                        dest="reposiroty",
                        action="store",
                        help="Repository Name",
                        required=False)

    parser.add_argument('-u', '--username',
                        dest="username",
                        help="Github username",
                        required=False)

    parser.add_argument('-p', '--password',
                        dest="password",
                        help="Github Password",
                        required=False
                        )

    return parser.parse_args()


def getGithubAccount(account) :
    if isGithubAccountAvailableInTerminal(account) :
        return account
    else :
        return getGithubAccountFromLocalFile()


def getGithubAccountFromTerminal() :
    return GithubAccount(sys.argv[2], sys.argv[3])


def getGithubAccountFromLocalFile() :
    return GithubAccount(config.USERNAME, config.PASSWORD)


def isGithubAccountAvailableInTerminal(account) :
    if account.username is not None or account.password is not None :
        if account.username is None or account.password is None :
            print(colored("Enter account credentials", "red"))
            exit()
            return False
        else :
            return account.username != "" and account.password != ""


def printBanner() :
    print(colored('''
 /$$$$$$$  /$$$$$$$   /$$$$$$     /$$$$$ /$$$$$$ /$$   /$$ /$$$$$$ /$$$$$$$$
| $$__  $$| $$__  $$ /$$__  $$   |__  $$|_  $$_/| $$$ | $$|_  $$_/|__  $$__/
| $$  \ $$| $$  \ $$| $$  \ $$      | $$  | $$  | $$$$| $$  | $$     | $$   
| $$$$$$$/| $$$$$$$/| $$  | $$      | $$  | $$  | $$ $$ $$  | $$     | $$   
| $$____/ | $$__  $$| $$  | $$ /$$  | $$  | $$  | $$  $$$$  | $$     | $$   
| $$      | $$  \ $$| $$  | $$| $$  | $$  | $$  | $$\  $$$  | $$     | $$   
| $$      | $$  | $$|  $$$$$$/|  $$$$$$/ /$$$$$$| $$ \  $$ /$$$$$$   | $$   
|__/      |__/  |__/ \______/  \______/ |______/|__/  \__/|______/   |__/   
                                                              
''', "green"))
    print(colored("                          By: @AmeerAssadi", "red"))


def createProject(repositoryName, account) :
    # Attempts counter
    count = 1

    # Repository name
    if repositoryName is None :
        repositoryName = input("Enter Repository Name: ").strip()
        while repositoryName == "" and count != 3 :
            count = count + 1
            repositoryName = input("Enter Repository Name: ").strip()
            if repositoryName != "".strip() and count != 3 :
                break
            elif count == 3 :
                print("too many attempts")
                exit()

    user = Github(account.username, account.password).get_user()

    try :
        repo = user.create_repo(repositoryName)
    except BadCredentialsException :
        print(colored("Enter correct password", "red"))
        exit(0)

    path = "/Users/ameerma/Documents/devProjects/"

    # creating repository
    folderName = str(repositoryName)

    if not os.path.exists(path + repositoryName):
        os.makedirs(path + str(repositoryName))
    else :
        print("folder or repository with the name ({}) is exist".format(repositoryName))
        exit(0)



    # move to the repository path
    os.chdir(path + repositoryName)

    # Run git commands
    os.system('git init')
    os.system('git remote add origin git@github.com:' + account.username + '/' + repositoryName + '.git')
    os.system('touch README.md')
    os.system('git add .')
    os.system('git commit -m \'Initial commit\'')
    os.system('git push -u origin master')
    os.system('subl .')

    print("\n\nRepository '{}' Was Successfully Created ~\n".format(repositoryName))


if __name__ == "__main__" :
    # parse arguments
    repositoryName = parse_args().reposiroty
    username = parse_args().username
    password = parse_args().password

    account = getGithubAccount(GithubAccount(username, password))

    # execute the various functions
    printBanner()
    createProject(repositoryName, account)

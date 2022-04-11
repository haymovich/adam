import sys
import os
import datetime
import subprocess
from logger import logger
"""
Author@Bar Levi Haymovich
"""


# ------- # global -> outside function # ------- #
# ------- # global function -> checkOsSystem # ------- #
# ------- # global -> outside variable # ------- #
scriptName = os.path.basename(__file__)


# ------- # Class -> GitHubManager # ------- #
class GitHubManager:
    """
    - Explain :
        - Github manager that can :
            - auto basic flow for :
                - git add .
                - git commit -m "InsertMessage"
                - git push
    """

    def __init__(self):
        # ------- # Default attributes -> basic Variable # ------- #
        # ------- # Default attributes -> Names # ------- #
        # ------- # Default attributes -> Path # ------- #
        pass

    # ------- # Methods -> pushBasicToGithub # ------- #
    def sendCommandToTerminalAndGetOutpout(self, commandToSendTypeStr: str):
        """
        - Explain :
            - Send any command to terminal and return in to user as return .
        - Flag :
            - commandToSendTypeStr
                - Which command to send
        - Return:
            - return the command as is.
        """
        # work flow
        newCommandSplitter = commandToSendTypeStr.split(' ')

        return subprocess.check_output(newCommandSplitter)

 # ------- # Methods -> pushBasicToGithub # ------- #
    def getLatestTagReleaseFromGit(self):
        """
        - Explain :
            - Get the latest tag from git and release it with update.
        - Flag :
            - None
        - Return:
            - If there none any tag then add the tag to auto add tag
        """
        # work flow
        try:
            extractReleaseTag = self.sendCommandToTerminalAndGetOutpout(
                'git describe')
            if 'False' in str(extractReleaseTag):
                return 'v1.0.0'
            else:
                return str(extractReleaseTag)[2::].split('-')[0]

        except subprocess.CalledProcessError:
            logger().printLog(0, 'Auto tag has been enable , tag 1.0.0 is create now for project.')
            return False

     # ------- # Methods -> pushBasicToGithub # ------- #
    def pushBasicToGithub(self, msgToCommitTypeStr: str):
        """
        - Explain :
            - push changes to git without any flows
        - Flag :
            - msgToCommitTypeStr : str
                - What to release for github.
        - Return:
            - call the update for insert message
        """
        # work flow.
        getLatesTag = ''
        if self.getLatestTagReleaseFromGit():
            getLatesTag = str(self.getLatestTagReleaseFromGit()
                              ).replace('\n', '').replace('\\n', '').replace("'", '')
        else:
            # enable create auto tag
            getLatesTag = 'v1.0.0'
            self.createAutoTagToGit(
                rawInput='', createAutoTagWhenNoTagInGit=True)
        # ragult push to git
        subprocess.call(["git", "add", "."])
        subprocess.call(
            ["git", "commit", "-m", f"Last Release Tag -> [{getLatesTag}] | {msgToCommitTypeStr}"])
        subprocess.call(["git", "push"])

     # ------- # Methods -> createAutoTagToGit # ------- #
    def createAutoTagToGit(
            self,
            rawInput,
            tagVersion=False,
            updateFirstIndex=False,
            updateSecondIndex=False,
            updateThirdIndex=False,
            createAutoTagWhenNoTagInGit=False
    ):
        """
        - Explain :
            - release to git with basic flow
        - Flag :
            - rawInput
                - What should be in the release ?
            - tagVersion
                - This auto tag version is
        - Return:
            - call the update for insert message.
        """
        # check if needed to release tag without any iteration of the user
        print('1')
        if createAutoTagWhenNoTagInGit:
            # push any changes to git
            autoMesageToGit = f'Auto Release was create by adam framework - Date {datetime.datetime.now().strftime("%D %T")}'
            subprocess.call(
                ["git", "tag", "-a", "-m", f"{autoMesageToGit}", f"v1.0.0"])
            subprocess.call(["git", "push", "origin", f"--tags"])
            self.pushBasicToGithub('Auto Tag has been release.')
        else:
            getLatestRelease = ''
            if self.getLatestTagReleaseFromGit():
                getLatestRelease = str(
                    self.getLatestTagReleaseFromGit()).replace('v', '').replace('\\n', '').replace("'", '').split('.')

                firstIndex = int(getLatestRelease[0])
                secondIndex = int(getLatestRelease[1])
                thirdIndex = int(getLatestRelease[2])
                # first index
                if updateFirstIndex:
                    firstIndex += 1
                    thirdIndex = 0
                    secondIndex = 0
                # second index
                if updateSecondIndex:
                    secondIndex += 1
                    thirdIndex = 0
                # third index
                if updateThirdIndex:
                    thirdIndex += 1
                else:
                    thirdIndex += 1
                # init full release version
                tagVersion = f'v{firstIndex}.{secondIndex}.{thirdIndex}'
            else:
                tagVersion = 'v1.0.0'
            # Create auto tag to git
            subprocess.call(
                ["git", "tag", "-a", "-m", f"Release from adam framework - {rawInput}", f"{tagVersion}"])
            subprocess.call(["git", "push", "origin", f"--tags"])
            self.pushBasicToGithub(f'Release from tag method --> {rawInput}')


# Running only if system in this file
if __name__ == '__main__':
    logger().printLog(
        5, f'# // Script Name --> [{scriptName}]')
    # check if git inside the current folder
    logger().printLog(
        7, f'Try to search .git folder inside --> {os.getcwd()}', 'Checking', 3)
    if '.git' in os.listdir(os.getcwd()):
        logger().printLog(1, f'.git folder match --> {os.getcwd()}')

        try:
            # ------- # Caller -> -t # ------- #
            # testing
            if sys.argv[1] == '-t':
                logger().printLog(7, '==== Test Init ====')
                logger().printLog(7, '==== Test Done ====')
                pass
            # ------- # Caller -> -p # ------- #
            # push basic stuff to git
            if sys.argv[1] == '-p':
                logger().printLog(7, '==== Test Init ====')
                GitHubManager().pushBasicToGithub(sys.argv[2])
                logger().printLog(7, '==== Test Done ====')
            # ------- # Caller -> -nt # ------- #
            # new tag to github .
            if sys.argv[1] == '-nt':
                # first index == major
                if sys.argv[2][0] == '1':
                    logger().printLog(7, '==== Test Init ====')
                    logger().printLog(0, 'Init activated MAJOR release.')
                    GitHubManager().createAutoTagToGit(
                        str(sys.argv[2][1::]).strip(), updateFirstIndex=True)
                    logger().printLog(7, '==== Test Done ====')

                # second index == MINOR.
                elif sys.argv[2][0] == '2':
                    logger().printLog(0, 'Init activated MINOR release.')
                    logger().printLog(7, '==== Test Init ====')
                    GitHubManager().createAutoTagToGit(
                        str(sys.argv[2][1::]).strip(), updateSecondIndex=True)
                    logger().printLog(7, '==== Test Done ====')

                # third index == PATCH
                elif sys.argv[2][0] == '3':
                    logger().printLog(7, '==== Test Init ====')
                    logger().printLog(0, 'Init activated PATCH release.')
                    GitHubManager().createAutoTagToGit(
                        str(sys.argv[2][1::]).strip(), updateThirdIndex=True)
                    logger().printLog(7, '==== Test Done ====')

                else:
                    logger().printLog(7, '==== Test Init ====')
                    logger().printLog(0, 'Init activated PATCH release.')
                    GitHubManager().createAutoTagToGit(
                        str(sys.argv[2][1::]).strip(), updateThirdIndex=True)
                    logger().printLog(7, '==== Test Done ====')
            # ------- # Caller -> -rt # ------- #
            # delete all tags from git --> remove tag
            if sys.argv[1] == '-rt':
                pass
        except IndexError:
            pass
    # git folder not exists in the folder
    else:
        logger().printLog(
            4, f'Try to search .git folder inside --> {os.getcwd()}')

        logger().printLog(
            2, '[Error] git repo folder is not in this folder , try to run git clone from your repo and start again.')

# tempList = []
# a = git tag | xargs git tag -d
# while True:
#     tag = input('input : ')
#     tempList.append(f'git push --delete origin {tag}')
#     if tag == 'e':
#         for _ in tempList:
#             print(_)

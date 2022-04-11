#!/usr/bin/python3
"""
@Author:Bar levi haymovich - bar.levix.haymovich@intel.com
System that enable to :
    - config command for or specific user ro default user.
    - config the order for all the command
    - exec this command once or for iteration.
"""
import json
import os
import sys
import subprocess
from logger import logger

# ------- # global -> outside variable # ------- #
scriptName = os.path.basename(__file__)
pathScriptFolder = os.path.dirname(os.path.realpath(__file__))
pathScript = os.path.join(pathScriptFolder, scriptName)
dashLine = '------------------------'*2


# ------- # Class -> CommandReadWriteManager # ------- #
class CommandReadWriteManager():
    """
    - Explain :
        - Get command from user by name.
        - Build for :
            - Read the command for giving user --> if giving user is not insert --> default user will be pick
            - Write the command for giving user --> if giving user is not insert --> default user will be pick (option)
            - update the order of the command for giving user / default user.
    """

    def __init__(self, userNameFolderToExract):
        # ------- # Default attributes -> Variables # ------- #
        # while Variables
        # json Variables
        self.JsonBasicDataToWrite = {
            'command': {}}
        # ------- # Default attributes -> Names # ------- #
        # adam_command_users --> this base folder will hold all data for all command for all users.
        self.nameForBaseCommandFolder = 'adam_command_users'
        self.nameForDefaultUser = 'default_user'
        self.nameForDynamicUser = userNameFolderToExract  # what user pick for the user
        # ------- # Default attributes -> Path # ------- #
        # --> this is where the user command folder will bi store
        self.pathFolderForBaseCommandPartOne = os.getcwd()
        self.pathFolderForBaseCommandPartTwo = os.path.join(
            self.pathFolderForBaseCommandPartOne, self.nameForBaseCommandFolder)
        # sub folders
        self.pathFolderSubDynamicUser = os.path.join(
            self.pathFolderForBaseCommandPartTwo, self.nameForDynamicUser)
        self.pathFolderSubDefaultUser = os.path.join(
            self.pathFolderForBaseCommandPartTwo, self.nameForDefaultUser)
        # sub files
        self.pathFileJsonCommandDynamicUser = os.path.join(
            self.pathFolderSubDynamicUser, self.nameForDynamicUser+'.json')
        self.pathFileJsonCommandDefaultUser = os.path.join(
            self.pathFolderSubDefaultUser, self.nameForDefaultUser+'.json')

    # ------- # Methods -> initCommand # ------- #
    def initCommand(self, commandToRunTypeStr: str, silenceModeTypeBool: bool = False):
        """
        - Explain :
            - extract command
        """
        execCommand = commandToRunTypeStr
        printInfo = []
        extractCommand = str(
            subprocess.check_output(execCommand, shell=True))[1::].replace('"', '').split('\\n')
        printInfo.append(logger().printLog(
            8, f'Command [{execCommand}] Was Send.', returnTrueOrPrintFalseTypeBool=True))
        if not silenceModeTypeBool:
            for _ in printInfo:
                print(_)
        return extractCommand

    # ------- # Methods -> findAliasValue # ------- #
    def findAliasValue(self, aliasNameToFindTypeStr: str, silenceModeTypeBool=False):
        """
        - Explain :
            - find adam script path from commnad alias
        - Example :
            - Class().findAliasValue('AliasName', True) --> for not print
            - Class().findAliasValue('AliasName') --> print
        """
        # init basic var
        extractAllAlias = self.initCommand(
            'bash -i -c "alias"', silenceModeTypeBool)
        foundAliasValue = ''
        printInfo = []
        # iter each items
        for eachItem in extractAllAlias:
            if f'alias {aliasNameToFindTypeStr}=' in eachItem:
                foundAliasValue = str(eachItem).replace(
                    f'alias {aliasNameToFindTypeStr}=', '').replace("'", '').strip()
        # split the value

        printInfo.append(logger().printLog(
            0, f'Extract alias value from command [{foundAliasValue}]', returnTrueOrPrintFalseTypeBool=True))
        try:
            foundAliasValue = foundAliasValue.split(' ')[1].strip()
            printInfo.append(logger().printLog(
                1, f'Found value [{foundAliasValue}]', returnTrueOrPrintFalseTypeBool=True))
        except IndexError:
            printInfo.append(logger().printLog(
                2, 'Cannot find any value inside this alias.', returnTrueOrPrintFalseTypeBool=True))

        if not silenceModeTypeBool:
            for eachPrint in printInfo:
                print(eachPrint)
        return foundAliasValue

    # ------- # Methods -> writeDataToAnyJson # ------- #
    def writeDataToAnyJson(self, pathJsonFileToWriteTypeStr: str, dataTypeDict: dict):
        """
        - Explain :
            - write data into json file.
        - Flags :
            - pathJsonFileToWriteTypeStr :
                - Where the json file will be store ?
            - dataTypeDict :
                - What to write into the json file ?
        - return :
            - If json file is'nt exists , create it and write into it else , just write into it
        """
        # check if exists
        with open(pathJsonFileToWriteTypeStr, 'w+') as autoJsonWriter:
            json.dump(dataTypeDict, autoJsonWriter, indent=1)

    # ------- # Methods -> initBasicFolder2ndVariable # ------- #
    def initBasicSettings(self, ActivatedPathForDefaultUserTypeBool: bool = False, ActivatedPathForDynamicUserTypeBool: bool = False):
        """
        - Explain :
            - Check if the folder with the name [adam_users] is exists
        - return :
            - Full path for this json file.
        """
        # Check for base folder - exists or not
        if not os.path.exists(self.pathFolderForBaseCommandPartTwo):
            logger().printLog(2,
                              f'Folder [{self.nameForBaseCommandFolder}] not exists , create it now.')
            os.system(f'sudo mkdir {self.pathFolderForBaseCommandPartTwo}')
            os.system(f'sudo chmod 777 {self.pathFolderForBaseCommandPartTwo}')
            logger().printLog(
                1, f'Folder [{self.nameForBaseCommandFolder}] is created.')
        # check for default user
        # print(
        #     '# ------------# init check for --> [Default User] # ------------# ')
        if not os.path.exists(self.pathFolderSubDefaultUser):
            # create folder
            logger().printLog(
                2, 'Folder [Default User] not exists , create it now')
            os.system(f'sudo mkdir {self.pathFolderSubDefaultUser}')
            os.system(f'sudo chmod 777 {self.pathFolderSubDefaultUser}')
            print('[Pass] Folder [Default User] is created.')
            # create json file for this user
            self.writeDataToAnyJson(
                self.pathFileJsonCommandDefaultUser, self.JsonBasicDataToWrite)

            logger().printLog(
                1, f'Create data for user [{self.nameForDefaultUser}]')
        # Check for sub dynamic folder if exists or not
        # print(
        #     f'# ------------# init check for --> [{self.nameForDynamicUser}] # ------------# ')
        if not os.path.exists(self.pathFolderSubDynamicUser):
            # create folder
            logger().printLog(2,
                              f'User [{self.nameForDynamicUser}] not exists , create it now.')
            os.system(
                f'sudo mkdir {self.pathFolderSubDynamicUser}')
            os.system(f'sudo chmod 777 {self.pathFolderSubDynamicUser}')

            logger().printLog(
                1, f'Folder user [{self.nameForDynamicUser}] created.')
            # create json file for this user
            self.writeDataToAnyJson(
                self.pathFileJsonCommandDynamicUser, self.JsonBasicDataToWrite)
            logger().printLog(
                1, f'Create data for user [{self.nameForDynamicUser}]')
            logger().printColor(5,
                                f'# ------------# Wellcome New User [{str(self.nameForDynamicUser).capitalize()}] # ------------#')
        # check if sub default/dynamic json file is not exists
        if not os.path.exists(self.pathFileJsonCommandDynamicUser):
            # create json file for this user
            self.writeDataToAnyJson(
                self.pathFileJsonCommandDynamicUser, self.JsonBasicDataToWrite)
        if not os.path.exists(self.pathFileJsonCommandDefaultUser):
         # create json file for this user
            self.writeDataToAnyJson(
                self.pathFileJsonCommandDefaultUser, self.JsonBasicDataToWrite)
        # flags
        if ActivatedPathForDefaultUserTypeBool:
            return self.pathFileJsonCommandDefaultUser
        if ActivatedPathForDynamicUserTypeBool:
            return self.pathFileJsonCommandDynamicUser
        else:
            return self.pathFileJsonCommandDefaultUser

    # ------- # Methods -> readJsonFolderUserCommand # ------- #
    def readJsonFolderUserCommand(self, pathForJsonToReadTypeStr: str):
        pathForCommand = pathForJsonToReadTypeStr
        if not os.path.exists(pathForCommand):
            with open(pathForCommand, 'w') as readJsonFile:
                json.dump(self.testJsonAttributes, pathForCommand, indent=1)
            return self.testJsonAttributes
        else:
            with open(pathForCommand) as readJsonFile:
                jsonReader = json.load(readJsonFile)
                return jsonReader

    # ------- # Methods -> writeToJson # ------- #
    def writeToJson(self, pathForWriteToJsonTypeStr: str, commandNameInsertFromOtherMethodTypeStr: str = False):
        """
        - Explain :
            - User not need to insert any of arguments , and script has auto insert to json.
        - Return :
            - update/create the json for this user.

        """
        # init basic args
        self.initBasicSettings()
        pathForJsonUserFile = pathForWriteToJsonTypeStr
        extractDataForJsonUserJson = self.readJsonFolderUserCommand(
            pathForJsonUserFile)
        commandName = commandNameInsertFromOtherMethodTypeStr
        commnadItems = {}
        removeIndexForCounter = True
        counter = 1
        while True:

            if not commandName:
                commandName = input('Please insert your command name : ')
                if commandName != '':
                    break
            else:
                logger().printLog(
                    0, f'Auto Insert command name --> [{commandName}]')
                break
        while True:
            commandPipLine = input(
                f'What your command number [{counter}] for command [{commandName}] - insert [q] to leave | insert [fq] to leave without save : ')
            if commandPipLine == '':
                logger().printLog(2,
                                  'Cannot Add this command to pipe , command must have items.')
                if counter == 1:
                    counter = 1
                elif counter > 1:
                    if removeIndexForCounter:
                        counter -= 1

            # quit
            elif commandPipLine == 'q':
                # check if the user insert more then one value
                if len(commandPipLine) == 0:
                    logger().printLog(2,
                                      'If you want to to exit the menu you must insert at least one command , if want to exit without save --> [fq]')
                else:
                    logger().printLog(0,
                                      f'Extract Data from user -> total command insert [{len(commandPipLine)}] has insert to user personal command.')
                    break
            # force quit
            elif commandPipLine == 'fq':
                logger().printLog(0, 'Activated force quit.')
                exit(0)
            else:
                logger().printLog(0,
                                  f'\t - Sub command --> [{commandPipLine}] with run order number -> [{counter}] has insert to system, waiting for [q] to exec.')
                commnadItems[counter] = commandPipLine
                counter += 1
                removeIndexForCounter = False
        # write the data to temp variable for json
        extractDataForJsonUserJson['command'][f'{commandName}'] = commnadItems
        # write the data from the temp variable to json
        self.writeDataToAnyJson(pathForJsonUserFile,
                                extractDataForJsonUserJson)

    # ------- # Methods -> seekCommandInsideAlias # ------- #
    def seekCommandInsideAlias(self, commandToSeekTypeStr: str):
        # init basic var
        splitCommandBySpace = str(commandToSeekTypeStr).split(' ')
        commandFind = ''
        for eachCommand in splitCommandBySpace:
            findAliasValue = self.findAliasValue(eachCommand, True)
            if findAliasValue:
                # check file
                if os.path.isfile(findAliasValue):
                    commandFind = commandFind + ' ' + findAliasValue
                # check folder
                else:
                    commandFind = commandFind + ' ' + f'cd {findAliasValue}'
            else:
                commandFind = commandFind + ' ' + eachCommand
        return commandFind.strip()

    # ------- # Methods -> execCommand # ------- #
    def execCommand(self, pathForJsonCommandFileTypeStr: str, commandKeyToExecTypeStr: str):
        # init basic args
        self.initBasicSettings()
        pathForJsonUserFile = pathForJsonCommandFileTypeStr
        nameUser = os.path.basename(
            pathForJsonCommandFileTypeStr).replace('.json', '').strip()
        readJsonCommand = self.readJsonFolderUserCommand(
            pathForJsonUserFile)['command']
        commandKeyToExecCaller = commandKeyToExecTypeStr
        # print
        print(dashLine)
        logger().printColor(5,
                            f'Wellcome user [{nameUser}]')
        if self.nameForDefaultUser != nameUser:
            logger().printLog(0, 'Start pulling personal command.')
        # check if the command key is in the command to exec
        if commandKeyToExecCaller not in readJsonCommand.keys():
            logger().printLog(2,
                              f'Command [{commandKeyToExecCaller}] not in exists , activated command auto insert.')
            self.writeToJson(pathForJsonUserFile, commandKeyToExecCaller)
            self.execCommand(pathForJsonUserFile, commandKeyToExecCaller)
        else:
            print(
                f'{dashLine}')
            for commandOrder, commandValue in sorted(readJsonCommand[commandKeyToExecCaller].items()):
                commandValue = self.seekCommandInsideAlias(
                    str(commandValue).strip())

                logger().printLog(0,
                                  f'Caller Script : Init Command --> {commandOrder}.{commandValue}')
                # replace the command ll
                if 'll' in commandValue:
                    commandValue = f'{str(commandValue).replace("ll","ls -lh")}'.strip(
                    )
                    os.system(commandValue)
                # command is cd
                elif commandValue == 'cd':
                    homePath = os.path.expanduser('~')
                    os.chdir(homePath)
                    logger().printLog(
                        7, f'Current Path : {os.getcwd()}', 'Path Info', 3)
                # replace the command ll
                elif 'cd' in commandValue:
                    commandValue = f'{str(commandValue).replace("cd","")}'.strip(
                    )
                    # check if ; in command
                    if ';' in commandValue:
                        commandValueSplitter = commandValue.split(';')
                        for eachCommand in commandValueSplitter:
                            try:
                                os.chdir(eachCommand.strip())
                            except FileNotFoundError:
                                pass
                    else:
                        os.chdir(commandValue)
                    logger().printLog(
                        7, f'Current Path : {os.getcwd()}', 'Path Info', 3)
                # command is pwd
                elif 'pwd' == commandValue:
                    logger().printLog(
                        7, f'Current Path : {os.getcwd()}', 'Path Info', 3)
                else:
                    os.system(commandValue)
                print(
                    f'{dashLine}')

    # ------- # Methods -> readCommandForUser # ------- #
    def readCommandForUser(self, pathToJsonFileTypeStr: str, commandKeyToGrabTypeStr: str = False):
        # init basic var
        # init basic var
        self.initBasicSettings()
        pathForJsonUserFile = pathToJsonFileTypeStr
        readJsonCommand = self.readJsonFolderUserCommand(pathForJsonUserFile)
        commandKeyToExecCaller = commandKeyToGrabTypeStr

        if commandKeyToExecCaller:
            # check if item is inside the json file
            logger().printLog(1,
                              f'Command [{commandKeyToExecCaller}] has been found.')
            if commandKeyToExecCaller in readJsonCommand['command'].keys():
                for k, v in sorted(readJsonCommand['command'][commandKeyToExecCaller].items()):
                    print(f'\t{k}.{v}')
            else:
                logger().printLog(2,
                                  f'Command [{commandKeyToExecCaller}] not in exists , activated command auto insert.')
                self.writeToJson(pathForJsonUserFile, commandKeyToExecCaller)
                self.readCommandForUser(
                    pathForJsonUserFile, commandKeyToExecCaller)
        else:
            locationItem = []
            for n, (k, v) in enumerate(sorted(readJsonCommand['command'].items())):
                logger().printLog(0, f'Insert number [{n}] For command [{k}]')
                locationItem.append(k)
            print(dashLine)
            logger().printLog(8, '[Activated] init while loop')
            while True:
                try:
                    print(dashLine)
                    userInput = int(
                        input('[Input] Please insert your choose : '))
                    if userInput <= len(locationItem)-1:
                        logger().printLog(1,
                                          f'Command [{locationItem[userInput]}] has been found.')
                        for k, v in readJsonCommand['command'][locationItem[userInput]].items():
                            print(f'\t{k}.{v}')
                        inpContinueToRunCommand = input(
                            'Do you want to run the command from here [1=y /enter=no] : ')
                        # == ''
                        if inpContinueToRunCommand == '':
                            logger().printLog(6, 'Execration')
                            break
                        # == '1'
                        elif inpContinueToRunCommand == '1':
                            logger().printLog(0,
                                              f'[Activating] Start to activated execute command [{locationItem[userInput]}]')
                            self.execCommand(pathForJsonUserFile,
                                             locationItem[userInput])
                            break
                    else:
                        logger().printLog(2,
                                          f'\tCommand number [{userInput}] is not exists in system.')

                except ValueError as e:
                    logger().printLog(2,
                                      '\tYou must insert command number for check what it hold.')

    # ------- # Methods -> updateCommand # ------- #
    def updateCommand(self, pathToJsonFileTypeStr: str, commandKeyToGrabTypeStr: str):
        # init basic var
        self.initBasicSettings()
        pathForJsonUserFile = pathToJsonFileTypeStr
        readJsonCommand = self.readJsonFolderUserCommand(
            pathForJsonUserFile)
        commandKeyToExecCaller = commandKeyToGrabTypeStr
        changeNewCommandInput = ''
        lastCommandOrderNumber = ''
        existsCommandDataTypeDict = {}
        # check if the command is empty or not
        if commandKeyToExecCaller not in readJsonCommand['command'].keys():
            logger().printLog(2,
                              f'Command [{commandKeyToExecCaller}] not in exists , activated command auto insert.')
            self.writeToJson(pathForJsonUserFile, commandKeyToExecCaller)
            self.updateCommand(pathForJsonUserFile, commandKeyToExecCaller)
        else:
            print(
                f'# -------------- # Start Section 1 --> Update/Remove command caller [{commandKeyToExecCaller}] # -------------- #')
            print(
                f'Current command name for calling is [{commandKeyToExecCaller}].\n'
                'For Changing hit [c]\n'
                'For Removing hit [r]\n'
                'For Ignoring hit [p]\n'
                f'{dashLine}'
            )
            # change or remote the command name caller
            while True:
                userInput = input(str('Please insert your chose [c/r/p] : '))
                # == c
                if userInput == 'c':
                    while True:
                        changeNewCommandInput = input(
                            f'[Input] Please insert your new call for command [{commandKeyToExecCaller}] : ')
                        # == ''
                        if changeNewCommandInput == '':
                            logger().printLog(2, 'Cannot accept empty new command')
                        else:
                            logger().printLog(1,
                                              f'Change the command [{commandKeyToExecCaller}] to new command caller [{changeNewCommandInput}]')
                            # extract old values
                            commandValuesFromDict = readJsonCommand['command'][commandKeyToExecCaller]
                            # remove old key from the list
                            readJsonCommand['command'].pop(
                                commandKeyToExecCaller)
                            # write new key with exists value
                            commandKeyToExecCaller = changeNewCommandInput
                            readJsonCommand['command'][commandKeyToExecCaller] = commandValuesFromDict
                            self.writeDataToAnyJson(
                                pathForJsonUserFile, readJsonCommand)
                            break
                        break
                    break
                # == r
                if userInput == 'r':
                    # remove old key from the lis
                    readJsonCommand['command'].pop(
                        commandKeyToExecCaller)
                    self.writeDataToAnyJson(
                        pathForJsonUserFile, readJsonCommand)
                    logger().printLog(1,
                                      f'Successful remove key [{commandKeyToExecCaller}] from user command')
                    exit(0)
                # == p
                if userInput == 'p':
                    logger().printLog(6,
                                      f'Ignoring changing for command caller [{commandKeyToExecCaller}]')
                    break
                # not both
                else:
                    logger().printLog(2, 'You must insert [c/r/p]')
            # section 2
            print(
                f'# -------------- # Start Section 2 --> Update/Remove sub command from [{commandKeyToExecCaller}] # -------------- #')

            # exists command insert data to variable
            print(
                '[Info]  You about to insert while loop editor.\n'
                '\tInsert [q]  for [quit with saving]\n'
                '\tInsert [fq] for [quit without saving]\n'
                '\tInsert [n]  for [add new command]\n'
                '\tInsert [c]  for [change exists command]\n'
                f'{dashLine}'
            )
            logger().printLog(0,
                              f'Total of [{len(readJsonCommand["command"][commandKeyToExecCaller])}] has been found.')
            existsCommandDataTypeDict = readJsonCommand['command'][commandKeyToExecCaller]
            for commandOrder, commandValue in sorted(readJsonCommand['command'][commandKeyToExecCaller].items()):
                lastCommandOrderNumber = int(commandOrder)+1
                logger().printLog(0,
                                  f'\tInsert [{commandOrder}] for sub command [{commandValue}]')
            while True:
                userInput = str(
                    input('[Input] Please insert command to edit [q/fq/n/c] : '))
                # == ''
                if userInput == '':
                    logger().printLog(2, '\tYou must insert command number')
                # == 'fq'
                elif userInput == 'fq':
                    logger().printLog(0,
                                      '\t[Activated] Force quit mode , quiting without saving.')
                    exit(0)
                # == 'q'
                elif userInput == 'q':
                    logger().printLog(
                        0, '\t[Activated] Quit mode , quiting with saving.')
                    # write data to json
                    readJsonCommand['command'][commandKeyToExecCaller] = existsCommandDataTypeDict
                    self.writeDataToAnyJson(
                        pathForJsonUserFile, readJsonCommand)
                    break
                # == 'n'
                elif userInput == 'n':
                    logger().printLog(0,
                                      f'\t[Activated] new command number [{lastCommandOrderNumber}] inside sub command')
                    logger().printLog(8, '\t[Activated] init while loop')
                    while True:
                        newCommandInput = input(
                            '[Input] what the new command do you want to insert : ')
                        if newCommandInput == '':
                            logger().printLog(2,
                                              '\tCommand cannot insert as empty str.')
                        else:
                            existsCommandDataTypeDict[str(
                                lastCommandOrderNumber)] = newCommandInput
                            logger().printLog(1,
                                              f'\tUpdate new command [{newCommandInput}] with number of execution [{lastCommandOrderNumber}]')
                            lastCommandOrderNumber += 1
                            logger().printLog(0, 'Exit while loop.')
                            # write data to json
                            readJsonCommand['command'][commandKeyToExecCaller] = existsCommandDataTypeDict
                            self.writeDataToAnyJson(
                                pathForJsonUserFile, readJsonCommand)
                            break
                # == 'c'
                elif userInput == 'c':
                    logger().printLog(8, '\t[Activated] init while loop')
                    while True:
                        userInput = str(
                            input('[Input] What the command number that you want to manupulated [hit q for leave] : '))
                        # check if the user insert command from the list
                        if userInput in existsCommandDataTypeDict.keys():
                            newCommand = str(
                                input('[Input] re-insert exists command : '))
                            # == ''
                            if newCommand == '':
                                logger().printLog(2, '\tCommand cannot be empty')
                            # != ''
                            elif newCommand != '':
                                logger().printLog(1,
                                                  f'\tUpdate commnad [{existsCommandDataTypeDict[userInput]}] with new command [{newCommand}]')

                                existsCommandDataTypeDict[userInput] = newCommand
                                readJsonCommand['command'][commandKeyToExecCaller] = existsCommandDataTypeDict
                                # write the new data to command
                                self.writeDataToAnyJson(
                                    pathForJsonUserFile, readJsonCommand)
                            elif newCommand == 'q':
                                logger().printLog(1,
                                                  'Exit command re-mange and exec command')
                                break
                            break
                        else:
                            logger().printLog(2,
                                              f'\tCommand number is not exists inside the command list')
            # exec the command
            logger().printLog(0,
                              f'Exit configuration section for command [{commandKeyToExecCaller}].')
            print(dashLine)
            self.execCommand(pathForJsonUserFile, commandKeyToExecCaller)


if __name__ == '__main__':
    logger().printLog(
        5, f'# // Script Name --> [{scriptName}]')
    os.system(f'sudo chmod 777 {pathScript}')
    try:
        # ------------------ # Dynamic User # ------------------ #
        # command read for dynamic user --> command.py cur <User> <Command>
        if sys.argv[1] == '-cru':
            """
            - Explain :
                - dynamic user can read their command
            - Syntax :
                - command.py -cru <User>
            - Name :
                - cru == command read user
            """
            # extract the user name
            dynamicUser = str(sys.argv[2]).strip()
            if dynamicUser == '':
                dynamicUser = CommandReadWriteManager(
                    '').nameForDefaultUser
            pathForJsonDynamicUser = CommandReadWriteManager(
                dynamicUser).pathFileJsonCommandDynamicUser
            # extract the command from the user
            try:
                """
                - Explain :
                    - default user can read their command without question what command to read
                - Syntax :
                    - command.py -cr <Command>
                - Name :
                    - cr == command read
                """
                extractCommand = str(sys.argv[3]).strip()
                CommandReadWriteManager(dynamicUser).readCommandForUser(
                    pathForJsonDynamicUser, extractCommand)
            except IndexError:
                """
                - Explain :
                    - default user can read their command with question what command to read
                - Syntax :
                    - command.py -cr <Command>
                - Name :
                    - cr == command read
                """
                CommandReadWriteManager(dynamicUser).readCommandForUser(
                    pathForJsonDynamicUser)
        # -cu : command user
        if sys.argv[1] == '-cu':
            """
            - Explain :
                - any user can read/write there personal command for the system
            - Syntax :
                - command.py -cu <User> <Command>
            - Name :
                - cu == command user
            """
            # extract the user name
            dynamicUser = str(sys.argv[2]).strip()
            if dynamicUser == '':
                dynamicUser = CommandReadWriteManager(
                    '').nameForDefaultUser
            # call the init method for activated all the checks
            CommandReadWriteManager(dynamicUser).initBasicSettings(
                ActivatedPathForDynamicUserTypeBool=True)
            # extract user json file to dynamic
            pathForJsonDynamicUser = CommandReadWriteManager(
                dynamicUser).pathFileJsonCommandDynamicUser
            # extract the command from the user
            try:
                # change/remote command for this user
                if sys.argv[3] == '-change':
                    """
                    - Explain :
                        - dynamic user can manage their command by Removing/update the command caller
                        - dynamic user can manage their sub command by updating the command their wanted or removing them
                    - Syntax :
                        - command.py -cu <User> -change <Command>
                    - Name :
                        - change == change command
                    """
                    extractCommand = str(sys.argv[4]).strip()
                    logger().printLog(0,
                                      f'Pick Method [Change Command] for command [{extractCommand}] to user [{dynamicUser}]')
                    CommandReadWriteManager(
                        dynamicUser).updateCommand(pathForJsonDynamicUser, extractCommand)
                # run exists command/write new command coomand for this user
                else:
                    """
                    - Explain :
                        - run command for dynamic user as usual
                    - Syntax :
                        - command.py -cu <User> <Command>
                    """
                    extractCommand = str(sys.argv[3]).strip()
                    logger().printLog(0,
                                      f'Pick Method [Exec Exists / write new command] for command [{extractCommand}] to user [{dynamicUser}]')
                    CommandReadWriteManager(
                        dynamicUser).execCommand(pathForJsonDynamicUser, extractCommand)

            except IndexError:
                logger().printLog(2,
                                  'You must insert command for activated all methods')
                exit(0)
        # ------------------ # Default User # ------------------ #
        # command for default user --> command.py c <Command>
        if sys.argv[1] == '-c':
            # if user did not enter any key --> he want to do other script from this
            defaultUser = CommandReadWriteManager('').nameForDefaultUser
            CommandReadWriteManager(defaultUser).initBasicSettings(
                ActivatedPathForDefaultUserTypeBool=True)
            # extract user json file to dynamic
            pathForJsonDefaultUser = CommandReadWriteManager(
                defaultUser).pathFileJsonCommandDefaultUser
            # extract the command from the user
            try:
                if sys.argv[2] == '-change':
                    """
                        - Explain :
                            - default user can manage their command by Removing/update the command caller
                            - default user can manage their sub command by updating the command their wanted or removing them
                        - Syntax :
                            - command.py -c <User> -change <Command>
                        - Name :
                            - change == change command
                    """
                    extractCommand = str(sys.argv[3]).strip()
                    logger().printLog(0,
                                      f'Pick Method [Change Command] for command [{extractCommand}] to user [{defaultUser}]')
                    CommandReadWriteManager(
                        defaultUser).updateCommand(pathForJsonDefaultUser, extractCommand)
                else:
                    extractCommand = str(sys.argv[2]).strip()
                    logger().printLog(0,
                                      f'Pick Method [Exec Exists / write new command] for command [{extractCommand}] to user [{defaultUser}]')
                    CommandReadWriteManager(defaultUser).execCommand(
                        pathForJsonDefaultUser, extractCommand)

            except IndexError:
                logger().printLog(2,
                                  'You must insert command for activated all methods')
                exit(0)
        # command read for default user --> command.py cr <Command>
        if sys.argv[1] == '-cr':
            """
            - Explain :
                - default user can read their command
            - Syntax :
                - command.py -cr
            - Name :
                - cr == command read
            """
            # if user did not enter any key --> he want to do other script from this
            defaultUser = CommandReadWriteManager('').nameForDefaultUser
            CommandReadWriteManager(defaultUser).initBasicSettings(
                ActivatedPathForDefaultUserTypeBool=True)
            # extract user json file to dynamic
            pathForJsonDefaultUser = CommandReadWriteManager(
                defaultUser).pathFileJsonCommandDefaultUser
            # extract the command from the user
            try:
                """
                - Explain :
                    - default user can read their command without question what command to read
                - Syntax :
                    - command.py -cr <Command>
                - Name :
                    - cr == command read
                """
                extractCommand = str(sys.argv[2]).strip()
                CommandReadWriteManager(defaultUser).readCommandForUser(
                    pathForJsonDefaultUser, extractCommand)
            except IndexError:
                """
                - Explain :
                    - default user can read their command with question what command to read
                - Syntax :
                    - command.py -cr <Command>
                - Name :
                    - cr == command read
                """
                CommandReadWriteManager(defaultUser).readCommandForUser(
                    pathForJsonDefaultUser)

    # default user
    except IndexError:
        logger().printLog(2, 'Error')

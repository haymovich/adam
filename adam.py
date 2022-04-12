#!/usr/bin/python3
from fileinput import filename
from scripts_files.logger import logger
import subprocess
from pprint import pprint
import pkg_resources
import sys
import json
import os
import datetime
import re
"""
Author@Bar Levi Haymovich
"""

# ------- # global -> outside variable # ------- #
scriptNameAdam = os.path.basename(__file__)
flagArgumentsHelp = {}
printLine = '# =================================================================== #'
check = u'\u2705'
pathScriptFolder = os.path.dirname(os.path.realpath(__file__))
pathScript = os.path.join(pathScriptFolder, scriptNameAdam)
flagArgumentsHelp = {}


# adam flag helper variable
# adamFrameworkHelpFlag
# ------- # global -> outside function # ------- #
# ------- # Function -> extractDataFromListToAutoAlias # ------- #
def extractDataFromListToAutoAlias(listType: list):
    returnValue = ''
    for _ in listType:
        returnValue = returnValue + ' ' + _
    return returnValue.strip()


# ------- # Function -> gotoAdamFolder # ------- #
def gotoAdamFolder():
    os.chdir(pathScriptFolder)
    logger().printLog(0, f'Goto --> Current Folder : {os.getcwd()}')


# ------- # Function -> argumentsHelpLocal # ------- #
def argumentsHelpLocal(
    argumentScriptNameTypeStr: str,
    argumentPathForScriptFolderTypeStr: str,
    argumentInterpertorNameTypeStr: str,
    argumentNameCallTypeStr: str,
    argumentExplainTypeStr: str,
    argumentSysArgsNeedTypeBool: bool,
    argumentQuickExample: str = False,
):
    """
    - Explain :
        - Helper to understand the script needed arguments for user.
    - Flags :
        - argumentNameCallTypeStr :
            - What the arguments needed to be ? for example -h/-p
        - argumentExplainTypeStr :
            - simple explain on how the arguments work.
        - argumentSysArgsNeedTypeBool :
            - is arguments need to give any data after the args.
        - argumentQuickExample :
            - How to use with this example ? 
    - Return :
        - Get a variable for dict and update
    """
    # global
    global flagArgumentsHelp
    # init basic var
    nowTime = datetime.datetime.now().strftime("%d-%m-%Y__%H-%M-%S")
    # check if the variable "flagArgumentsHelp" is empty or not
    if not flagArgumentsHelp:
        flagArgumentsHelp[str(argumentScriptNameTypeStr)] = {
            'path': str(argumentPathForScriptFolderTypeStr),
            'interpertor': str(argumentInterpertorNameTypeStr),
            "flags": {}}
    try:
        # manipulate data inside the var "flagArgumentsHelp"
        flagArgumentsHelp[str(argumentScriptNameTypeStr)]['flags'][f"{str(argumentNameCallTypeStr)}"] = {
            "flagName": str(argumentExplainTypeStr),
            "dateUpdateForFlag": nowTime,
            "sysArgsNeed": str(argumentSysArgsNeedTypeBool),
            "QuickExample": str(argumentQuickExample)
        }
    except KeyError:
        flagArgumentsHelp[str(argumentScriptNameTypeStr)] = {
            'path': str(argumentPathForScriptFolderTypeStr),
            'interpertor': str(argumentInterpertorNameTypeStr),
            "flags": {}}
        flagArgumentsHelp[str(argumentScriptNameTypeStr)]['flags'][f"{str(argumentNameCallTypeStr)}"] = {
            "flagName": str(argumentExplainTypeStr),
            "dateUpdateForFlag": nowTime,
            "sysArgsNeed": str(argumentSysArgsNeedTypeBool),
            "QuickExample": str(argumentQuickExample)
        }


# ------- # global function -> checkOsSystem # ------- #
def checkOsSystem():
    """
    Explain :\n
        check the type of os
    Retrun :
        return type os
    """
    if sys.platform == "linux" or sys.platform == "linux2":
        return 'linux'

    elif sys.platform == "darwin":
        return 'mac'

    elif sys.platform == "win32":
        return 'windows'


# ------- # Caller -> Call function before the class started # -------#
argumentsHelpLocal(
    scriptNameAdam,
    pathScript,
    'python3',
    '-i',
    'install adam folder and mapping',
    False,
    'adam.py -i'
)
argumentsHelpLocal(
    scriptNameAdam,
    pathScript,
    'python3',
    '-f',
    'force install adam folder and mapping',
    False,
    'adam.py -f'
)
argumentsHelpLocal(
    scriptNameAdam,
    pathScript,
    'python3',
    '-h',
    'Read all item inside the adam libray with filter for only show the name file/folder.',
    False,
    'adam.py -h'
)
argumentsHelpLocal(
    scriptNameAdam,
    pathScript,
    'python3',
    '-cts',
    'Copy and file to script folder , just insert the file name and adam will insert realpath of this script.',
    False,
    'adam.py -cts FileName'
)
argumentsHelpLocal(
    scriptNameAdam,
    pathScript,
    'python3',
    '-su',
    'Update/create exists flag inside system -> call the script with wanted flag and args , sw will auto insert/update.',
    True,
)
argumentsHelpLocal(
    scriptNameAdam,
    pathScript,
    'python3',
    '-a',
    'Create auto alias from adam framework',
    True,
    'adam.py -a <AliasName> <AliasValue>'
)


# ------- # Class -> Installer # ------- #
class Installer():
    """
    Explain :\n
        Install deafult folders, files, for system.
            Folder :
                app,
                email,
                scripts,
                json_files,
                logs
            Files :
                diary.json -> hold the basic attributes for system.
    """

    def __init__(self):
        # ------- # Default attributes -> basic Variable # ------- #
        self.nowTime = datetime.datetime.now().strftime("%d-%m-%Y__%H-%M-%S")
        self.varDiaryJson = {
            'folderMap': {},
            'folderMapLevel2': {},
            'installDate': self.nowTime,
            'initWrite': False,
            'pipList': ['paramiko']
        }

        # ------- # Default attributes -> Names # ------- #
        self.nameBasicFolderToCreate = [
            'scripts_files',
            'json_files',
            'adam_files'
        ]
        self.nameDiaryJson = 'diary.json'
        # ------- # Default attributes -> Path # ------- #
        self.pathAdamScript = os.path.dirname(os.path.realpath(__file__))

        self.fullPathDiaryJsonFile = os.path.join(
            self.pathAdamScript, 'adam_files', self.nameDiaryJson)

    # ------- # Methods -> initBasicFolder2ndVariable # ------- #
    def initBasicFolder2ndVariable(self):
        """
        Explain :
            Create the default system folder
        Flag :
            None
        Return:
            Folder exists -> Ignore.
            Folder not exists -> Create the folder.
        """

        # check missing folder and create them if needed.
        logger().printLog(
            8, f'Basic variable and checking missing folders')
        basicFolder = self.pathAdamScript
        # install the folder first
        for eachNewFolderToCreate in self.nameBasicFolderToCreate:
            fullPathForCreateEachFolder = os.path.join(
                basicFolder, eachNewFolderToCreate)
            # check missing folder :
            if not os.path.exists(fullPathForCreateEachFolder):
                os.mkdir(fullPathForCreateEachFolder)
                logger().printLog(
                    1, f'Create missing folder [{eachNewFolderToCreate}].')
        # mapping starting for each folder
        for eachFolder in os.listdir(self.pathAdamScript):
            if '.' in eachFolder:
                pass
            else:
                fullPathToEachFolder = os.path.join(basicFolder, eachFolder)
                # add path that for find to diary variable :
                self.varDiaryJson['folderMap'][eachFolder] = {
                    'mainPathFolder': fullPathToEachFolder,
                    'subFilesFolder': {}}
                logger().printLog(
                    0, f'insert folder [{eachFolder}] to diary file.')

    # ------- # Methods -> diaryInitStepOne # ------- #
    def diaryInitStepOne(self, forceWrite=False):
        """
        Explain :
            - Step One :
                - Start the diary file with all needed item inside it.
                - Mapping all folders, subfolders, and files in the project dir.
                - Write diary file with all changes.
            - Step Two :
                - Recap all item inside the 'folderMapLevel2' key and reconfig them.
                - Change the structure of how look file and file
        Flag :
            None
        Return:
            None
        """
        global parentDir

        # iterate each key inside the diary keys :
        self.initBasicFolder2ndVariable()
        logger().printLog(8, 'Diary settings and checking for missing values.')
        checkSubFolderPrint = set()
        for eachKey in self.varDiaryJson['folderMap'].keys():
            fullPathEachKey = self.varDiaryJson['folderMap'][eachKey]['mainPathFolder']
            # go each root, dirs,files in the key path
            parentDir = os.path.dirname(fullPathEachKey)
            for root, dirs, files in os.walk(fullPathEachKey, topdown=True):
                newRoot = ''
                # check type of os
                if checkOsSystem() == 'mac' or checkOsSystem() == 'linux':
                    newRoot = str(root).replace(parentDir, '').split('/')[1::]
                if checkOsSystem() == 'windows':
                    newRoot = str(root).replace(parentDir, '').split('\\')[1::]
                # start loop for each item
                for num, eachFolderName in enumerate(newRoot):
                    if num == 0:
                        rawPath = os.path.join(parentDir, eachFolderName)
                        # added the folder name (global folder name) to level 2 mapping
                        self.varDiaryJson['folderMapLevel2'][eachFolderName] = rawPath
                        if rawPath in checkSubFolderPrint:
                            pass
                        else:
                            parantNewPath = os.path.basename(rawPath)
                            self.varDiaryJson['folderMap'][str(
                                parantNewPath)]['subFilesFolder'][f'{rawPath}'] = [file for file in os.listdir(rawPath)]
                            # added each sub folder or each sub file to level 2 mapping
                            listdirForRawPath = os.listdir(rawPath)
                            # check if any file is in raw path to prevent looping
                            if listdirForRawPath:
                                for eachSubFile in os.listdir(rawPath):
                                    pathFullEachSubFile = os.path.join(
                                        rawPath, eachSubFile)
                                    # added found map file to diary file
                                    self.varDiaryJson['folderMapLevel2'][eachSubFile] = pathFullEachSubFile

                            checkSubFolderPrint.add(rawPath)
                    else:
                        rawPath = os.path.join(rawPath, eachFolderName)
                        if rawPath in checkSubFolderPrint:
                            pass
                        else:
                            # added each sub folder or each sub file to level 2 mapping
                            listdirForRawPath = os.listdir(rawPath)
                            # check if any file is in raw path to prevent looping
                            if listdirForRawPath:
                                for eachSubFile in os.listdir(rawPath):
                                    pathFullEachSubFile = os.path.join(
                                        rawPath, eachSubFile)
                                    # added found map file to diary file

                                    self.varDiaryJson['folderMapLevel2'][eachSubFile] = pathFullEachSubFile
                            self.varDiaryJson['folderMap'][str(
                                parantNewPath)]['subFilesFolder'][f'{rawPath}'] = [file for file in os.listdir(rawPath)]
                            checkSubFolderPrint.add(rawPath)
        # check if diary is exists and not need to rewrite
        jsonReader = self.diaryRead()
        if jsonReader:
            if jsonReader['initWrite']:
                # :flag : forceWrite
                if forceWrite:
                    logger().printLog(7, 'Force json write', 'Activated')
                    self.varDiaryJson['initWrite'] = True
                    self.jsonWrite(self.varDiaryJson,
                                   self.fullPathDiaryJsonFile)
                    logger().printLog(0, 'Exists diary json file.')
                    self.diaryInitStepTwo()
                    self.diaryInitStepThree()

                else:
                    logger().printLog(
                        2, 'initWrite Value is True, Enable forceWrite args or change value to false..')
            else:
                # update the diary json file
                self.varDiaryJson['initWrite'] = True
                self.jsonWrite(self.varDiaryJson, self.fullPathDiaryJsonFile)
                logger().printLog(0, 'Exists diary json file.')
                self.diaryInitStepTwo()
                self.diaryInitStepThree()
        else:
            # create the diary json file
            self.varDiaryJson['initWrite'] = True
            self.jsonWrite(self.varDiaryJson, self.fullPathDiaryJsonFile)
            logger().printLog(0, 'New diary json file.')
            self.diaryInitStepTwo()
            self.diaryInitStepThree()

        self.installerLog(finalPrint=False)

    # ------- # Methods -> diaryInitStepTwo # ------- #
    def diaryInitStepTwo(self):
        """
        Explain :
            - Step One :
                - Start the diary file with all needed item inside it.
                - Mapping all folders, subfolders, and files in the project dir.
                - Write diary file with all changes.
            - Step Two :
                - Recap all item inside the 'folderMapLevel2' key and reconfig them.
                - Change the structure of how look file and file

        Flag :
            None
        Return:
            None
        """
        # init basic var
        readJsonFileRaw = self.diaryRead()
        pathLogShowOnlyMappingFiles = os.path.join(
            readJsonFileRaw['folderMapLevel2']['logs'], 'LogType_showOnly_MappingFiles.json')

        dataToInsertToLogShowOnly = {}
        # looping all variable inside the json item
        for k, v in readJsonFileRaw['folderMapLevel2'].items():
            # revel the type of file -> script / folder / txt
            checkTypeOfFile = str(k).split('.')
            if len(checkTypeOfFile) > 1:
                # json or txt pass type
                if checkTypeOfFile[1] == 'json' or checkTypeOfFile[1] == 'txt':
                    pass
                # in mean script
                else:
                    # check if the script have .py in the end to check if this script is python script
                    InterpertorMatchToPython = ''
                    if str(k).endswith('.py'):
                        InterpertorMatchToPython = 'python3'
                    # change structure for this script
                    readJsonFileRaw['folderMapLevel2'][k] = {
                        'path': v,
                        'interpertor': InterpertorMatchToPython,
                        'flags': {}
                    }
                    # change structure for this script --> git_manager.py
                    if k == 'git_manager.py':
                        argumentsHelpLocal(
                            k,
                            v,
                            'python3',
                            '-p',
                            'push to git automatic with the last know tag -> recommending when using git work flow.',
                            True,
                            'adam git -p <What do push>'
                        )
                        argumentsHelpLocal(
                            k,
                            v,
                            'python3',
                            '-nt',
                            'automatic release new tag to git [1=MAJOR/2=MINOR/3=PATCH --> release] -> recommending when using git work flow.',
                            True,
                            'adam -nt <Type Of Push == 1/2/3> <What the release value>'
                        )
                        readJsonFileRaw['folderMapLevel2'][k] = flagArgumentsHelp[k]
                    # change structure for this script --> command.py
                    if k == 'command.py':
                        argumentsHelpLocal(
                            k,
                            v,
                            'python3',
                            '-c',
                            'Execute command.',
                            True,
                            'adam -c <AnyCommand>'
                        )
                        argumentsHelpLocal(
                            k,
                            v,
                            'python3',
                            '-c -change',
                            'Execute command.',
                            True,
                            'adam -c -change <AnyCommand>'
                        )
                        argumentsHelpLocal(
                            k,
                            v,
                            'python3',
                            '-cr',
                            'Read the command.',
                            False,
                            'adam -cr <Command Name To Read>'
                        )
                        argumentsHelpLocal(
                            k,
                            v,
                            'python3',
                            '-cu',
                            'Run Command from specific user.',
                            True,
                            'adam -cu <UserName> <CommandToExec>'
                        )
                        argumentsHelpLocal(
                            k,
                            v,
                            'python3',
                            '-cru',
                            'Read Command from specific user.',
                            True,
                            'adam -cru <UserName> <CommandToRead>'
                        )
                        readJsonFileRaw['folderMapLevel2'][k] = flagArgumentsHelp[k]
                    # change structure for this script --> createAliasForAdamFramework.py
                    if k == 'createAliasForAdamFramework.py':
                        # add args to outside variable
                        argumentsHelpLocal(
                            k,
                            v,
                            'python3',
                            '-p',
                            'Get the path for adam script , this step is automatic.',
                            True,
                            'adam createAliasForAdamFramework.py -p <PathForAdamFolder>'
                        )
                        argumentsHelpLocal(
                            k,
                            v,
                            'python3',
                            '-a',
                            'Insert new alias from adam framework -> Alias name && Alias Value.',
                            True,
                            'adam createAliasForAdamFramework.py -a <AliasName> <Alias Value>'
                        )

                        # add insert data to json file to read
                        readJsonFileRaw['folderMapLevel2'][k] = flagArgumentsHelp[k]

        # add data to logShowOnlyForMapping
        readJsonFileRaw['folderMapLevel2'][scriptNameAdam] = flagArgumentsHelp[scriptNameAdam]
        # write the changes inside the diary file
        self.jsonWrite(readJsonFileRaw, self.fullPathDiaryJsonFile)

    # ------- # Methods -> diaryInitStepTwo # ------- #
    def diaryInitStepThree(self):
        """
        Explain :
            - Step One :
                - Start the diary file with all needed item inside it.
                - Mapping all folders, subfolders, and files in the project dir.
                - Write diary file with all changes.
            - Step Two :
                - Recap all item inside the 'folderMapLevel2' key and reconfig them.
                - Change the structure of how look file and file
            - Step Three :
                - extract all items inside the 'folderMapLevel2' and create alias for each item that is there.

        Flag :
            None
        Return:
            None
        """
        # init basic var
        readJsonFileRaw = self.diaryRead()['folderMapLevel2']
        self.autoAliasForAdam(InsertDefaultAdamAlias=True)
        for k, v in readJsonFileRaw.items():
            # ignore file
            if '__pycache__' in k or '.DS_Store' in k:

                logger().printLog(6, f'[{k}]')
            # check for folder
            elif type(v) == str:
                aliasName = k
                aliasValue = v
                logger().printLog(1,
                                  f'Matching folder name [{v}] --> init alias --> {aliasName}="{aliasValue}"')
                # init alias writer
                self.autoAliasForAdam(
                    insertDynamicNameAliasTypeStr=aliasName, insertDynamicValueAliasTypeStr=aliasValue)
            # check for file
            elif type(v) == dict:
                aliasName = k
                aliasValue = v['path']
                logger().printLog(1,
                                  f'Matching file name [{aliasName}] --> init alias {aliasName}="{aliasValue}"')
                # init alias writer
                self.autoAliasForAdam(
                    insertDynamicNameAliasTypeStr=aliasName, insertDynamicValueAliasTypeStr=aliasValue)

    # ------- # Methods -> autoAliasForAdam # ------- #
    def autoAliasForAdam(self, insertDynamicNameAliasTypeStr: str = False, insertDynamicValueAliasTypeStr: str = False, InsertDefaultAdamAlias: str = False):
        # default alias
        if InsertDefaultAdamAlias:
            logger().printLog(0, 'Init auto adam alias')
            pathAdamScript = f'python3 {os.path.join(self.pathAdamScript, scriptNameAdam)}'
            callAutoAliasScript = f'{pathAdamScript} createAliasForAdamFramework.py -p {pathAdamScript}'
            os.system(callAutoAliasScript)
        # dynamic alias
        if insertDynamicNameAliasTypeStr and insertDynamicValueAliasTypeStr:
            logger().printLog(
                5, f'Extract Alias Name  [{insertDynamicNameAliasTypeStr}]')
            logger().printLog(
                5, f'Extract Alias Value [{insertDynamicValueAliasTypeStr}]')
            pathAdamScript = f'python3 {os.path.join(self.pathAdamScript, scriptNameAdam)}'
            callAutoAliasScript = f"{pathAdamScript} createAliasForAdamFramework.py -a [{insertDynamicNameAliasTypeStr}]-[{insertDynamicValueAliasTypeStr}]"
            os.system(callAutoAliasScript)

    # ------- # Methods -> diaryRead # ------- #
    def diaryRead(self):
        """
        Explain :
            Read the diary file and return dict with diary data.

        Flag :
            None

        Return:
            json exists -> False.
            Json not exists -> dict
        """
        if not os.path.exists(self.fullPathDiaryJsonFile):
            return False
        else:
            with open(self.fullPathDiaryJsonFile, 'r') as readJson:
                return json.load(readJson)

    # ------- # Methods -> jsonWrite # ------- #
    def jsonWrite(self, jsonDataToWriteTypeDict, pathWhereJsonFileIsTypePath):
        """
        Explain :
            Write into json file with 'w' option.
        Flag :
            :jsonDataToWriteTypeDict : dict = json dict data
                what to write inside of json file ?
            :pathWhereJsonFileIsTypePath : str/path
                where the json file is located ?
        Return:
            new data inside the json file
        """
        with open(pathWhereJsonFileIsTypePath, 'w') as initBasicDiaryJsonFile:
            json.dump(
                jsonDataToWriteTypeDict,
                initBasicDiaryJsonFile,
                indent=2)
        logger().printLog(7, 'Writing data to diary file', 'Writing Data', 3)

    # ------- # Methods -> installerLog # ------- #
    def installerLog(self, finalPrint=False):
        """
        Explain :
            Show the status for action happend in code
        Flag :
            :finalPrint : bool -> [Default] : False
                True : show the install process print to user.
        Return:
            print for all action
        """
        if finalPrint:
            for eachRow in self.installSetupsPrintTypeDict['installProcess']['actionToPrint']:
                print(eachRow)

    # ------- # Methods -> info # ------- #
    def getSpaces(self, maximumSpacesTypeInt: int, wordToCalcTypeStr: str):
        # init basic args
        lenWord = maximumSpacesTypeInt - int(len(str(wordToCalcTypeStr)))
        spacesToReturn = ' '*lenWord
        # return the spaces
        return spacesToReturn

     # ------- # Methods -> flagReaderBasicPrintHelper # ------- #
    def flagReaderBasicPrintHelper(self, printFullDialog=False, printOnlyNamedDialog=False):
        """
        - Explain :
            - Enable to read all flags avaliable from the diary json file.
        - Flag :
            - None
        - Return :
            - Print all the avaliable flags.
        """
        # init basic vars
        readJsonFile = self.diaryRead()
        counter = 1
        spacerMaxInt = 20
        dictPrintLogCollector = {
            'script': [],
            'folder': []
        }
        # iter all items inside mapping level 2
        for eachKeyRaw, eachValueRaw in readJsonFile['folderMapLevel2'].items():
            # check which item has data type of dict --> meaning that this key is file
            if type(eachValueRaw) == dict:
                # checking for missing interpreter and missing flags
                mappingKeys = [k for k in eachValueRaw.keys()]
                # init basic vars
                interpertorKey = mappingKeys[1]
                flagKey = mappingKeys[2]
                pathSubScript = mappingKeys[0]
                fullPathSubScript = eachValueRaw[pathSubScript]

                # check missing interpertor
                if eachValueRaw[interpertorKey] != '':
                    # check if this script has any flags
                    allSubFlagKeysInsideScriptN = eachValueRaw[flagKey].keys(
                    )
                    if len(allSubFlagKeysInsideScriptN) > 0:
                        for eachFlagKey, eachFlagValue in eachValueRaw[flagKey].items():
                            # init basic vars
                            flagCall = eachFlagKey
                            flagName = eachFlagValue['flagName']
                            lastUpdateTimeForThisFlag = eachFlagValue['dateUpdateForFlag']
                            argsNeeded = eachFlagValue['sysArgsNeed']
                            argsNeededWordArgs = ''
                            fullScriptNameCaller = ''
                            quickExample = eachFlagValue['QuickExample']
                            # key == the script name
                            if eachKeyRaw == scriptNameAdam:
                                fullScriptNameCaller = str(
                                    eachKeyRaw).replace('.py', '')
                                # args variable is True
                                if argsNeeded:
                                    argsNeededWordArgs = '[Args Need]'
                                # update Vars
                                recommendedCall = f'{scriptNameAdam.replace(".py","")} {flagCall} {argsNeededWordArgs}'

                            # key != the script name
                            if eachKeyRaw != scriptNameAdam:
                                fullScriptNameCaller = f'{eachKeyRaw}'
                                # args variable is True
                                if argsNeeded:
                                    argsNeededWordArgs = '[Args Need]'
                                  # update Vars
                                recommendedCall = f'{scriptNameAdam.replace(".py","")} {eachKeyRaw} {flagCall} {argsNeededWordArgs}'

                            # update vars
                            fullScriptNameCaller = f'{fullScriptNameCaller} {flagCall} {argsNeededWordArgs}'
                            # add the print to the list
                            dictPrintLogCollector['script'].append(
                                f'{logger().printColor(1,fullScriptNameCaller)} :'
                                f'\n\t- Flag Name{self.getSpaces(spacerMaxInt,"Flag Name")}|     {flagName}'
                                f'\n\t- Interpreter{self.getSpaces(spacerMaxInt,"Interpreter")}|     {eachValueRaw[interpertorKey]}'
                                f'\n\t- Update Time{self.getSpaces(spacerMaxInt,"Update Time")}|     {lastUpdateTimeForThisFlag}'
                                f'\n\t- script Path{self.getSpaces(spacerMaxInt,"script Path")}|     {fullPathSubScript}'
                                f'\n\t- Sys Args{self.getSpaces(spacerMaxInt,"Sys Args")}|     {argsNeeded}'
                                f'\n\t- Full call{self.getSpaces(spacerMaxInt,"Full call")}|     {eachValueRaw[interpertorKey]} {fullPathSubScript} {flagCall} {argsNeededWordArgs}'
                                f'\n\t- Code Show{self.getSpaces(spacerMaxInt,"Code Show")}|     {quickExample}'
                                f'\n\t- {logger().printColor(5,"Recommend call")}{self.getSpaces(spacerMaxInt,"Recommend call")}|     {logger().printColor(5,recommendedCall)}')
                    # if not missing interprtor && no flag
                    if len(allSubFlagKeysInsideScriptN) == 0:
                        pathForScriptForInterpreterButNonFlag = eachValueRaw['path']
                        interpertorValueForNonFlag = eachValueRaw['interpertor']
                        recommendedCall = f'{scriptNameAdam.replace(".py","")} {eachKeyRaw}'
                        dictPrintLogCollector['script'].append(
                            f'{logger().printColor(1,eachKeyRaw)} : '
                            f'\n\t- {logger().printColor(3,"Flag Exists")}{self.getSpaces(spacerMaxInt,"Flag Exists")}|     {logger().printColor(3,"False")}'
                            f'\n\t- Interpreter{self.getSpaces(spacerMaxInt,"Interpreter")}|     {interpertorValueForNonFlag}'
                            f'\n\t- Script Path{self.getSpaces(spacerMaxInt,"script Path")}|     {pathForScriptForInterpreterButNonFlag}'
                            f'\n\t- {logger().printColor(5,"Recommend call")}{self.getSpaces(spacerMaxInt,"Recommend call")}|     {logger().printColor(5,recommendedCall)}'
                        )
                else:
                    # __Any__ ignore
                    if '__' in eachKeyRaw:
                        pass
                    else:
                        # .pyc ignore or diary.json
                        if str(eachKeyRaw).endswith('.pyc'):
                            pass
                        else:
                            pathForScript = eachValueRaw['path']
                            dictPrintLogCollector['script'].append(
                                f'{logger().printColor(1,eachKeyRaw)} : '
                                f'\n\t- Flag Exists{self.getSpaces(spacerMaxInt,"Flag Exists")}|     {logger().printColor(3,"False")}'
                                f'\n\t- script Path{self.getSpaces(spacerMaxInt,"script Path")}|     {pathForScript}'
                                f'\n\t- Recommend call{self.getSpaces(spacerMaxInt,"Recommend call")}|     python3 {os.path.join(self.pathAdamScript, scriptNameAdam)} {eachKeyRaw}'
                            )
            else:
                # __Any__ ignore
                if '__' in eachKeyRaw or 'diary.json' in eachKeyRaw:
                    pass
                else:
                    # init basic var
                    pathForFolder = eachValueRaw
                    recommendedCall = f' c{os.path.basename(pathForFolder)}'
                    # add item to dict
                    dictPrintLogCollector['folder'].append(f'{logger().printColor(1,eachKeyRaw)} : '
                                                           f'\n\t- folder Path{self.getSpaces(spacerMaxInt,"folder Path")}|      {pathForFolder}'
                                                           f'\n\t- {logger().printColor(5,"Recommend call")}{self.getSpaces(spacerMaxInt,"Recommend call")}|     {logger().printColor(5,recommendedCall)}'

                                                           )

                counter += 1

        if printOnlyNamedDialog:
            print(logger().printColor(0, f'{printLine}'))
            for k, _ in dictPrintLogCollector.items():
                logger().printLog(7, k, 'Match Type')
                for n, eachItem in enumerate(sorted(dictPrintLogCollector[k]), start=1):
                    logger().printLog(7, eachItem, '', False, False)
                    print('---------------------------------------------------')
            print(logger().printColor(0, f'{printLine}'))

    # ------- # Methods -> installerLog # ------- #
    def scriptVersion(self, scriptNameTypeStr: str):
        """
        Explain :
            Grab from diary file the script version
        Flag :
            :scriptNameTypeStr : str -> [Default] : None
                what is script name to extract ?
        Return:
            str(script version)
        """
        readDiaryJsonFile = self.diaryRead()['versions'][str(
            scriptNameTypeStr)]['VersionNumber']

        return readDiaryJsonFile

    # ------- # Methods -> installerLog # ------- #
    def scriptVersionUpdate(
        self,
        scriptNameTypeStr: str,
        firstIndexToUpdateTypeBool: bool = False,
        SecondIndexToUpdateTypeBool: bool = False,
        ThirdIndexToUpdateTypeBool: bool = False,
    ):
        """
        Explain :
            Update the script version to desirable script name.\n
            Syntax for script is :
            -> v1.2.3
            -> FirstIndex = 1
            -> SecondIndex = 2
            -> ThirdIndex = 3
        Flag :
            :scriptNameTypeStr : str -> [Default] : None
                How  the script  is call ?

            :firstIndexToUpdateTypeBool : bool -> [Default] : None
                Add index +1 to first Index -> 1 --> 2

            :SecondIndexToUpdateTypeBool : bool -> [Default] : None
                Add index +1 to second Index -> 2 --> 3

            :ThirdIndexToUpdateTypeBool : bool -> [Default] : None
                Add index +1 to first Index -> 3 --> 4
        Return:
            str(script version)
        """
        # init basic variable
        ############# setup --> reset counter --> Start #############
        self.installSetupEditor(
            msg=f'',
            resetCounter=True)
        ############# setup --> reset counter --> End #############
        ############# setup --> typeInstallProcess --> Start #############
        self.installSetupEditor(
            msg=f'Mapping Folder Script Version.',
            typeInstallProcess=True)
        ############# setup --> typeInstallProcess --> Start  #############
        pathForScriptVersionFolderMain = self.diaryRead(
        )['folderMap']['script_version']['mainPathFolder']
        listdirForFolderscriptVersion = os.listdir(
            pathForScriptVersionFolderMain)
        scriptNameTypeStrNewName = scriptNameTypeStr.split('.')[0]
        # check if folder exists inside script version with script name
        if scriptNameTypeStrNewName in listdirForFolderscriptVersion:
            ############# setup --> typePass --> Start #############
            self.installSetupEditor(
                msg=f'Folder [{scriptNameTypeStr}] Already in script version folder.',
                typePass=True)
            ############# setup --> typePass --> End #############
        if scriptNameTypeStrNewName not in listdirForFolderscriptVersion:
            os.mkdir(os.path.join(pathForScriptVersionFolderMain,
                     scriptNameTypeStrNewName))
            ############# setup --> typeCreate --> Start #############
            self.installSetupEditor(
                msg=f'Folder [{scriptNameTypeStr}] in script version folder.',
                typeCreate=True)
            ############# setup --> typeCreate --> End #############
        # print setup results
        self.installerLog(finalPrint=True)

    # ------- # Methods -> findLocationFromAlias # ------- #
    def findLocationFromAlias(self, aliasNameTypeStr: str):
        """
        Explain :
            extract the path from alias name
        """
        # init basic var
        # run commnad
        def initCommand(commandToRunTypeStr: str):
            execCommand = commandToRunTypeStr
            extractCommand = str(
                subprocess.check_output(execCommand, shell=True))[1::].replace('"', '').split('\\n')
            return extractCommand
        # find adam script path from commnad alias

        # init basic var
        extractAdamScriptPath = initCommand('bash -i -c "alias"')
        foundAdamPathFromAlias = ''
        # iter each items
        for eachItem in extractAdamScriptPath:
            if aliasNameTypeStr in eachItem:
                foundAdamPathFromAlias = str(eachItem).replace(
                    f'alias {aliasNameTypeStr}=', '').replace("'", '').strip()
        return foundAdamPathFromAlias

    # ------- # Methods -> findLocationFromAlias # ------- #
    def copyFilesToScriptsFolder(self, fileThatWantToCopyTypeStr: str):
        """
        Explain :
            copy files to script folder
        """
        # init basic var
        extractScriptFolder = os.path.join(
            os.getcwd(), self.nameBasicFolderToCreate[0])
        fileNameExtract = os.path.basename(fileThatWantToCopyTypeStr)
        initCopy = True
        # check if the file is exists
        logger().printLog(
            7, f'Check if file [{fileThatWantToCopyTypeStr}] is exists.', 'Checking')
        if os.path.exists(fileThatWantToCopyTypeStr):
            # check if the file is in the script folder
            logger().printLog(
                7, f'Check if file [{fileNameExtract}] is in scripts_folder.', 'Checking')
            for dirs, folder, files in os.walk(extractScriptFolder):
                if fileNameExtract in files:
                    for eachFile in files:
                        # if file is already inside the script
                        if eachFile == fileNameExtract:
                            logger().printLog(
                                7, f'File [{eachFile}] is already in script folder , ', 'Duplication Error', 2)
                            askUserToReplace = input(
                                logger().printLog(7, f'Please approve this transaction by hit [1 to pass] / [Any other key to ignore] :', 'User Input', 1, returnTrueOrPrintFalseTypeBool=True))
                            # pass
                            if askUserToReplace == '1':
                                initCopy = True
                            else:
                                initCopy = False
                                logger().printLog(
                                    6, f'For copy file [{fileNameExtract}]')

            if initCopy:
                commandToCopy = f'sudo cp -r {fileThatWantToCopyTypeStr} {extractScriptFolder}'
                logger().printLog(8, f'Command [{commandToCopy}]')
        else:
            logger().printLog(
                2, f'File [{fileThatWantToCopyTypeStr}] is not exists , copy will no be made.')

    # ------- # Methods -> copyLoggerToSystem # ------- #
    def copyLoggerToSystem(self):
        """
        Explain :
            copy the logger.py to systemFolder
        """
        # function
        def findOsPath():
            osPath = imp.find_module('os')[1]
            return osPath
        # init basic var
        pathOsModule = str(findOsPath()).replace('os.py', '').strip()
        loggerFileLocation = self.findLocationFromAlias('f_logger')
        loggerPathForLibraryFolder = os.path.join(pathOsModule, 'logger.py')
        # copy the logger to where python hold
        os.system(f'cp -r {loggerFileLocation} {pathOsModule}')
        # change the privilage for logger file
        os.system(f'chmod 777 {loggerPathForLibraryFolder}')
        print(pathOsModule)

    # ------- # Methods -> installPipLibrary # ------- #
    def runningOsCommand(self, commandToRunTypeStr: str, silenceInstallTypeBool: bool = False):
        """
        - Explain :
            - Running any os command that user need
        - Flags :
            - commandToRunTypeStr :
                - what command run ?
            - silenceInstallTypeBool :
                - True --> Show the information on the screen
                - False --> install but without any output
        """
        # init basic args :
        commandToRunVar = str(commandToRunTypeStr)
        # check if user want it in silence
        if silenceInstallTypeBool:
            logger().printLog(
                7, f'Silence mode.', 'Activated', 4)
            commandToRunVar = f'{commandToRunVar} >/dev/null 2>&1'
        # run the command
        os.system(commandToRunVar)
        logger().printLog(
            1, f'Command [{commandToRunTypeStr}] was sent.')

    # ------- # Methods -> installPipLibrary # ------- #
    def installPipLibrary(self):
        """
        Explain :
            check for missing libray that need to be install - python only.
        Flag :
            None
        Return:
            for each pip item in the diary list , system will install them.
        """
        # init basic var
        grabList = self.diaryRead()['pipList']

        logger().printLog(8, 'Init checker for python libray.')

        for librayCheckingExists in grabList:
            logger().printLog(
                0, f'Start to install libray [{librayCheckingExists}].')
            self.runningOsCommand(f'pip3 install {librayCheckingExists}', True)

    def finalResults(
        self,
        forceCreateDiaryInitTypeBool: bool = False
    ):
        """
        Explain :
            main caller for all needed method to install the system

        Flags :
        """
        logger().printLog(
            7, f'#-----------------# Start Installetion #-----------------#')
        if forceCreateDiaryInitTypeBool:
            logger().printLog(5, 'Activated Mode -> Update diary file')
            # init diary settings and checking for missing files and values && init the basic variable and cheking missing folder:
            self.diaryInitStepOne(forceWrite=True)
        if not forceCreateDiaryInitTypeBool:
            # init diary settings and checking for missing files and values && init the basic variable and cheking missing folder:
            self.diaryInitStepOne()
        # checking missing libray :
        self.installPipLibrary()
        # init user command :
        self.runningOsCommand('python3 -m pip install --upgrade pip', True)
        # show print to user :
        # self.installerLog(finalPrint=True)
        logger().printLog(
            7, f'#-----------------# End Installetion #------------------#')


# ------- # Class -> Interpertor # ------- #
class Interpertor(Installer):
    """
    - Explain :\n
        - Ability to call any script from this script by just his name --> adam.py git -r
        - Create or update whithing this script all argument need to wanter script

    """

    def __init__(self):
        super().__init__()
        pass
        # ------- # Default attributes -> basic Variable # ------- #
        # ------- # Default attributes -> Names # ------- #
        # ------- # Default attributes -> Path # ------- #

    # ------- # Methods -> askUserInput # ------- #
    def askUserInput(
            self,
            msg: str,
            expectTypeInputOfStringTypeBool: bool = False,
            expectTypeInputOfIntegerTypeBool: bool = False,
            expectTypeInputTrueOrFalse: bool = False,
    ):
        """
        - Explain :
            - Ask user any input , when need to interact with while loop
        - Flag :
            - msg :
                - When should be ask the user ?
            - expectTypeInputOfStringTypeBool :
                - When system will ask user input , the input need to be string only
            - expectTypeInputOfStringTypeBool :
                - When system will ask user input , the input need to be Integer only
            - expectTypeInputTrueOrFalse :
                - When system will ask user input , the input need to be True or False Only
        - Return:
            - user input
        """
        # Checking
        if expectTypeInputTrueOrFalse:
            msg = msg + '[1 For True / 0 For False]'

        while True:
            inp = input(f'{msg} ')
            if expectTypeInputOfIntegerTypeBool:
                try:
                    return int(inp)
                except ValueError:
                    print('error , Should be only intger type , try again.')
            if expectTypeInputOfStringTypeBool:
                return str(inp)
            if expectTypeInputTrueOrFalse:
                if inp == '0':
                    return False
                if inp == '1':
                    return True
                else:
                    print('\tPlease insert 0 or 1 only.')

    # ------- # Methods -> seekFlags # ------- #
    def seekFlags(
            self,
            sysArgsFromUserTypeList: list,
            seekFlagsOnlyTypeBool: bool = False,
            seekArgsOnlyTypeBool: bool = False,
    ):
        """
        - Explain :
            - Get list for all argument that user insert and seek all flags that user insert with synatx -Flag and return with the order user insert.
        - Flag :
            - sysArgsFromUserTypeList :
                - All Args that user insert -> list
        - Return:
            - True -> Match flag and return str with flag order
            - False -> Not one match for flag
        """
        # init basic vars
        flagFounds = ''
        argsFounds = ''
        # start checking
        for eachItem in sysArgsFromUserTypeList:
            searcher = re.findall(re.compile('^-'), eachItem)
            if searcher:
                flagFounds = f'{flagFounds} {eachItem}'
            if not searcher:
                argsFounds = f'{argsFounds} {eachItem}'
        # seekFlagsOnlyTypeBool
        if seekFlagsOnlyTypeBool:
            if flagFounds:
                return [True, flagFounds.strip()]
            else:
                return [False]
        # seekArgsOnlyTypeBool
        if seekArgsOnlyTypeBool:
            if argsFounds:
                return[True, argsFounds.strip()]
            else:
                return [False]

    # ------- # Methods -> seekFlags # ------- #
    def callerHandlerInterpertor(
            self,
            scriptNameTypeStr: str
    ):
        """
        - Explain :
            - Manage all interpertor for giving script
        - Flag :
            - scriptNameTypeStr :
                - All Args that user insert -> list
        - Return:
            - True -> Match flag and return str with flag order
            - False -> Not one match for flag
        """
        # init basic vars
        readJsonFileSubRead = self.diaryRead()
        # start checking
        # start to check missing interpertor
        if readJsonFileSubRead['folderMapLevel2'][scriptNameTypeStr]['interpertor'] == '':
            # ask user input
            getUserinterpertorToCreate = self.askUserInput(f'\tWhen should the interpertor should be for script [{scriptNameTypeStr}] ?',
                                                           expectTypeInputOfStringTypeBool=True)
            # insert the input inside of the json
            readJsonFileSubRead['folderMapLevel2'][scriptNameTypeStr]['interpertor'] = getUserinterpertorToCreate
            # write the new data to json
            self.jsonWrite(readJsonFileSubRead, self.fullPathDiaryJsonFile)
            # return only the interpertor fort this script
            return readJsonFileSubRead['folderMapLevel2'][scriptNameTypeStr]['interpertor']
        # if the interpertor for this file is not ''
        if readJsonFileSubRead['folderMapLevel2'][scriptNameTypeStr]['interpertor'] != '':
            # return only the interpertor fort this script
            return readJsonFileSubRead['folderMapLevel2'][scriptNameTypeStr]['interpertor']

    # ------- # Methods -> seekFlags # ------- #
    def callerHandlerFlags(
            self,
            scriptNameTypeStr: str,
            wantedFlagToReadTypeStr: str,
            updateFlagTypeList: list = False,
    ):
        """
        - Explain :
            - manage all the flags for scripts, it's mean that this method is checker, create and update if needed.
        - Flag :
            - scriptNameTypeStr :
                - How the script call ?
            - searchFlagTypeStr :
                - search if this flag is in the flag section inside the script section.
            - updateFlagTypeList :
                - to update the wanted flag.
                - Needed giving list like this ['OldFlag' , 'NewFlag']
            - createFlagTypeBool :
                - Create flag for script.
        - Return:
            - List -> ['Results for test - True/False']
        """
        # init basic vars
        readJsonFile = self.diaryRead()

        # ------- # Sub Methods -> updateExistsFlag # ------- #
        def updateExistsFlag():
            # init basic vars
            readJsonFileSubRead = self.diaryRead()
            # check first if flag exists in the system
            if checkExistsFlagInSystemSubFunction(autoReturnForOutsideFunctionTypeBool=False):
                # dashLine('Menu : updateExistsFlag')
                # ask user input.
                getUserInputNewFlagMainCaller = self.askUserInput(f'\tWhat will be the new flag insert of old flag :  [{wantedFlagToReadTypeStr}] ?',
                                                                  expectTypeInputOfStringTypeBool=True)
                getUserInputFlagName = self.askUserInput(f'\tWhat the name for flag [{getUserInputNewFlagMainCaller}] ?',
                                                         expectTypeInputOfStringTypeBool=True)
                getUserInputFlagArgsNeeded = self.askUserInput(f'\tDid need call args for [{scriptNameTypeStr} {getUserInputNewFlagMainCaller}] ?',
                                                               expectTypeInputTrueOrFalse=True)
                # remove the old data from the json
                readJsonFileSubRead['folderMapLevel2'][scriptNameTypeStr]['flags'].pop(
                    wantedFlagToReadTypeStr)
                # insert the input inside of the json
                readJsonFileSubRead['folderMapLevel2'][scriptNameTypeStr]['flags'][getUserInputNewFlagMainCaller] = {
                    'flagName': getUserInputFlagName,
                    'dateUpdateForFlag': self.nowTime,
                    'sysArgsNeed': getUserInputFlagArgsNeeded}

                # write the new data to json
                self.jsonWrite(readJsonFileSubRead, self.fullPathDiaryJsonFile)
                # return only the check if args needed for
                return getUserInputFlagArgsNeeded
            if not checkExistsFlagInSystemSubFunction(autoReturnForOutsideFunctionTypeBool=False):
                logger().printLog(2,
                                  f'Flag {wantedFlagToReadTypeStr} is just insert into system, try to re-insert this flag again.')
                exit(0)

        # ------- # Sub Methods -> createNewFlag # ------- #
        def createNewFlag():
            # dashLine('Menu : createNewFlag')
            # init basic vars
            readJsonFileSubRead = self.diaryRead()
            # ask user input
            getUserInputFlagName = self.askUserInput(f'\tWhat the name for flag [{wantedFlagToReadTypeStr}] ?',
                                                     expectTypeInputOfStringTypeBool=True)
            getUserInputFlagArgsNeeded = self.askUserInput(f'\tDid need call args for [{scriptNameTypeStr} {wantedFlagToReadTypeStr}] ?',
                                                           expectTypeInputTrueOrFalse=True)
            # insert the input inside of the json
            readJsonFileSubRead['folderMapLevel2'][scriptNameTypeStr]['flags'][wantedFlagToReadTypeStr] = {
                'flagName': getUserInputFlagName,
                'dateUpdateForFlag': self.nowTime,
                'sysArgsNeed': getUserInputFlagArgsNeeded}

            # write the new data to json
            self.jsonWrite(readJsonFileSubRead, self.fullPathDiaryJsonFile)
            # return only the check if args needed for
            return readJsonFileSubRead

        # ------- # Sub Methods -> checkExistsFlagInSystemSubFunction # ------- #
        # basic check - check if the flag exists in the system
        def checkExistsFlagInSystemSubFunction(autoReturnForOutsideFunctionTypeBool: bool = True):
            # init basic vars
            readJsonFile = self.diaryRead()
            checkStatusForFlagExistsInSystem = True
            # start to check if the script inside of the diary file
            if scriptNameTypeStr not in readJsonFile['folderMapLevel2'].keys():
                logger().printLog(
                    2, f'Script name [{scriptNameTypeStr}] not in system.')
                exit(0)
            # that mean that script has in the diary system.
            else:
                # check if flags is empty
                if not readJsonFile['folderMapLevel2'][scriptNameTypeStr]['flags']:
                    # create any flag
                    readJsonFile = createNewFlag()
                    checkStatusForFlagExistsInSystem = False
                # if flags item is not empty
                else:
                    # add new flag ?
                    # update old flag ?
                    # check if this flag is in the system
                    if wantedFlagToReadTypeStr not in readJsonFile['folderMapLevel2'][scriptNameTypeStr]['flags'].keys():
                        # create any flag
                        readJsonFile = createNewFlag()
                        checkStatusForFlagExistsInSystem = False
                    else:
                        checkStatusForFlagExistsInSystem = True

            if autoReturnForOutsideFunctionTypeBool:
                return readJsonFile['folderMapLevel2'][scriptNameTypeStr]['flags'][wantedFlagToReadTypeStr]['sysArgsNeed']
            if not autoReturnForOutsideFunctionTypeBool:
                return checkStatusForFlagExistsInSystem
        # start to check if the script inside of the diary file
        if scriptNameTypeStr not in readJsonFile['folderMapLevel2'].keys():
            logger().printLog(
                2, f'Script name [{scriptNameTypeStr}] not in system.')
        # that mean that script has in the diary system.
        else:
            if updateFlagTypeList:
                print(updateExistsFlag())
            else:
                return checkExistsFlagInSystemSubFunction()

    # ------- # Methods -> manageScriptCaller # ------- #
    def manageScriptCaller(
            self,
            scriptFileName: str,
            argsInsertTypeStr: str = False,
            callAndUpdateToFullScriptTypeBool: bool = False
    ):
        """
        - Explain :
            - Checking all items inside the diary mapping level 2 .
            - Check if the file have interpreter.
                - If the file have interpreter -> continue to next check.
                - If not -> Ask user what interpreter to have to file and update the diary + mapping file inside the logs
            - Check if the file have any flags
        - Flag :
            - scriptFileName : str -> [Default] : False
                - What to search inside the diary file ? which script name ?
        - Return:
            - str with (Interpertor) (ScriptPath) (Flags) (AnySysArgs)
            - python FullPathForScript -t AnyArgs
        """
        # init basic args
        readJsonFile = self.diaryRead()
        # extract full path for this script
        fullPathForInsertScript = readJsonFile['folderMapLevel2'][scriptFileName]['path']
        # start to check missing interpertor
        interpreter = self.callerHandlerInterpertor(scriptFileName)
        # check if the user is insert any flags
        seekFlags = self.seekFlags(
            argsInsertTypeStr, seekFlagsOnlyTypeBool=True)
        # check if the user is insert any args
        seekArgs = self.seekFlags(
            argsInsertTypeStr, seekArgsOnlyTypeBool=True)
        # start to check missing flags
        # True
        if seekFlags[0]:
            logger().printLog(0, f'Flag Giving is [{seekFlags[1]}].')
            # check if for this args need to be any args
            checkFlagSysArgs = self.callerHandlerFlags(
                scriptFileName, seekFlags[1], updateFlagTypeList=callAndUpdateToFullScriptTypeBool)
            # true
            if checkFlagSysArgs:
                logger().printLog(
                    3, f'Check Args for this script is [{checkFlagSysArgs}]')
                # check the user for insert any args
                # True
                if seekArgs[0]:
                    logger().printLog(
                        1, f'Args giving for script is [{seekArgs[1]}]')

                    return f'{interpreter} {fullPathForInsertScript} {seekFlags[1]} "{seekArgs[1]}"'
                # False
                else:
                    logger().printLog(2, 'Not giving any args for this flag , return it as it.')
                    return f'{interpreter} {fullPathForInsertScript} {seekFlags[1]}'
            else:
                logger().printLog(0,
                                  'No Args was giving or needed , return auto caller for giving script.')
                return f'{interpreter} {fullPathForInsertScript} {seekFlags[1]}'

        if not seekFlags[0]:
            logger().printLog(2, 'Not Flag giving.')
            tempVar = ''
            for each in list(range(2, len(sys.argv))):
                tempVar = tempVar + ' ' + sys.argv[each]
            return f'{interpreter} {fullPathForInsertScript} {tempVar.strip()}'

    # ------- # Methods -> revelFolderOrFile # ------- #
    def revelFolderOrFile(self, nameToRevel: str):
        """
        Explain :
            Check if file is folder or file
        Flag :
            :itemToSearchTypeStr : str -> [Default] : False
                What to search inside the diary file ? file ? folder ?
        Return:
            'folder' = it's a folder
            'file' = it's a file
        """
        nameTpRevelCheck = nameToRevel.split('.')
        if len(nameTpRevelCheck) > 1:
            return 'file'
        if len(nameTpRevelCheck) == 1:
            return 'folder'

    # ------- # Methods -> searchFileFolderInDiaryFile # ------- #
    def searchFileFolderInDiaryFile(
            self,
            itemToSearchTypeStr: str,
            argsInsert: str,
            callAndUpdateToFullScriptTypeBool: bool = False,
            returnOnlyPathForFileFolderTypeBool: bool = False

    ):
        """
        Explain :
            Show the status for action happend in code
        Flag :
            :itemToSearchTypeStr : str -> [Default] : False
                What to search inside the diary file ? file ? folder ?
        Return:
            Found -> full path of this file or folder./n
            Not Found -> False
        """
        # init basic variable

        readDiaryFile = self.diaryRead()['folderMapLevel2']
        # check if the item exists or not
        if itemToSearchTypeStr in readDiaryFile.keys():
            # print(
            #     f'Key [{itemToSearchTypeStr}] --> Value [{readDiaryFile[itemToSearchTypeStr]}] ', )
            if self.revelFolderOrFile(itemToSearchTypeStr) == 'folder':
                return readDiaryFile[itemToSearchTypeStr]
            if self.revelFolderOrFile(itemToSearchTypeStr) == 'file':
                if returnOnlyPathForFileFolderTypeBool:
                    return readDiaryFile[itemToSearchTypeStr]
                else:
                    return self.manageScriptCaller(itemToSearchTypeStr, argsInsert, callAndUpdateToFullScriptTypeBool)
        else:
            # init basic variable
            askUserWhichValueToReturn = True
            matchKeys = []
            regexPatt = re.compile(f"{itemToSearchTypeStr}")
            # start checking
            for eachKey in readDiaryFile.keys():
                regexSearch = re.findall(regexPatt, eachKey)
                # check if regex found any item
                if regexSearch:
                    matchKeys.append(eachKey)
            # check how many rows the found keys :
            #   If len=1 : return this list
            #   else: ask user which item to insert
            if len(matchKeys) == 1:
                logger().printLog(1,
                                  f'Found key [{matchKeys[0]}] by partial str --> [{itemToSearchTypeStr}].')
                if self.revelFolderOrFile(matchKeys[0]) == 'folder':
                    return readDiaryFile[matchKeys[0]]
                if self.revelFolderOrFile(matchKeys[0]) == 'file':
                    if returnOnlyPathForFileFolderTypeBool:
                        return readDiaryFile[matchKeys[0]]
                    else:
                        return self.manageScriptCaller(matchKeys[0], argsInsert, callAndUpdateToFullScriptTypeBool)
            elif len(matchKeys) > 1:
                # print all items inside match keys
                logger().printLog(1,
                                  f'Found more then one key [{len(matchKeys)-1}] from partial insert key --> [{itemToSearchTypeStr}]')
                # looping
                for n, eachItem in enumerate(matchKeys):
                    print(f'\tFor key [{eachItem}] Chose Number [{n}]')
                while askUserWhichValueToReturn:
                    try:
                        inpChose = input('Please chose which one to use : ')
                        logger().printLog(5,
                                          f'\tKey [{matchKeys[int(inpChose)]}] --> Value [{readDiaryFile[matchKeys[int(inpChose)]]}]')
                        if self.revelFolderOrFile(matchKeys[int(inpChose)]) == 'folder':
                            return readDiaryFile[matchKeys[int(inpChose)]]
                        if self.revelFolderOrFile(matchKeys[int(inpChose)]) == 'file':
                            if returnOnlyPathForFileFolderTypeBool:
                                return readDiaryFile[matchKeys[int(inpChose)]]
                            else:
                                return self.manageScriptCaller(matchKeys[int(inpChose)], argsInsert, callAndUpdateToFullScriptTypeBool)

                    except (ValueError, IndexError):
                        logger().printLog(2, 'Number Only / Only number in range.')


# Running only if system in this file
if __name__ == '__main__':
    startTime = datetime.datetime.now()
    # print(logger().printColor(0, f'{printLine}'))
    logger().printLog(
        7, f'# // System in main --> [{str(scriptNameAdam).replace(".py","")}]')
    try:
        # ------- # Caller -> -a # ------- #
        # call alias writer
        if sys.argv[1] == '-a':
            aliasName = sys.argv[2]
            aliasValue = extractDataFromListToAutoAlias(sys.argv[3::])
            if aliasName and aliasValue:
                Installer().autoAliasForAdam(insertDynamicNameAliasTypeStr=aliasName,
                                             insertDynamicValueAliasTypeStr=aliasValue)
        # ------- # Caller -> -f # ------- #
        # force init diary file
        # -f : force install
        if sys.argv[1] == '-f':
            gotoAdamFolder()
            Installer().finalResults(forceCreateDiaryInitTypeBool=True)
        # ------- # Caller -> -i # ------- #
        # install without any force
        # -i : install
        if sys.argv[1] == '-i':
            gotoAdamFolder()
            Installer().finalResults()
        # ------- # Caller -> -ss # ------- #
        # search Item inside diary folder
        # -s : search diary
        if sys.argv[1] == '-s':
            gotoAdamFolder()
            print(Interpertor().searchFileFolderInDiaryFile(
                sys.argv[2], sys.argv[3::]))
        # ------- # Caller -> -su # ------- #
        # -su : search diary and update it with insert flag
        if sys.argv[1] == '-su':
            gotoAdamFolder()
            Interpertor().searchFileFolderInDiaryFile(
                sys.argv[2],
                sys.argv[3::],
                callAndUpdateToFullScriptTypeBool=True)
        # ------- # Caller -> -h # ------- #
        # auto helper with mode of basic
        if sys.argv[1] == '-h':
            Installer().flagReaderBasicPrintHelper(printOnlyNamedDialog=True)
        # [ extract path ]the path of the file/folder only and return it
        if sys.argv[1] == '-ep':
            gotoAdamFolder()
            print(Interpertor().searchFileFolderInDiaryFile(
                sys.argv[2], sys.argv[3::]))
        # ------- # Caller -> -epa # ------- #
        # [ extract path automatic]the path of the file/folder only and return it
        if sys.argv[1] == '-epa':
            gotoAdamFolder()
            print(str(Interpertor().searchFileFolderInDiaryFile(
                sys.argv[2], sys.argv[3::])).replace('python3', '').replace('python', '').strip())
        # ------- # Caller -> -cts # ------- #
        # [ copy to script folder ] copy any file to script folder
        if sys.argv[1] == '-cts':
            # init basic var
            extractRealPathFile = os.popen(
                f'realpath {sys.argv[2]}').read().strip()
            gotoAdamFolder()
            Installer().copyFilesToScriptsFolder(extractRealPathFile)
        # ------- # Caller -> -c / -cr / -cu / -cru # ------- #
        if sys.argv[1] == '-c' or sys.argv[1] == '-cr' or sys.argv[1] == '-cu' or sys.argv[1] == '-cru':
            # chdir
            gotoAdamFolder()
            getResultsFromAutoSearcher = Interpertor().searchFileFolderInDiaryFile(
                'command.py', sys.argv[1::])
            print(logger().printColor(0, f'{printLine}'))
            os.system(getResultsFromAutoSearcher)

        # search other script automatic and exec them
        else:
            logger().printLog(
                5, f'# // Script Name --> [{scriptNameAdam}]')
            getResultsFromAutoSearcher = Interpertor().searchFileFolderInDiaryFile(
                sys.argv[1], sys.argv[2::])
            if getResultsFromAutoSearcher == None:
                pass
            else:
                scriptName = os.path.basename(getResultsFromAutoSearcher)
                if str(scriptName).split(' ')[0] != 'git_manager.py':
                    gotoAdamFolder()
                scriptFlag = ''
                if not sys.argv[2::]:
                    scriptFlag = 'None Script Flag Insert'
                else:
                    scriptFlag = sys.argv[2::]
                logger().printLog(0,
                                  f'Activated Script Name [{scriptName}] With Flag [{scriptFlag}] {check}')
                print(logger().printColor(0, f'{printLine}'))

                os.system(getResultsFromAutoSearcher)
                # print(logger().printColor(0, f'{printLine}'))

    except IndexError:
        # if user did not enter any key --> he want to do other script from this
        pass

    logger().printLog(
        7, f'Total Time = {datetime.datetime.now()-startTime}', 'Time Calc')
    print(logger().printColor(0, f'{printLine}'))

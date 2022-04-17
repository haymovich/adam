import os
import sys
import time
from logger import logger
# ------- # global -> outside variable # ------- #
scriptName = os.path.basename(__file__)
check = u'\u2705'


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


def addItem(item):
    if checkOsSystem() == 'mac':
        return os.path.join(os.path.expanduser("~/"), str(item))
    if checkOsSystem() == 'linux':
        if item == '.bash_profile':
            pass
        else:
            originalUsername = str(os.path.dirname(
                os.path.realpath(__file__))).split('/')[2]
            return os.path.join(f'/home/{originalUsername}', str(item))


def extractTheRightSyntaxForAdamAutoAlias(aliasNameTypeStr: str, aliasValueTypeStr: str):
    """
    - Explain :
        - Check if the alias value is folder or file:
            - If folder --> add auto c_ before the alias name
            - Else -->
                - add auto f_ before the alias name
    """
    # init basic var
    aliasNameVar = str(aliasNameTypeStr)
    aliasValueVar = str(aliasValueTypeStr)
    # check if the alias value is file
    if '.' in aliasNameVar:
        aliasNameVar = f"f{aliasNameVar.split('.')[0].strip()}"
        logger().printLog(0,
                          'Auto [file] detect.')
        # ignore .pyc
        if aliasValueTypeStr.endswith('.pyc'):
            logger().printLog(6, 'Ignoring .pyc file.')
        # check if alias is finish with .py
        if aliasValueTypeStr.endswith('.py'):
            logger().printLog(0, 'Python file has been detected , add auto python3 before alias value.')
            aliasValueVar = f'python3 {aliasValueVar}'
        # check if the file is javascript
        if aliasValueTypeStr.endswith('.js'):
            logger().printLog(0, 'JavaScript file has been detected , add auto node before alias value.')
            aliasValueVar = f'node {aliasValueVar}'

    # check if the alias value is folder
    elif '.' not in aliasNameVar:
        # ADD C_ BEFORE
        # aliasNameVar = str(f'c_{aliasNameVar.replace(".","").strip()}')
        aliasNameVar = str(f'c{aliasNameVar.replace(".","").strip()}')
        aliasValueVar = f'cd {aliasValueVar}'
        logger().printLog(0,
                          'Auto [folder] detect.')
    # return
    return f'alias {aliasNameVar}="{aliasValueVar}"'


# read and modify bash profile file
def readAndModifyBashProfileFile(
        adamPathTypeStr: str = False,
        aliasNameToAddTypeStr: str = False,
        aliasValueToAddTypeStr: str = False):
    # init basic var
    counter = 1
    aliasAdam = []
    tempListForHoldDataTypeList = []
    fileNameToRewrite = ['.bashrc', '.bash_profile']
    pathBashProfile = list(map(addItem, fileNameToRewrite))

    # check if user insert the adam path
    if adamPathTypeStr:
        logger().printLog(0, 'Init auto adam alias.')
        # aliasAdam.append(f'alias adam="{adamPathTypeStr}"')
        aliasAdam.append(f'alias adam="sudo {adamPathTypeStr}"')
        aliasAdam.append(
            f'alias cadam="cd {os.path.dirname(str(adamPathTypeStr).replace("python3","").strip())}"')
    elif aliasNameToAddTypeStr and aliasValueToAddTypeStr:
        if '.pyc' in aliasValueToAddTypeStr:
            logger().printLog(6, 'Ignoring .pyc file.')
        else:
            logger().printLog(0,
                              f'Init alias Call from adam --> Alias Key [{aliasNameToAddTypeStr}] | Alias Value [{aliasValueToAddTypeStr}]')
            aliasSynatx = extractTheRightSyntaxForAdamAutoAlias(
                aliasNameToAddTypeStr, aliasValueToAddTypeStr)
            aliasAdam.append(aliasSynatx)
    # print
    logger().printLog(0,
                      f'Step Number --> [{counter}] | Please wait , mapping files --> [bash_profile,bashrc]')
    counter += 1
    # open the bash_profile and update it to adam -- read
    for eachItem in pathBashProfile:
        if eachItem == None:
            pass
        else:
            with open(eachItem, 'r') as readBashProfile:
                for eachRow in readBashProfile.readlines():
                    # get rid of the '\n' for each row
                    eachRowWithoutNewLineError = eachRow.replace('\n', '')
                    tempListForHoldDataTypeList.append(
                        eachRowWithoutNewLineError)
            # check if giving item is in the file
            for eachAlias in sorted(aliasAdam):
                if eachAlias not in tempListForHoldDataTypeList:
                    tempListForHoldDataTypeList.append(eachAlias)
            # print
            logger().printLog(0,
                              f'Step Number --> [{counter}] | Finish Mapping file [{eachItem}] with adam alias , Starting to write')
            # write
            counter += 1

            with open(eachItem, 'w') as writeNewDataToBashProfile:
                for eachRow in tempListForHoldDataTypeList:
                    writeNewDataToBashProfile.write(f'{eachRow}\n')
            os.system(f'source {eachItem}')
            # print
            logger().printLog(0,
                              f'Step Number --> [{counter}] | Finish Mapping adam libray to system , please re-lunch the terminal')
            counter += 1
            logger().printLog(0,
                              f'Step Number --> [{counter}] | You can use commnad - [adam -h] to see avaliable command')
            tempListForHoldDataTypeList.clear()
            logger().printLog(1,
                              f'# ----- # {check} Done Mapping alias [{eachAlias}] {check} # ----- #')


# Running only if system in this file
if __name__ == '__main__':
    logger().printLog(
        5, f'# // Script Name --> [{scriptName}]')
    try:
        # ------- # Caller -> -p # ------- #
        # call alias auto mode for adam folder
        if sys.argv[1] == '-p':
            # test start
            logger().printLog(7, '==== Test Init ====')
            readAndModifyBashProfileFile(sys.argv[2::][0])
            logger().printLog(7, '==== Test Done ====')
        # ------- # Caller -> -a # ------- #
        # alias
        elif sys.argv[1] == '-a':
            try:
                logger().printLog(7, '==== Test Init ====')
                aliasName = str(sys.argv[2]).split('-')[0][1::][:-1].strip()
                aliasValue = str(sys.argv[2]).split('-')[1][1::][:-1].strip()
                readAndModifyBashProfileFile(False, aliasName, aliasValue)
                logger().printLog(7, '==== Test Done ====')

            except IndexError:
                logger().printLog(2, 'Must get both alias key && alias value.')
            # readAndModifyBashProfileFile()
    except IndexError:
        pass

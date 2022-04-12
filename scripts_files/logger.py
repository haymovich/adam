#!/usr/bin/python3
"""
@Author:Bar levi haymovich
"""
import datetime
import subprocess
import sys
import os


# ------- # Outside Variable # ------- #
logCounter = 0
dashLine = '-------------------------------------------'


# ------- # Class -> logger # ------- #
class logger:
    """
    - Explain :
        - print with color inside user interface
    - Available methods :
        - info : blueColor | Bold
            - info for something like ip address / hostname
        - pass : greenColor | Bold
            - test pass
        - failed : failColor | Bold
            - test failed
        - check started : yellowColor | Bold
            - start to checking something
        - check ended : yellowColor | Bold
            - end to checking something
        - change : turquoiseColor | Bold
            - something that change like ip address
        - costumeInfo : color white
            - able to print what the user want.
    - Comment :
        - Add Style && info about what happened in system.
    """

    def __init__(self):
        # ------- # Default attributes -> color Variable # ------- #
        self.purpleColor = '\033[95m'
        self.blueColor = '\033[94m'
        self.turquoiseColor = '\033[96m'
        self.greenColor = '\033[92m'
        self.yellowColor = '\033[93m'
        self.failColor = '\033[91m'
        # ------- # Default attributes -> option To Colors # ------- #
        self.endOfLine = '\033[0m'
        self.makeBold = '\033[1m'
        self.makeUnderline = '\033[4m'
        # ------- # Default attributes -> basic Variable # ------- #
        self.currentTime = datetime.datetime.now().strftime(f"%d-%b-%y %T")
        # ------- # Default attributes -> Names # ------- #
        pass
        # ------- # Default attributes -> Path # ------- #
        pass
        # ------- # Default attributes -> Example # ------- #
        # logger().printLog(0,'test_0')
        # logger().printLog(0,'test_0',False)
        # logger().printLog(1,'test_1')
        # logger().printLog(1,'test_1',False)
        # logger().printLog(2,'test_2')
        # logger().printLog(2,'test_2',False)
        # logger().printLog(3,'test_3')
        # logger().printLog(3,'test_3',False)
        # logger().printLog(4,'test_4')
        # logger().printLog(4,'test_4',False)
        # logger().printLog(5,'test_5')
        # logger().printLog(5,'test_5',False)
        # logger().printLog(6,'test_6')
        # logger().printLog(6,'test_6',False)

        # logger().printLog(7, 'test', 'test', 1)
        # logger().printLog(7, 'test', 'test', 2)
        # logger().printLog(7, 'test', 'test', 3)
        # logger().printLog(7, 'test', 'test', 4)
        # logger().printLog(7, 'test', 'test', 5)
        # logger().printLog(7, 'test', 'test')

    # ------- # Methods -> saveLogToFile # ------- #
    def saveLogToFile(
            self,
            saveTypeHistoryOrOutputTypeInt: int,
    ):
        """
        - Explain : 
            - This method is for saving what happens in the run to a file.
            - 
        - TODO :
            - Not finish.
        """
        # init basic var
        findLogFilePath = self.findAliasValue('clogs')
        pathLogRunHistoryFiles = ''
        # check if the
        if os.path.exists(findLogFilePath):
            pathLogRunHistoryFiles = os.path.join(
                findLogFilePath, 'LogRunHistoryFiles', 'text.txt')

    # ------- # Methods -> getSpaces # ------- #
    def getSpaces(self, maximumSpacesTypeInt: int, wordToCalcTypeStr: str):
        """
        - Explain : 
            - This is for get space even between what user need
        """
        # init basic args
        lenWord = maximumSpacesTypeInt - int(len(str(wordToCalcTypeStr)))
        spacesToReturn = ' '*lenWord
        # return the spaces
        return spacesToReturn

    # ------- # Methods -> loggerCounterKeepTrack # ------- #
    def loggerCounterKeepTrack(self):
        """
        - Explain :
            - Keep track of counter for each test the have been call
        """
        # init basic var
        pathFolderLogsFromAlias = self.findAliasValue('logs')
        counterDictTracker = {}

    # ------- # Methods -> printLog # ------- #
    def printLog(
            self,
            logPrintTypeInt: int,
            msgTypeStr: str,
            statusInBracketTypeStr: str = False,
            colorToPickTypeInt: int = False,
            dateEnableDisableTypeBool: bool = True,
            returnTrueOrPrintFalseTypeBool=False
    ):
        """
        - Flag :
            - dateEnableDisableTypeBool :
                - True == With date
                - False == Without date
            - logPrintTypeInt:
                - What will be inside the Status && what will be the color :
                    - 0 == info :           BlueColor           | Bold
                    - 1 == pass :           greenColor          | Bold
                    - 2 == failed :         failColor           | Bold
                    - 3 == check started :  yellowColor         | Bold
                    - 4 == check ended :    yellowColor         | Bold
                    - 5 == change :         turquoiseColor      | Bold
                    - 6 == ignoring :       yellowColor         | Bold
                    - 7 == User Need :      WhiteColor          | None
                    - 8 == init :          yellowColor         | Bold

            - statusInBracketTypeStr:
                - What the status will be --> only work on level 7++
            - colorToPickTypeInt :
                - What color will be insert --> only work on level 7++ :
                    - 0 : white [default]
                    - 1 : blue
                    - 2 : red
                    - 3 : yellow
                    - 4 : turquoise

        """
        global logCounter

        # init basic Var
        status = ''
        colorToPick = ''
        boldText = self.makeBold
        spaces = self.getSpaces(7, logCounter)
        separator = '|'
        showResults = f'{msgTypeStr}'

        # assign the correct color and status --> info : blue : bold
        if logPrintTypeInt == 0:
            status = ' [Status --> Info]'
            colorToPick = self.blueColor
        # assign the correct color and status --> pass : green : bold
        if logPrintTypeInt == 1:
            status = ' [Status --> Pass]'
            colorToPick = self.greenColor
        # assign the correct color and status --> failed : red : bold
        if logPrintTypeInt == 2:
            status = ' [Status --> Failed]'
            colorToPick = self.failColor
        # assign the correct color and status --> check started : yellow : bold
        if logPrintTypeInt == 3:
            status = ' [Status --> Check Started]'
            colorToPick = self.yellowColor
        # assign the correct color and status --> check ended : yellow : bold
        if logPrintTypeInt == 4:
            status = ' [Status --> Check Ending]'
            colorToPick = self.yellowColor
        # assign the correct color and status --> change : turquoise : bold
        if logPrintTypeInt == 5:
            status = ' [Status --> Change]'
            colorToPick = self.turquoiseColor
        # assign the correct color and status --> Ignoring : Yellow : bold
        if logPrintTypeInt == 6:
            status = ' [Status --> Ignoring]'
            colorToPick = self.turquoiseColor
        # assign the correct color and status --> user need
        if logPrintTypeInt == 7:
            # check for status
            if statusInBracketTypeStr:
                status = f' [Status --> {statusInBracketTypeStr}]'
            # check for color
            # blue
            if colorToPickTypeInt == 1:
                colorToPick = self.blueColor
            # red
            if colorToPickTypeInt == 2:
                colorToPick = self.failColor
            # yellow
            if colorToPickTypeInt == 3:
                colorToPick = self.yellowColor
            # turquoise
            if colorToPickTypeInt == 4:
                colorToPick = self.turquoiseColor
        # assign the correct color and status --> check : yellow : bold
        if logPrintTypeInt == 8:
            status = ' [Status --> init]'
            colorToPick = self.yellowColor
        # check for date --> True
        if dateEnableDisableTypeBool:
            showResults = f'{boldText}{self.currentTime} {separator}{colorToPick}{status} {showResults} {self.endOfLine}'
            # showResults = f'{boldText}{colorToPick}{logCounter}{spaces}{separator} {self.currentTime} {separator}{status} {showResults} {self.endOfLine}'
        # check for date --> False
        if not dateEnableDisableTypeBool:
            showResults = f'{boldText}{colorToPick}{status}{showResults} {self.endOfLine}'
            # showResults = f'{boldText}{colorToPick}{logCounter}{spaces}{separator} {status} {showResults} {self.endOfLine}'
        # added counter log by one
        logCounter += 1
        # return
        if returnTrueOrPrintFalseTypeBool:
            return showResults
        # print
        if not returnTrueOrPrintFalseTypeBool:
            print(showResults)

    # ------- # Methods -> printColor # ------- #
    def printColor(self, colorToPickTypeInt: int, msgTypeStr: str):
        """
        - Explain :
            - Print with any color and not with any item of printLog
        - Flags :
            - colorToPickTypeInt :
                - 0 : white [default]
                - 1 : blue
                - 2 : red
                - 3 : yellow
                - 4 : turquoise
                - 5 : green
            - msgTypeStr :
                - What do you want to print ?
        """
        # init basic vars
        showResults = msgTypeStr
        # print(showResults)
        colorToPick = ''
        # check for color
        # blue
        if colorToPickTypeInt == 1:
            colorToPick = self.blueColor
        # red
        if colorToPickTypeInt == 2:
            colorToPick = self.failColor
        # yellow
        if colorToPickTypeInt == 3:
            colorToPick = self.yellowColor
        # turquoise
        if colorToPickTypeInt == 4:
            colorToPick = self.turquoiseColor
        # green
        if colorToPickTypeInt == 5:
            colorToPick = self.greenColor
        # change the variable
        showResults = f'{self.makeBold}{colorToPick}{showResults}{self.endOfLine}'
        # print the output
        return showResults

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
            - find adam script path from command alias
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


# if __name__ == '__main__':
#     logger().findAliasValue('clogs', True)
    # logger().saveLogToFile('1')

import shutil
import subprocess
import threading
from tkinter import *
import os
from tkinter import messagebox


def getAllItemToPyinstaller(pathForFind):
    filePathList = []
    for _ in os.listdir(pathForFind):
        if _.endswith('.py'):
            filePathList.append(os.path.join(pathForFind, _))
    return filePathList


def createAppFolder(pathForFindUnLocal):
    appFolderPath = os.path.join(pathForFindUnLocal, 'App')
    tempList = []
    if not os.path.exists(appFolderPath):
        os.mkdir(appFolderPath)
    if os.path.exists(appFolderPath):
        shutil.rmtree(appFolderPath)
        os.mkdir(appFolderPath)

    for each in getAllItemToPyinstaller(pathForFindUnLocal):
        extractFileNameFull = each
        extractFileNameRaw = str(os.path.basename(each)).replace('.py', '')
        pathForEachFolder = os.path.join(appFolderPath, extractFileNameRaw)
        # create each folder in the folder for each app
        if not os.path.exists(pathForEachFolder):
            os.mkdir(pathForEachFolder)
        # create each app installer for each app
        fullPathForBatFile = os.path.join(
            pathForEachFolder, extractFileNameRaw + '.bat')
        tempList.append(fullPathForBatFile)
        with open(fullPathForBatFile, 'w') as newBatFile:
            newBatFile.write(
                f'pyinstaller --onefile --noconsole "{extractFileNameFull}"')
    return tempList


def centerWindow(windowVariable,
                 windowHeight,
                 windowWidth):
    screen_width = windowVariable.winfo_screenwidth()
    screen_height = windowVariable.winfo_screenheight()
    window_height = windowHeight
    window_width = windowWidth
    x_coordinate = int((screen_width / 2) - (window_width / 2))
    y_coordinate = int((screen_height / 2) - (window_height / 2))
    return f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}"


# ------------- # Class -> ApplicationGuiFrontEnd # ------------- #
root = Tk()


class ApplicationGuiFrontEnd():
    def __init__(self, masterRoot):
        # ------------- # Class Attributes -> Super Init # ------------- #
        # ------------- # Class Attributes -> Super master root # ------------- #
        self.masterRoot = masterRoot

        self.colorMaster = '#126de3'

        self.masterRoot.config(bg="white")
        self.checkSnMultiWindow = 0
        self.multiWindowSection = []
        self.mainWellcome = ''
        self.winBackEndWindow = ''

        # Put window in middle in the startup
        screen_width = masterRoot.winfo_screenwidth()
        screen_height = masterRoot.winfo_screenheight()
        window_width = 320
        window_height = 130
        x_coordinate = int((screen_width / 2) - (window_width / 2))
        # x_coordinate = 0
        y_coordinate = int((screen_height / 2) - (window_height / 2))
        # y_coordinate = 100
        self.masterRoot.geometry(
            f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")
        # Get the title for the window
        self.masterRoot.title('Application Auto Bat')
        # version
        self.masterRoot.resizable(False, False)
        # ------------- # Class Attributes -> variable # ------------- #

        # Update btn Main
        self.lblForEnterFolder = Label(self.masterRoot,
                                       text=f'Please Enter A Folder',
                                       font=("calibri", 16,
                                             "bold"))
        self.entForEntAutoBat = Entry(self.masterRoot,
                                      bd=2,
                                      width=37)
        self.btnUpdateMain = Button(self.masterRoot,
                                    text='Create Auto Bat Here',
                                    font=("calibri", 18, "bold"),
                                    relief=GROOVE,
                                    command=self.threadingMain,
                                    bg=self.colorMaster,
                                    fg="white")

        # ------------- # Class Attributes ->  layout # ------------- #
        # main frame label
        self.lblForEnterFolder.config(bg="white")

        self.lblForEnterFolder.pack()
        self.entForEntAutoBat.pack(pady=3)
        self.btnUpdateMain.pack()

    # ////////////////////////// Start Methods ////////////////////////// #
    # ------------- # Class Method ->  initAutoBat # ------------- #
    def threadingMain(self):
        threadLoadingBar = threading.Thread(target=self.loadindWindow)
        threadBackEnd = threading.Thread(target=self.initAutoBat)

        threadLoadingBar.start()
        threadBackEnd.start()

    def loadindWindow(self):
        # Open the Top Level window
        self.PopupWindowForProgressBar = Toplevel(self.masterRoot)
        # Create Progress Bar
        self.lblWait = Label(self.PopupWindowForProgressBar,
                             text='Please Wait While init pyinstaller for files...',
                             font=("calibri", 10, "bold")).pack(pady=30, padx=10)
        # Put window in middle in the startup
        screen_widthProgressBar = self.PopupWindowForProgressBar.winfo_screenwidth()
        screen_heightProgressBar = self.PopupWindowForProgressBar.winfo_screenheight()
        window_heightProgressBar = 100
        window_widthProgressBar = 270
        x_coordinateProgressBar = int(
            (screen_widthProgressBar / 2) - (window_widthProgressBar / 2))
        y_coordinateProgressBar = int(
            (screen_heightProgressBar / 2) - (window_heightProgressBar / 2))
        self.PopupWindowForProgressBar.geometry(
            f"{window_widthProgressBar}x{window_heightProgressBar}+{x_coordinateProgressBar}+{y_coordinateProgressBar}")
        # make the window on top the main root window
        self.PopupWindowForProgressBar.lift(self.PopupWindowForProgressBar)
        self.PopupWindowForProgressBar.grab_set()
        self.PopupWindowForProgressBar.grab_set_global()

        # Disable the option to close the window
        def disableEvent():
            pass

        self.PopupWindowForProgressBar.protocol(
            "WM_DELETE_WINDOW", disableEvent)
        # Get the title for the window
        self.PopupWindowForProgressBar.title('Loading Window')

    def initAutoBat(self):
        batItem = createAppFolder(self.entForEntAutoBat.get())

        for i in batItem:
            baseNameForFile = os.path.basename(i)
            chadirToBatFolder = str(i).replace(baseNameForFile, '')
            os.chdir(chadirToBatFolder)
            subprocess.call(f'{i}')

        self.entForEntAutoBat.delete(0, END)
        self.loadingBarDestroy()
        tempVar = ''
        for _ in batItem:
            tempVar = os.path.basename(
                tempVar) + os.path.basename(tempVar) + f'\n{_}'
        messagebox.showinfo('App Finish Successfully',
                            'Successfuly extract all items in :\n'
                            f'{[i for i in [os.path.basename(i) for i in batItem]]}.\n'
                            f'You can close this promote.')

    def loadingBarDestroy(self):
        try:
            # Pull back the main window
            self.PopupWindowForProgressBar.destroy()
            self.masterRoot.lift()
        except AttributeError:
            pass


callerApplicationGui = ApplicationGuiFrontEnd(root)
root.mainloop()

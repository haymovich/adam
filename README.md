# Adam Framework
![GitHub commit activity](https://img.shields.io/github/commit-activity/w/haymovich/adam?style=flat-square) ![GitHub last commit](https://img.shields.io/github/last-commit/haymovich/adam?label=Last%20Commit&style=flat-square) ![GitHub](https://img.shields.io/github/license/haymovich/adam)

## Requirements ❗️
* Any linux base / mac pc.
* Currently this repo isn't work on windows machine.

## Interduction 📜
### Adam is a python linux workflow helper that able to :
1. Call other script from anywhere on the pc.
2. Insert pined command and call them from by one command.
3. Create alias for Linux/Mac automatic.
4. Git manger to push/create new tag with batter syntax.
5. Logger script for batter readably.
6. General improve workflow for user.
The idea is put all script in one folder and call them by just one script , or pull personal command.

## Installation 💻
### Go to folder that you want to install adam and run command :
```
git clone https://github.com/haymovich/adam.git
```
### Install adam by enter :
```
sudo ./adam.py -i 
```
### You can allways do another installation and by instert :
```
sudo ./adam.py -f
```
* Note that you must close your terminal after installtion ( this is one time opration ).
* Adam will map folder and files and create auto alias.
* If he'll find folder then the alias will be cFolderName, Example : 
```
cadam
```
* If he'll find file then the alias will be FileName
```
adam
```
## Usage 📝
### Adam 👨🏻‍💻
* Helper - this will show all available action that can be do and and what all the path for all folder.
```
adam -h
```
#### Default Call other script from adam 🔎
* By Default , you can use all this scripts :
* Repleace the # before if want to exec them
```
#adam -a AliasName AliasValue
#adam -f
#adam -i
#adam -su
#adam -cts FileName
#adam command.py -c Command
#adam command.py -c -change Command
#adam command.py -cr Command
#adam git_mannger.py -nt 1 Create new Tag Type Major
#adam git_mannger.py -nt 2 Create new Tag Type Minor
#adam git_mannger.py -nt 3 Create new Tag Type Patch
#adam git_mannger.py -p Push
#adam logger.py
#adam testScriptExample.py 
```
#### Dyamic Call other script from adam 🔎
* Any script can be insert to adam libray.
* You'll need to be inside the folder that the file you want to copy is located in.
* You can activated the dynamic create with one command : 
```
adam -cts FileName
```
* Example for copy : 
![image](https://user-images.githubusercontent.com/81128508/162971128-b5c7efef-ee93-426c-ab7a-5218afc12eca.png)
![image](https://user-images.githubusercontent.com/81128508/162971822-f40d2a8e-f781-4e56-a612-e7d2222a6022.png)

#### Create alias with adam 🆕
```
adam -a AliasName AliasValue
```
### Command 📚
#### Create / Exec command 🆕
* You can create or Execuate your command
```
adam -c commandExample
```
* Example for command : 
![image](https://user-images.githubusercontent.com/81128508/162733694-120361f3-c7bf-49ed-83de-af8fbc9602f6.png)
* You can insert command like :
```
cadam ; pwd ; cd ../ ; pwd ; hostname
```
#### Change your command ✍🏽
```
adam -c -change commandExample 
```
#### Read Your command 📖
```
adam -cr commandExample 
```
* Example :
![image](https://user-images.githubusercontent.com/81128508/162733623-6d66daac-9660-4d5e-bdb3-18b78c14fdcd.png)
### Git Manager 🕴
#### Push to git with specific syntax
* It'll push from exists folder.
* Authentication for git is require.
```
adam git_manager.py -p WhatToPush
```
#### Create tag by adam 🆕
* You have 3 diffrent option to release a tag.
* Each type will incress the index by 1.
##### Major Tag Release 🔴
* Major is the 1️⃣.0.0
```
adam git_manager.py -nt 1 WhatToReleaseMajorTagPush
```
##### Minor Tag Release 🟠
* Minor is the 1.0️⃣.0
```
adam git_manager.py -nt 2 WhatToReleaseMinorTagPush
```
##### Patch Tag Release ⚪️
* Patch is the 1.0.0️⃣
```
adam git_manager.py -nt 3 WhatToReleasePatchTagPush
```

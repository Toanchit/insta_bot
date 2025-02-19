import time
import webbrowser
import random
from time import sleep
# pickle is used to save the cookies
import os
import downloadVideo,instaloader
import glob
# pyautogui is usded to handle popup
import shutil,json,threading
import pyperclip
import account
import util
from datetime import date
# path="C:/Users/leduc/OneDrive/Desktop/code/python/insta_bot/listAccount"
path = os.getcwd()+"/listAccount"
# path1="C:/Users/leduc/OneDrive/Desktop/code/python/insta_bot/listData/"
path1 = os.getcwd()+"/listData/"

existTask =6
if os.path.isdir(path) == False:
    os.mkdir(path)
def convertStringToInt(s):
    try:
        size =len(s)
        temp=""
        for i in s:
            if i =='K':
                temp = temp+"000"
                break
            if i >='0' and i<='9':
                temp=temp+i
        return int(temp)
    except:
        return 0
def print_log(logs):
    fileLog = open("LogPost.txt","a",encoding='utf8')
    fileLog.write(logs)
    fileLog.write("\n")

listAccount=[]
isAccountAdded={}
def updateListAccount():
    listFollower=""
    for acc in glob.glob(path1+"*.json"):
        info = open(acc)
        data = json.load(info)
        mUser = data["accountUser"]
        mPassword = data["password"]
        mNiche = data["niche"]
        mHastagsSearch=data["hastagToSearch"]
        mHastagsPost = data["hastagToPost"]
        try:
            if isAccountAdded[mUser] == True:
                continue
        except:
            isAccountAdded[mUser]=True
        acc1 = account.account(mUser,mPassword,mHastagsSearch,mHastagsPost,mNiche)
        listAccount.append(acc1)
        print("find a new account ",acc1.mUser)
    #     listFollower=listFollower+downloadVideo.getNoFollower(mUser)

def getEachAcc(userName):
    for acc in listAccount:
        if acc.mUser == userName:
            return acc
def postForAllAccount():
    print("Start post all with ",len(listAccount)," account")
    j =0
    listFailAcc={}
    for acc in listAccount:
        j = j+1
        try:
            if acc.mUser !="startrek_fanaccount":
                if acc.login() == True:
                    acc.postTheNewPost(acc.downloadPost2())
                    acc.finishTask()
                    if j == len(listAccount):
                        break
                #     acc.postTheNewPost(True)
                else:
                    print(acc.mUser," login fail,try again")
                    acc.finishTask()
            elif acc.mUser =="startrek_fanaccount":
                continue
        except:
            print("there is an issue with account : ",acc.mUser," ",Exception)
            listFailAcc.append(acc)
            acc.finishTask()
            continue
        # change the sleep time to the end of loop to avoid the waiting time with the last element
        time.sleep(random.randint(200, 400))
    print("retry 1 time with acc post fail")
    j=0
    for acc in listFailAcc:
        j = j + 1
        try:
            if acc.mUser != "startrek_fanaccount":
                if acc.login() == True:
                    acc.postTheNewPost(acc.downloadPost2())
                    acc.finishTask()
                    if j == len(listFailAcc):
                        break
                #     acc.postTheNewPost(True)
                else:
                    print(acc.mUser, " login fail,try again")
                    acc.finishTask()
            elif acc.mUser == "startrek_fanaccount":
                continue
        except:
            print("there is an issue with account : ", acc.mUser, " ", Exception)
            acc.finishTask()
            continue
        # change the sleep time to the end of loop to avoid the waiting time with the last element
        time.sleep(random.randint(200, 400))
def handlingThePost():
    print("list the acc as below:")
    i =1
    for acc in listAccount:
        print(i,":",acc.mUser)
        i=i+1
    noAcc =int(input("Choose the acc will be post manually: "))
    if listAccount[noAcc-1].login() == True:
        while True:
            nextAct = int(input("What do you want to do :(1: exit) (2: fillCaption to post shirt) "))
            if nextAct == 1:
                listAccount[noAcc - 1].finishTask()
                break
            if nextAct ==2:
                listAccount[noAcc - 1].fillTheCaption()

def followWithAccount(mUser):
    print("Start follow the acount: ",mUser)
    acc = getEachAcc(mUser)
def postForEachAcc():
    print("list the acc as below:")
    i = 1
    for acc in listAccount:
        print(i, ":", acc.mUser)
        i = i + 1
    noAcc = int(input("Choose the acc will be post manually: "))
    if listAccount[noAcc - 1].login() == True:
        acc = listAccount[noAcc - 1]
        acc.postTheNewPost(acc.downloadPost2())
        acc.finishTask()
def postIncludedShirt():
    print("list the acc as below:")
    i = 1
    for acc in listAccount:
        print(i, ":", acc.mUser)
        i = i + 1
    noAcc = int(input("Choose the acc will be post manually: "))
    if listAccount[noAcc - 1].login() == True:
        acc = listAccount[noAcc - 1]
        acc.postTheNewPost2(acc.downloadPost2())
        acc.finishTask()
def postSpecificPost():
    print("list the acc as below: ")
    i = 1
    for acc in listAccount:
        print(i, ":", acc.mUser)
        i = i + 1
    noAcc = int(input("Choose the acc will be post with specific post : "))
    if listAccount[noAcc - 1].login() == True:
        acc = listAccount[noAcc - 1]
        acc.postTheNewPost3(acc.downloadSpecificPost())
        acc.finishTask()

def updatefFollower():
    lastData={}
    if os.path.isfile("today.json"):
        lastRe=open("today.json","r")
        lastData=json.load(lastRe)
    data={}
    change={}
    today = date.today()
    data["today"] = str(today)
    # Check with case create new yesterday data when detect the next day
    if lastData.get("today") != None:
        if lastData["today"]!= str(today):
            if os.path.isfile("yesterday.json"):
                os.remove("yesterday.json")
                yesterdayTemp = open("yesterday.json","w")
                json.dump(lastData,yesterdayTemp)
                yesterdayTemp.close()
            else:
                yesterdayTemp = open("yesterday.json", "w")
                json.dump(lastData, yesterdayTemp)
                yesterdayTemp.close()
    lastData1={}
    if os.path.isfile("yesterday.json"):
        lastRe1=open("yesterday.json","r")
        lastData1=json.load(lastRe1)
    for i in listAccount:
        if lastData1.get(i.mUser) == None:
            lastData1[i.mUser] = 0
        try:
            data[i.mUser]=getNoFollower(i.mUser)
            change[i.mUser]=data[i.mUser]-lastData1[i.mUser]
        except:
            print("cannot get followers of ",i.mUser," keep the latest data")
            data[i.mUser]=lastData1[i.mUser]
            continue
    data["change"] = change
    result = open("today.json","w")
    json.dump(data,result)
    # print("open file")
    os.startfile("today.json")
    # print("update follower succesffully")
def getNoFollower(userName):
    bot = instaloader.Instaloader()
    # Loading a profile from an Instagram handle
    profile = instaloader.Profile.from_username(bot.context, userName)
    return profile.followers
appStop = False
updateListAccount()
# fl=threading.Thread(target=updatefFollower,name="updateFollowerPerDay")
# fl.start()
print("List the action as below: ")
i = 1
while True:
    t1 = threading.Thread(target=postForAllAccount, name="postAll")
    t2 = threading.Thread(target=handlingThePost, name="posttheShirt")
    t3 = threading.Thread(target=postForEachAcc, name="postForEachAcc")
    t4= threading.Thread(target=postIncludedShirt, name="postIncludedShirt")
    t5 = threading.Thread(target=postSpecificPost,name ="postSpecificPost")
    listThread = []
    listThread.append(t1)
    listThread.append(t2)
    listThread.append(t3)
    listThread.append(t4)
    listThread.append(t5)
    i=1
    for mThread in listThread:
        print(i, ":", mThread.name)
        i = i + 1
    print(i,": exit")
    indThread = int(input("Choose the thread will be run:"))
    if indThread==existTask:
        break
    listThread[indThread-1].start()
    listThread[indThread-1].join()


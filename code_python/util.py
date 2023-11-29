import glob
import os
import random


def convertUrlToShortCode(urlLink):
    # urllink will be : https://www.instagram.com/p/Czu32hLLz6A/
    generalLink ="https://www.instagram.com/p/"
    lastId=0
    for i in range(len(generalLink),len(urlLink)):
        if urlLink[i] =='/':
            lastId =i
            break
    return urlLink[len(generalLink):lastId]
def correctFolderNameForCaption(folder):
    newFolder1 = folder.replace('\\','/')
    return newFolder1
def correctFolderName2(folder):
    newFolder = folder.replace('/','\\')
    newFolder1 =""
    for i in newFolder:
        newFolder1=newFolder1+i
    return newFolder1
def genRandom30List(maxNum):
    result =[]
    isCheck={}
    if maxNum<30:
        for i in range(maxNum):
            result.append(i)
    else:
        for k in range(maxNum):
            isCheck[k]=False
        count =0
        while count<30:
            i = random.randint(0,maxNum)
            if isCheck.get(i) == False:
                isCheck[i] = True
                count = count+1
                result.append(i)
    return result

def getCaption(folder,mHastagPost,mUser):
    try:
        filesToGet =""
        for files in glob.glob(folder+"*.txt"):
            filesToGet = files
            break
        print(correctFolderNameForCaption(filesToGet))
        caption = open(correctFolderNameForCaption(filesToGet),"r",encoding='utf8')
        result1 = caption.readlines()
        result=[]
        caption.close()
        for i in result1:
            if i[0] != '#':
                result.append(i)
        followMe = "Follow me for more : @"+mUser
        result.append(followMe)
        sizeHastag = len(mHastagPost)
        rand30 = genRandom30List(sizeHastag)
        hastag =""
        for i in rand30:
            hastag=hastag+mHastagPost[i]+" "
        result.append(hastag)
        return result
    except:
        print("Cannot get caption")
        print(NameError)
        return False
# t = "C:/Users/Admin/Desktop/code/code_python/listAccount\ "
# print(correctFolderName2(t))
# getCaption("C:/Users/Admin/Desktop/code/code_python/listAccount/startrek_fanaccount/image/")
def genJsonformat(path):
    try:
        file = open(path,"r")
        result = open("resultPost.txt","w",encoding='utf8')
        listHastags = file.readlines()
        for lineHastag in listHastags:
            for i in lineHastag:
                if i.isspace() == False:
                    if i != '#':
                        result.write(i)
                    else:
                        result.write("\"#")
                else:
                    result.write("\", \n")
        result.write('\"')
    except:
        print("cannot open file")
def genJsonformatSearch(path):
    try:
        file = open(path,"r")
        result = open("resultSearch.txt","w",encoding='utf8')
        listHastags = file.readlines()
        for lineHastag in listHastags:
            for i in lineHastag:
                if i.isspace() == False:
                    if i != '#' and i != ',':
                        result.write(i)
                    elif i =='#':
                        result.write("\"")
                    elif i ==',':
                        result.write("\",\n")
                else:
                    result.write("\",\n")
        result.write('\"')
    except:
        print("cannot open file")
genJsonformat("hastag.txt")
# for i in getCaption(30):
#     print(i)
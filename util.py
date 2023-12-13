import glob
import os
import random,requests,urllib.request
from bs4 import BeautifulSoup as bs
import html5lib
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
        isEnglish = False
        for i in result1:
            if i[0] != '#':
                result.append(i)
            if isEnglish == False and i[0].isascii() == False:
                print("the language is not English , need to download post again :",i[0])
                return ["NotEnglish"]
            else:
                isEnglish = True
        followMe = "Follow me for more : @"+mUser+"\n"
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
        print(Exception)
        return "False"
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


def get_video_links(archive_url):
    # create response object
    r = requests.get(archive_url)
    # create beautiful-soup object
    soup = bs(r.content, 'html.parser')
    # find all links on web-page
    links = soup.find('video')
    # filter the link ending with .mp4
    video_links = links['src']

    return video_links
def downloadVideoWithLink(url):
    # user_agent = {'User-agent': 'Mozilla/5.0'}
    # r = requests.get(url,stream=True,headers=user_agent)
    # with open("a.temp","wb") as fd:
    #     for chunk in r.iter_content(chunk_size=1024*1024):
    #         if chunk:
    #             fd.write(chunk)
    #         # fd.flush()
    # os.replace("a.temp","a.mp4")
    video_links = get_video_links(url)
    print("there are video with link",video_links)
    for link in video_links:
        file_name = link.split('/')[-1]
        print("Downloading file:%s" % file_name)
        urllib.request.urlretrieve(url,file_name)

# downloadVideoWithLink("https://www.instagram.com/p/C0OhH-wPZ_z")
# for i in getCaption(30):
#     print(i)
# genJsonformat("hastag.txt")
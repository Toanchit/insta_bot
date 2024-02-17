import time
import webbrowser
import random
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome import service
from selenium.webdriver.chrome.options import Options
# pickle is used to save the cookies
import os,pickle
import downloadVideo,instaloader
import glob
# pyautogui is usded to handle popup
import shutil,json,threading
import pyperclip

import util

path = "C:/Users/Admin/Desktop/code/code_python/listAccount"
JS_ADD_TEXT_TO_INPUT = """
  var elm = arguments[0], txt = arguments[1];
  elm.value += txt;
  elm.dispatchEvent(new Event('change'));
  """
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
            if i!=',' and i!='.':
                temp=temp+i
        return int(temp)
    except:
        return 0
def print_log(logs):
    fileLog = open("LogPost.txt","a",encoding='utf8')
    fileLog.write(logs)
    fileLog.write("\n")
class account:
    # the 2 line below to set chrome in the mode headless(ko hien thi)
    # optio = webdriver.ChromeOptions()
    # optio.add_argument('--headless')
    # driver = webdriver.Chrome(options=optio)
    # get chrome drive to open
    def __init__(self,user,passw,hastagsSearch,hastagsPost):
        # Create Chromeoptions instance
        self.options = webdriver.ChromeOptions()

        # Adding argument to disable the AutomationControlled flag
        self.options .add_argument("--disable-blink-features=AutomationControlled")

        # Exclude the collection of enable-automation switches
        self.options .add_experimental_option("excludeSwitches", ["enable-automation"])
        # turn off pop up save password
        self.options.add_argument("--password-store=basic")
        self.options.add_experimental_option(
        "prefs",
        {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
        },
        )
        # Turn-off userAutomationExtension
        self.options .add_experimental_option("useAutomationExtension", False)
        self.L = instaloader.Instaloader()
        self.mUser = user
        self.mPassw = passw
        self.isLogin = False
        self.mHastagsSearch = hastagsSearch
        self.mHastagsPost = hastagsPost
        self.mPath = path + '/' + self.mUser
        self.L.dirname_pattern = self.mPath+'/'
        if os.path.isdir(self.mPath) == False:
            os.mkdir(path+'/'+self.mUser)
        # login instagram
    def login(self):
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.get("https://www.instagram.com")
        if self.isCookies()==True:
            print("there already was cookies for accout: ",self.mUser)
            cookies = pickle.load(open(self.mPath+'/'+"cookies.pkl", "rb"))
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            time.sleep(random.randint(1,3))
        else:
            username = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
            password = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))
            username.clear()
            username.send_keys(self.mUser)
            time.sleep(random.randint(1,3))
            password.clear()
            password.send_keys(self.mPassw)
            time.sleep(random.randint(1,3))
            # login button
            Login_button = WebDriverWait(self.driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
            time.sleep(10)
            # click not turn off notification, there are 2 cases for this task, will use the try except to handle all cases can be occured.
        result = False
        self.driver.get("https://www.instagram.com")
        time.sleep(2)
        try:
            notnow3 = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]")))
            notnow3.click()
            result = True
        except:
            notnow2 = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div/div/div/div")))
            notnow2.click()
            time.sleep(random.randint(1, 3))
            result = True
        try:
            notnow3 = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]")))
            notnow3.click()
            result = True
        except:
            time.sleep(random.randint(1,3))
        if result == True:
            self.isLogin=True
            self.saveCookies()
        else:
            print("cannot login")
        return result
    def saveCookies(self):
        try:
            pickle.dump(self.driver.get_cookies(),open(self.mPath+'/'+"cookies.pkl","wb"))
        except:
            print("cannot save cookies, the error is below")
            print(NameError)
    def isCookies(self):
        return os.path.isfile(self.mPath+'/'+"cookies.pkl")

    def nexPost(self):
        try:
            nextPost = self.driver.find_elements(By.CSS_SELECTOR, "svg[aria-label='Next']")
            print("number of next button in post is ",len(nextPost))
            if len(nextPost) > 1:
                nextPost[1].click()
            else:
                nextPost[0].click()
            return True
        except:
            print("cannot click nextPost,try to using scroll down")
            self.nextPost2()
            return False
    # sometime,we need to nextpost by using scroll down
    def nextPost2(self):
        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(2)

    def downloadPost(self):
        # go to url link of hastag search:
        noHastag = len(self.mHastagsSearch)
        randInd = random.randint(0,noHastag-1)
        self.driver.get("https://www.instagram.com/explore/tags/"+self.mHastagsSearch[randInd]+'/')
        time.sleep(2)
        # click to first thumbnail
        result = False
        time.sleep(random.randint(1,5))
        WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.CLASS_NAME,"_aagv")))
        thumnails = self.driver.find_elements(By.CSS_SELECTOR,"div[class^='x9f619']")
        count =len(thumnails)
        if count != 0:
            # need to be random for the first click
            thumnails[0].click()
            # time.sleep(30)
            for i in range(count):
                print(self.driver.current_url)
                WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span[class^='html-span']")))
                noOfLike = self.driver.find_elements(By.CSS_SELECTOR, "span[class^='html-span xdj266r']")
                time.sleep(2)
                print(len(noOfLike))
                for k in noOfLike:
                    print(k.text)
                try :
                    if len(noOfLike) >= 3 :
                        print("noOfLike is ",noOfLike[2].text)
                        if convertStringToInt(noOfLike[2].text)>200:
                            print("noOflike is ",noOfLike[2].text)
                            downloadVideo.downloadPost(self.L,self.driver.current_url)
                            break
                        else:
                            print("the noOfLike < 500")
                            self.nexPost()
                    else:
                        print("This post is not show noof like ")
                        if i == 10:
                            print("already check 10 posts, still download")
                            downloadVideo.downloadPost(self.L, self.driver.current_url)
                            break
                        self.nexPost()
                        time.sleep(random.randint(1,5))
                except:
                    print("there is an error when get like")
                    print(NameError)
        else :
            print("there is no thumnail is get")

        return result
    def genHastagRand(self):
        noHastag = len(self.mHastagsSearch)
        print("there are ", len(self.mHastagsSearch), " to search")
        randInd = random.randint(0, noHastag - 1)
        mHastagRandom = "#"
        mHastagRandom = mHastagRandom + self.mHastagsSearch[randInd]
        return mHastagRandom
    def goToHastag(self):
        mHastagRandom = self.genHastagRand()
        self.driver.get("https://www.instagram.com")
        # push button search
        searchButton = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "svg[aria-label='Search']")))
        searchButton.click()
        # get and fill the input
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[aria-label='Search input']")))
        inputSearch = self.driver.find_element(By.CSS_SELECTOR, "input[aria-label='Search input']")
        inputSearch.send_keys(mHastagRandom)
        time.sleep(2)
        # click to the hastag
        # WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.LINK_TEXT,mHastagRandom)))
        listHastag = self.driver.find_elements(By.CSS_SELECTOR, "span[class^='x1lliihq']")
        result = False
        for mHastag in listHastag:
            try:
                print(mHastag.text)
                if mHastag.text == mHastagRandom:
                    try:
                        mHastag.click()
                        WebDriverWait(self.driver, 10).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, "div[class^='x9f619']")))
                        result =True
                        break
                    except:
                        print("cannot click with this element")
                        continue
            except:
                continue
        time.sleep(5)
        return result
    def goToHastag2(self):
        noHastag = len(self.mHastagsSearch)
        randInd = random.randint(0, noHastag - 1)
        self.driver.get("https://www.instagram.com/explore/tags/" + self.mHastagsSearch[randInd] + '/')
        return True
    def downloadPost2(self):
        # go to url link of hastag search:
        if self.goToHastag2() == False:
            print("cannot go to this hastag")
            return False
        # click to first thumbnail
        result = False
        time.sleep(5)
        WebDriverWait(self.driver,20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"div[class^='x9f619']")))
        thumnails = self.driver.find_elements(By.CSS_SELECTOR,"div[class^='x9f619']")
        count =len(thumnails)
        if count != 0:
            # need to be random for the first click
            thumnails[0].click()
            for ranI in range(random.randint(0,10)):
                if self.nexPost() == False:
                    # self.driver.refresh()
                    print("currently do nothing")
                time.sleep(1)
            # time.sleep(30)
            for i in range(count):
                print(self.driver.current_url)
                WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span[class^='html-span']")))
                noOfLike = self.driver.find_elements(By.CSS_SELECTOR, "span[class^='html-span xdj266r']")
                time.sleep(2)
                print(len(noOfLike))
                # for k in noOfLike:
                #     print(k.text)
                try :
                    if len(noOfLike) >= 2 :
                        print("noOfLike is ",noOfLike[len(noOfLike)-1].text)
                        if convertStringToInt(noOfLike[len(noOfLike)-1].text)>200:
                            print("noOflike is ",noOfLike[len(noOfLike)-1].text)
                            # will set the folder of instaloader again because after download , the folder is change
                            self.L.dirname_pattern = self.mPath + '/'
                            result=downloadVideo.downloadPost(self.L,self.driver.current_url)
                            break
                        else:
                            print("the noOfLike < 300")
                            self.nexPost()
                    else:
                        print("This post is not show noof like ")
                        if i == 10:
                            print("already check 10 posts, still download")
                            # will set the folder of instaloader again because after download , the folder is change
                            self.L.dirname_pattern = self.mPath + '/'
                            result= downloadVideo.downloadPost(self.L, self.driver.current_url)
                            break
                        self.nexPost()
                        time.sleep(random.randint(1,5))
                except:
                    print("there is an error when get like")
                    print(NameError)
        else :
            print("there is no thumnail is get")

        return result
    def inputToPopUp(self,filePath):
        # there is an issue when write , so we will write the first
        # first character and delete it before write the correct filePath
        print("start write caption")
        pyautogui.typewrite("a", interval=0.05)
        pyautogui.press('backspace')
        pyautogui.typewrite(filePath, interval=0.05)
        time.sleep(2)
        pyautogui.press('enter')
        time.sleep(2)
    def getFileToPost(self,isVideo):
        print("get file path to post")
        fileToPost =""
        while len(fileToPost)==0:
            print("fileToPost still empty,fill the infor again")
            anyVideo = False
            if isVideo == True:
                folderToPost = self.mPath + "/video/"
                if os.path.isdir(folderToPost) == False:
                    print("the folder is not exist")
                    return fileToPost
                for files in glob.glob(folderToPost + "*.mp4"):
                    fileToPost = files
                    anyVideo = True
                    return fileToPost
            else:
                folderToPost = self.mPath + "/image/"
                if os.path.isdir(folderToPost) == False:
                    print("the folder is not exist")
                    return fileToPost
                # handle the case that there still had a video in the image folder
                for files in glob.glob(folderToPost + "*.mp4"):
                    fileToPost = files
                    anyVideo = True
                    return fileToPost
                if anyVideo == False:
                    for files in glob.glob(folderToPost + "*.jpg"):
                        fileToPost = files
                        return fileToPost
            time.sleep(2)
        return fileToPost
    def followThePeople(self):
        self.goToHastag()
    def nextButtonWhenPost(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[role='button']")))
        next1 = self.driver.find_elements(By.CSS_SELECTOR, "div[role='button']")
        for nex in next1:
            try:
                if nex.text == "Next":
                    nex.click()
                    return True
            except:
                continue
        return False
    def checkButtonOk(self):
        try :
            WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"button[type='button']")))
            buttonOk = self.driver.find_elements(By.CSS_SELECTOR, "button[type='button']")
            for btt in buttonOk:
                if btt.text == "OK":
                    btt.click()
        except:
            print("there is no button Ok for video")
    def pasteContent(self,caption,action):
        pyperclip.copy(caption)
        action.key_down(Keys.CONTROL).send_keys("v").key_up(Keys.CONTROL).perform()
    def finishTask(self):
        self.driver.close()
    def postTheNewPost(self,isVideo):
        print("start to post")
        folderToPost =""
        if isVideo == True:
            folderToPost = self.mPath+"/video/"
        else:
            folderToPost = self.mPath+"/image/"
        # will get caption on the begin of function to check the caption is English or not
        captions = util.getCaption(folderToPost, self.mHastagsPost, self.mUser)
        if captions[0] == "NotEnglish":
            shutil.rmtree(folderToPost)
            self.postTheNewPost(self.downloadPost2())
            return True
        fileToPost = self.getFileToPost(isVideo)
        if len(fileToPost)>0:
            print(fileToPost)
        else:
            print("get file to post fail,delete folder to repost in the next time")
            shutil.rmtree(folderToPost)
            return
        self.driver.get("https://www.instagram.com/")
        # time.sleep(100)
        create = WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"svg[aria-label='New post']")))
        create.click()
        time.sleep(1)
        try:
            postbtt2 = WebDriverWait(self.driver,5).until(EC.element_to_be_clickable((By.LINK_TEXT,"Post")))
            postbtt2.click()
        except:
            print("there is no button post when create new post")
        time.sleep(2)
        # don't need to use button select from computer, instead of that, we will use send_key to send the path
        # WebDriverWait(self.driver,20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"button[type='button']")))
        # buttonToPost = self.driver.find_elements(By.CSS_SELECTOR,"button[type='button']")
        # for btt in buttonToPost:
        #     if btt.text == "Select from computer":
        #         print("there is a button select from computer")
        #         btt.click()
        filePath = util.correctFolderName2(fileToPost)
        print("file path to post is ",filePath)
        # self.inputToPopUp(filePath)
        inputPath = self.driver.find_elements(By.CSS_SELECTOR,"input[accept^='image/jpeg']")
        print("number of input Path = ",len(inputPath))
        try:
            inputPath[0].send_keys(filePath)
        except:
            print("cannot send path to choose file to post ",len(inputPath))
            return
        time.sleep(2)
        self.checkButtonOk()
        # need to press nextButton 2 times
        for i in range(2):
            if self.nextButtonWhenPost() == False:
                self.checkButtonOk()
                self.nextButtonWhenPost()

        WebDriverWait(self.driver,15).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"div[aria-label='Write a caption...']")))
        textCaption = self.driver.find_element(By.CSS_SELECTOR,"div[aria-label^='Write a caption']")
        textCaption.click()
        for cap in captions:
            try:
                print(cap)
                textCaption.send_keys(cap)
            except:
                # self.driver.execute_script(JS_ADD_TEXT_TO_INPUT,textCaption,cap)
                action = ActionChains(self.driver)
                self.pasteContent(cap,action)
        shares = self.driver.find_elements(By.CSS_SELECTOR,"div[role='button']")
        for share in shares:
            if share.text=="Share":
                share.click()
                break
        needToWait = True
        while needToWait==True:
            print("need to wait more 5s for post successfully")
            time.sleep(5)
            successPost = self.driver.find_elements(By.CSS_SELECTOR, "span[class^='x1lliihq']")
            for i in successPost:
                if i.text =="Your post has been shared." or i.text=="Your reel has been shared.":
                    needToWait = False
                    break
        print("The new post is created successfully,remove folder")
        shutil.rmtree(folderToPost)
        time.sleep(10)
        # self.driver.close()
        return True
    def fillTheCaption(self):
        folderToPost = self.mPath + "/caption/"
        captions = util.getCaptionToFillPOD(folderToPost, self.mHastagsPost, self.mUser)
        WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div[aria-label='Write a caption...']")))
        textCaption = self.driver.find_element(By.CSS_SELECTOR, "div[aria-label^='Write a caption']")
        textCaption.click()
        for cap in captions:
            try:
                print(cap)
                textCaption.send_keys(cap)
            except:
                # self.driver.execute_script(JS_ADD_TEXT_TO_INPUT,textCaption,cap)
                action = ActionChains(self.driver)
                self.pasteContent(cap, action)


path1 = "C:/Users/Admin/Desktop/code/code_python/listData/"
listAccount=[]
isAccountAdded={}
def updateListAccount():
    for acc in glob.glob(path1+"*.json"):
        info = open(acc)
        data = json.load(info)
        mUser = data["accountUser"]
        mPassword = data["password"]
        mHastagsSearch=data["hastagToSearch"]
        mHastagsPost = data["hastagToPost"]
        try:
            if isAccountAdded[mUser] == True:
                continue
        except:
            isAccountAdded[mUser]=True
        acc1 = account(mUser,mPassword,mHastagsSearch,mHastagsPost)
        listAccount.append(acc1)
        print("find a new account ",acc1.mUser)
def getEachAcc(userName):
    for acc in listAccount:
        if acc.mUser == userName:
            return acc
def postForAllAccount():
    print("Start post all with ",len(listAccount)," account")
    j =0
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

appStop = False
updateListAccount()
print("List the action as below: ")
i = 1
while True:
    t1 = threading.Thread(target=postForAllAccount, name="postAll")
    t2 = threading.Thread(target=handlingThePost, name="postManually")
    t3 = threading.Thread(target=postForEachAcc, name="postForEachAcc")
    listThread = []
    listThread.append(t1)
    listThread.append(t2)
    listThread.append(t3)
    i=1
    for mThread in listThread:
        print(i, ":", mThread.name)
        i = i + 1
    print(i,": exit")
    indThread = int(input("Choose the thread will be run:"))
    if indThread==4:
        break
    listThread[indThread-1].start()
    listThread[indThread-1].join()


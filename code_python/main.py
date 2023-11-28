import time
import webbrowser
import random
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome import service
from selenium.webdriver.chrome.options import Options
# pickle is used to save the cookies
import os,pickle
import downloadVideo,instaloader
import glob
# pyautogui is usded to handle popup
import pyautogui,shutil,json,threading

import util

path = "C:/Users/Admin/Desktop/code/code_python/listAccount"
if os.path.isdir(path) == False:
    os.mkdir(path)
def convertStringToInt(s):
    size =len(s)
    temp=""
    for i in s:
        if i!=',':
            temp=temp+i
        if i =='K':
            temp = temp+"000"
            break
    return int(temp)
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

        # Turn-off userAutomationExtension
        self.options .add_experimental_option("useAutomationExtension", False)
        # self.driver = webdriver.Chrome(options=options)
        # self.driver.get("https://www.instagram.com")
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
            time.sleep(100)
            # click not turn off notification, there are 2 cases for this task, will use the try except to handle all cases can be occured.
        result = False
        self.driver.get("https://www.instagram.com")
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
            nextPost = self.driver.find_elements(By.CSS_SELECTOR, "button[class='_abl-']")
            if len(nextPost) > 1:
                nextPost[1].click()
            else:
                nextPost[0].click()
        except:
            print("cannot click nextPost")
            print(NameError)
    def downloadPost(self):
        # go to url link of hastag search:
        noHastag = len(self.mHastagsSearch)
        randInd = random.randint(0,noHastag-1)
        self.driver.get("https://www.instagram.com/explore/tags/"+self.mHastagsSearch[randInd]+'/')
        time.sleep(10)
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
                # for k in noOfLike:
                #     print(k.get_attribute("textContent"))
                try :
                    if len(noOfLike) >= 2 :
                        print("noOfLike is ",noOfLike[1].text)
                        if convertStringToInt(noOfLike[1].text)>500:
                            print("noOflike is ",noOfLike[1].text)
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
    def inputToPopUp(self,filePath):
        # there is an issue when write , so we will write the first
        # first character and delete it before write the correct filePath
        pyautogui.typewrite("a", interval=0.05)
        pyautogui.press('backspace')
        pyautogui.typewrite(filePath, interval=0.05)
        time.sleep(2)
        pyautogui.press('enter')
        time.sleep(2)
    def postTheNewPost(self,isVideo):
        print("start to post")
        folderToPost =""
        fileToPost =""
        anyVideo = False
        if isVideo == True:
            folderToPost = self.mPath+"/video/"
            for files in glob.glob(folderToPost+"*.mp4"):
                fileToPost = files
                anyVideo=True
                break
        else:
            folderToPost = self.mPath+"/image/"
            # handle the case that there still had a video in the image folder
            for files in glob.glob(folderToPost+"*.mp4"):
                fileToPost = files
                anyVideo=True
                break
            if anyVideo ==False:
                for files in glob.glob(folderToPost+"*.jpg"):
                    fileToPost = files
                    break
        print(fileToPost)
        self.driver.get("https://www.instagram.com/")
        # time.sleep(100)
        create = WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"svg[aria-label='New post']")))
        create.click()
        time.sleep(2)
        WebDriverWait(self.driver,20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"button[type='button']")))
        buttonToPost = self.driver.find_elements(By.CSS_SELECTOR,"button[type='button']")
        for btt in buttonToPost:
            if btt.text == "Select from computer":
                btt.click()
        filePath = util.correctFolderName2(fileToPost)
        print(filePath)
        self.inputToPopUp(filePath)
        if anyVideo == True:
            time.sleep(20)
        try :
            WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"button[type='button']")))
            buttonOk = self.driver.find_elements(By.CSS_SELECTOR, "button[type='button']")
            for btt in buttonOk:
                if btt.text == "OK":
                    btt.click()
        except:
            print("there is Ok for video")
        next1 = self.driver.find_elements(By.CSS_SELECTOR,"div[role='button']")
        for nex in next1:
            if nex.text == "Next":
                nex.click()
                break
        next2 = self.driver.find_elements(By.CSS_SELECTOR, "div[role='button']")
        for nex in next2:
            if nex.text == "Next":
                nex.click()
                break
        captions = util.getCaption(folderToPost,self.mHastagsPost)
        try:
            WebDriverWait(self.driver,15).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"div[aria-label='Write a caption...']")))
            textCaption = self.driver.find_element(By.CSS_SELECTOR,"div[aria-label='Write a caption...']")
            for cap in captions:
                try:
                    textCaption.send_keys(cap)
                except:
                    continue
        except:
            print("cannot get a text caption")
            return False
        shares = self.driver.find_elements(By.CSS_SELECTOR,"div[role='button']")
        for share in shares:
            if share.text=="Share":
                share.click()
                break
        time.sleep(10)
        print("The new post is created successfully,remove folder")
        shutil.rmtree(folderToPost)
        time.sleep(20)
        self.driver.close()
        return True
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
    for acc in listAccount:
        # if acc.mUser == "fanaccount_rowing":
        #     continue
        if acc.mUser=="fanlove_yelowstone" and  acc.login()==True:
            # acc.downloadPost()
            acc.postTheNewPost(acc.downloadPost())
        # time.sleep(random.randint(200,600))
appStop = False
updateListAccount()
t1 = threading.Thread(target=postForAllAccount(),name="postAll")
t1.start()




import time

import pyperclip
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC



JS_ADD_TEXT_TO_INPUT = """
  var elm = arguments[0], txt = arguments[1];
  elm.value += txt;
  elm.dispatchEvent(new Event('change'));
  """
texts = ["Paddling on a sunny day in Livigno ☀️",
"Credit: rambo.luca"
"Follow @rowinghantos",
"What is your favorite shirt⁠",
"💥 𝗦𝗛𝗢𝗣 𝗡𝗢𝗪 🔥𝗟𝗜𝗡𝗞 𝗜𝗡 𝗠𝗬 𝗕𝗜𝗢 👆🏻 𝗦𝗵𝗶𝗽𝗽𝗶𝗻𝗴 ✈️⁠"]

class test:
    def __init__(self,mNumS):
        self.num = mNumS
        self.driver = webdriver.Chrome()
        self.driver.get("https://www.instagram.com")
    def login(self):
        username = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
        username.click()
        password = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))
        for text in texts:
            try:
                username.send_keys(text)
            except:
                pyperclip.copy(text)
                action = ActionChains(self.driver)
                action.key_down(Keys.CONTROL).send_keys("v").key_up(Keys.CONTROL).perform()
        time.sleep(10)

a1 = test(10)
a1.login()
time.sleep(10)
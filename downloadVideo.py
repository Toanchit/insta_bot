import requests
from bs4 import BeautifulSoup
import shutil
import re,string
import instaloader
from instaloader import Post
import util
def downloadPost(L,urlLink):
    print("shortCode = ",util.convertUrlToShortCode(urlLink))
    post = Post.from_shortcode(L.context,util.convertUrlToShortCode(urlLink))
    print(post.is_video)
    if post.is_video == True:
        downloadvideo(L,post)
        return True
    else:
        downloadImage(L,post)
        return False
def downloadvideo(L,post):
    temPattern = L.dirname_pattern
    L.dirname_pattern = L.dirname_pattern+"video/"
    L.download_post(post,"video")
    L.dirname_pattern = temPattern
def downloadImage(L,post):
    temPattern = L.dirname_pattern
    L.dirname_pattern = L.dirname_pattern + "image/"
    L.download_post(post,"image")
    L.dirname_pattern = temPattern


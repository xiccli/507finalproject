#import needed modules
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
#

### PART 1. Make Request WWF All Species page
print ("\n ********* PART 1*********")
print ("WWF - Get Species' Info")

### "download" species information from species directory page
driver=webdriver.Chrome("")
driver.get("https://medium.com/topic/digital-design")
time.sleep(2)

def execute_times(times):
    for i in range(times + 1):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
execute_times(4)

html=driver.page_source
soup=BeautifulSoup(html,"html.parser")
get_title=soup.find_all(class_="u-flexColumnTop u-flexWrap u-overflowHidden u-absolute0 u-xs-relative")
for each in getall:
    get_atag=get_title.find("a")
    url_each=get_atag["data-post-id"]
    print (url_each)

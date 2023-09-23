from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import os
import pickle
from time import sleep

def readData(fileName):
    f = open(fileName, 'r', encoding='utf-8')
    data = []
    for i, line in enumerate(f):
        line = repr(line)
        line = line[1:len(line) - 3]
        data.append(line)
    return data

def writeFile(fileName, content):
    with open(fileName, 'a', encoding='utf-8') as f1:
        f1.write(content + os.linesep)
# Hàm lấy cookies chỉ cần đăng nhập 1 lần
def get_cookies(driver,path):
    # 1. Mở trang facebook 
    driver.get("https://facebook.com/")
    # 2.Điền username và password thật của tài khoản facebook
    txtUser = driver.find_element(By.ID,"email")
    txtUser.send_keys("username")
    sleep(10)
    txtPass = driver.find_element(By.ID,"pass")
    txtPass.send_keys("password")
    # 3.Đăng nhập 
    txtPass.send_keys(Keys.ENTER)
    sleep(5)
    pickle.dump(driver.get_cookies(), open(path,"wb"))
    driver.close()

# Khởi tạo một webdriver trên máy (sử dụng Chrome)
def Setup():
    options = Options()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    browser = webdriver.Chrome("C:/Users/VQ/Downloads/chromedriver_win32/chromedriver.exe", chrome_options=options) 
    return browser

# Đăng nhập Facebook bằng cookies
def loginFacebookByCookies(driver,path):
    # 1. open Facebook
    driver.get("http://facebook.com")
    # 2.Load cookie from file
    cookies = pickle.load(open(path,"rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)

# Lấy ID của bài đăng cụ thể 
def getPostIds(driver,allPosts):
    sleep(2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    shareBtn = driver.find_elements(By.XPATH,'//a[contains(@href, "/sharer.php")]')
    if (len(shareBtn)):
        for link in shareBtn:
            postId = link.get_attribute('href').split('sid=')[1].split('&')[0]
            #print(postId)
            if postId not in allPosts:
                allPosts.append(postId)
    return allPosts
# Lấy text của dòng comment
def getComment(driver):
    try:
        comments_of_a_post = []
        links = driver.find_elements(By.XPATH,'//a[contains(@href, "comment/replies")]')
        ids = []
        if (len(links)):
            for link in links:
                sleep(5)
                takeLink = link.get_attribute('href').split('ctoken=')[1].split('&')[0]
                CommentElement = driver.find_element(By.XPATH,('//*[@id="' + takeLink.split('_')[1] + '"]/div/div[1]'))
                if (takeLink not in ids):
                    comments_of_a_post.append(CommentElement.text)
                    ids.append(takeLink)
        return ids, comments_of_a_post
    except:
        print("error get link")

# Thực hiện crawl comments từ mỗi bài post
def getCommentsfromPosts(driver, postId, numberComment, comments):
    print('Start to crawl comments')
    try:
        sleep(5)
        driver.get("https://mbasic.facebook.com/" + str(postId))
        sumLinks, comments_of_a_post = getComment(driver)
        comments.append(comments_of_a_post)
        while(len(sumLinks) < numberComment):
            try:
                sleep(2)
                nextBtn = driver.find_elements(By.XPATH,'//*[contains(@id,"see_next")]/a')
                if (len(nextBtn)):
                    nextBtn[0].click()
                    sumLink, comment_of_a_post = getComment(driver)
                    comments.append(comment_of_a_post)
                    sumLinks.extend(sumLink)
                else:
                    break
            except:
                print('Error while trying to crawl comments')
        return comments
    except:
        print("Error to get comments")
    print('Done')

posts = []
comments = []
cookies = "C:/Users/VQ/Downloads/my_cookie.pkl"
# cookies = "C:/Users/VQ/Donwloads/cookies.pkl"
browser = Setup()

# Lấy cookies và đăng nhập Facebook 
# get_cookies(browser,cookies) # --> Chỉ chạy 1 lần để lấy file cookies của tài khoản log in 

loginFacebookByCookies(browser,cookies)

# Tìm ID của các bài đăng 
n = 5
browser.get("https://touch.facebook.com/" + 'UITconfess')
while len(posts)<n:
    posts.append(getPostIds(browser,posts))
print(posts)

# Duyệt qua từng id của bài post
for postId in posts:
    comments.append(getCommentsfromPosts(browser, postId, 10,comments))
print(comments)
# Lưu dữ liệu đã crawl về
Posts = 'C:/Users/VQ/Desktop/CS232-TTDPT/Lab 1/Crawl Post and Comment from Facebook/posts.csv'
for post in posts:
    writeFile(Posts,post)
Comments = 'C:/Users/VQ/Desktop/CS232-TTDPT/Lab 1/Crawl Post and Comment from Facebook/comments.csv'
a = {'List comments': comments}
pd.DataFrame(a).to_csv(Comments)
browser.close()
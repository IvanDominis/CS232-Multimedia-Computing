from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import random
import pickle
def loginFacebookByCookies(driver,path):
    # 1. open Facebook
    driver.get("http://facebook.com")
    # 2.Load cookie from file
    cookies = pickle.load(open(path,"rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
    # 3. Refresh the browser
    driver.get("http://facebook.com")
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
browser = webdriver.Chrome(executable_path="C:/Users/VQ/Downloads/chromedriver_win32/chromedriver.exe",options=options)
path = "C:/Users/VQ/Downloads/my_cookie.pkl"
# get_cookies(driver,path)
loginFacebookByCookies(browser,path)
# Này là nhấp bất kì trên màn hình, để tắt thông báo của facebook
# x, y = 100, 200
# actions = ActionChains(browser)
# sleep(5)
# actions.move_by_offset(x, y).click().perform()
browser.get("https://www.facebook.com/UITconfess/posts/pfbid0EWcBYpv6H99GcoYT5gUvpCBPAmCTQHopEbRZwqmg2biX6T7B7J5bWridDMM2MBcml")

for _ in range(2): 
        try:
            browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            showmore_button = browser.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div/div/div/div/div/div/div/div/div/div/div/div[2]/div/div/div[4]/div/div/div[2]/div[4]/div[1]/div[2]/span') 
            showmore_button.click() 
            sleep(3)
        except:
            break

comment_list = browser.find_elements(By.XPATH, '//div[starts-with(@aria-label,"Bình luận dưới tên")]')

for comment in comment_list:
    comment_text = comment.text
    print(comment_text)
browser.close()
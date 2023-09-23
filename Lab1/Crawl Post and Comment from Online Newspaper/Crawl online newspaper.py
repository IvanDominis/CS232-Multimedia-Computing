from selenium import webdriver
from selenium.webdriver.common.keys  import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import csv
import pandas as pd

def take_comment(driver,link,num_comment):
    print('Start to get comments!')
    driver.get(link)
    page_source = BeautifulSoup(driver.page_source,'html.parser')
    time.sleep(2)
    commenters = []
    comments = []
    cters = page_source.find_all('b')
    cts = page_source.find_all('p', class_='full_content')
    count = 0
    for ct in cts:
        if count==num_comment: break
        comments.append(ct.span.next_sibling.strip())
        count+=1
    for cter in cters:
        if count==num_comment*2: break
        commenters.append(cter.text)
        count+=1
    print('Finished!')
    return commenters,comments
    # driver.close()

driver = webdriver.Chrome(executable_path="C:/Users/VQ/Downloads/chromedriver_win32/chromedriver.exe")
path = 'C:/Users/VQ\Desktop/CS232-TTDPT/Lab 1/Crawl Post and Comment from Online Newspaper/data.csv'
url = 'https://vnexpress.net/'
driver.get(url)
num_article = 5
num_comment = 10

# Get element article
page_source = BeautifulSoup(driver.page_source,'html.parser')
title_articles = page_source.find_all('h3', class_ = "title-news")
# Get title name and link 
list_link = []
list_title = []
list_comments = []
list_authors = []
for element in title_articles:
    list_title.append(element.find('a').get('title'))
    list_link.append(element.find('a').get('href'))

# Get all element comments
for link in list_link[:min(len(list_link),  num_article)]:
    cters,cts = take_comment(driver,link,num_comment)
    list_comments.append(cts)
    list_authors.append(cters)
driver.close()
# Save data to file .csv
df = pd.DataFrame()
for i in range(num_article):
    new_row = {'Post':list_link[i],'Name of author':list_authors[i][0],'Comment':list_comments[i][0] }
    df = df.append(new_row, ignore_index=True)
    n = min(len(list_comments[i]),num_comment)
    for j in range(1,n):
        print(j,n)
        print(list_authors[i][j],': ',list_comments[i][j])
        new_row = {'Name of author':list_authors[i][j],'Comment':list_comments[i][j] }
        df = df.append(new_row, ignore_index=True)
df.to_csv(path,index = False, encoding = 'utf-8-sig')

# fieldnames = ['Post','Name of author','Comment']
# with open(path, 'w', encoding='utf-8-sig', newline='') as f:
#     writer = csv.DictWriter(f,fieldnames)
#     writer.writeheader()
#     for i in range(num_article):
#         writer.writerow({'Post':list_link[i],'Name of author':list_authors[i][0],'Comment':list_comments[i][0] })
#         for j in range(1,num_comment):
#             writer.writerow({'Name of author':list_authors[i][j],'Comment':list_comments[i][j] })



from selenium.webdriver import Chrome
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select

import sqlite3 as sql

import time 
import os

conn = sql.connect("views.db")
#items = [i for i in cur.execute('SELECT hash, title from items limit 50;').fetchall()]
cur = conn.cursor()
cur.execute('CREATE TABLE nana (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, length INTEGER, views INTEGER, link TEXT);')

os.environ['PATH'] += r"C:\Users\USER\Desktop\Webscraper\webdrivers\chromedriver.exe"

driver =  Chrome()
driver.get('https://www.youtube.com/@TechWorldwithNana/videos')

for i in range(50):
    driver.execute_script("window.scrollBy(0,600)")
    time.sleep(.75)

time.sleep(5)

title = [i.text for i in driver.find_elements(By.ID, 'video-title')]
link = [i.get_attribute('href') for i in driver.find_elements(By.CSS_SELECTOR, 'a[id=video-title-link]')]
temp_views = [i.text.split('\n')[0].split()[0] for i in driver.find_elements(By.ID, 'metadata-line')]

length = []
for i in filter(lambda x: x != '', [i.text for i in driver.execute_script("return document.querySelectorAll('div[id=time-status]')")]): 
    i = i.split(':')
    if len(i) == 3:
        ii = int(i[0])*3600 + int(i[1])*60 + int(i[2])
    elif len(i) == 2:
        ii = int(i[0])*60 + int(i[1])
    length.append(ii)

views = []
for i in temp_views:
    if i.endswith('M'):
       views.append(int(float(i[:-1])*1_000_000))
    elif i.endswith('K'):
       views.append(int(float(i[:-1])*1_000))
    else:
        views.append(int(i))
del temp_views

for i in zip(title, length, views, link):
    cur.execute('INSERT INTO nana (title, length, views, link) VALUES (? ,?, ? ,?)', (i[0], i[1], i[2], i[3]))
    conn.commit()
    print(i[0], i[1], i[2], i[3])

conn.close()
time.sleep(5)
driver.quit()

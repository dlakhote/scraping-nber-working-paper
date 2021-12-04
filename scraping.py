import requests
from bs4 import BeautifulSoup
import time
import os
import codecs
from urllib.parse import urljoin

import chromedriver_binary
from selenium import webdriver


def page_transition():

    URL = ''
    for i in range(1, 8):
        URL = 'https://www.nber.org/papers?endDate=2021-12-04T00%3A00%3A00%2B09%3A00&facet=topics%3ALabor%20Economics&page=' + str(i) + '&perPage=100&sortBy=public_date&startDate=2020-04-01T00%3A00%3A00%2B09%3A00'
        
        scraping_nber(URL)



def scraping_nber(URL):
        #    https://www.nber.org/papers?endDate=2021-12-04T00%3A00%3A00%2B09%3A00&facet=topics%3ALabor%20Economics&page=2&perPage=100&sortBy=public_date&startDate=2020-04-01T00%3A00%3A00%2B09%3A00
        #    https://www.nber.org/papers?endDate=2021-12-04T00%3A00%3A00%2B09%3A00&facet=topics%3ALabor%20Economics&page=1&perPage=100&sortBy=public_date&startDate=2020-04-01T00%3A00%3A00%2B09%3A00

    TITLE_CLASS_NAME = 'digest-card__title'

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')

    driver = webdriver.Chrome(options=options)
    driver.get(URL)

    time.sleep(5)

    html = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html, 'html.parser')
    titles = soup.find_all(class_ = TITLE_CLASS_NAME)
    titles_page1 = [0]*100
    links_page1 = [0]*100

    # title 1-100 | len(titles)=101 
    # link example https://www.nber.org/papers/w29177
    for i in range(1, 101): 
        titles_page1[i - 1] = titles[i].get_text()

        link = titles[i].find('a')
        links_page1[i - 1] = "https://www.nber.org/" + link.get('href')
    
    # print(titles_page1)
    # print(links_page1)


scraping_nber()
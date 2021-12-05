# reference: https://qiita.com/ulwlu/items/c84501993635c72540a7

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import chromedriver_binary

options = Options()
options.add_argument("--disable-gpu")
options.add_argument("--disable-extensions")
options.add_argument("--proxy-server='direct://'")
options.add_argument("--proxy-bypass-list=*")
options.add_argument("--start-maximized")
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

def page_transition():

    URL = ''
    
    # dict = {
    #     'titles_page1' : [titles_list page1],
    #     'links_page1' : [links_list page1],
    #     ...
    # }
    working_papers = dict()


    for i in range(1, 8):
        URL = 'https://www.nber.org/papers?endDate=2021-12-04T00%3A00%3A00%2B09%3A00&facet=topics%3ALabor%20Economics&page=' + str(i) + '&perPage=100&sortBy=public_date&startDate=2020-04-01T00%3A00%3A00%2B09%3A00'
        
        titles_list, links_list = scraping_nber(URL)

        working_papers['titles_page' + str(i)] = titles_list
        working_papers['links_page' + str(i)] = links_list



def scraping_nber(URL):
        #    https://www.nber.org/papers?endDate=2021-12-04T00%3A00%3A00%2B09%3A00&facet=topics%3ALabor%20Economics&page=2&perPage=100&sortBy=public_date&startDate=2020-04-01T00%3A00%3A00%2B09%3A00
        #    https://www.nber.org/papers?endDate=2021-12-04T00%3A00%3A00%2B09%3A00&facet=topics%3ALabor%20Economics&page=1&perPage=100&sortBy=public_date&startDate=2020-04-01T00%3A00%3A00%2B09%3A00

    TITLE_CLASS_NAME = 'digest-card__title'

    driver.get(URL)
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.' + TITLE_CLASS_NAME))
    )

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    titles = soup.find_all(class_ = TITLE_CLASS_NAME)
    num_of_papers = len(titles) - 1
    titles_list = [0]*num_of_papers
    links_list = [0]*num_of_papers

    # title 1-100 | len(titles)=101 
    # link example https://www.nber.org/papers/w29177

    for i in range(1, num_of_papers + 1): 
        titles_list[i - 1] = titles[i].get_text()

        link = titles[i].find('a')
        links_list[i - 1] = "https://www.nber.org/" + link.get('href')
    
    print(titles_list)
    # print(links_list)
    # return titles_list, links_list


scraping_nber('https://www.nber.org/papers?endDate=2021-12-04T00%3A00%3A00%2B09%3A00&facet=topics%3ALabor%20Economics&page=1&perPage=100&sortBy=public_date&startDate=2020-04-01T00%3A00%3A00%2B09%3A00')
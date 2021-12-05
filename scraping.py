# reference: https://qiita.com/ulwlu/items/c84501993635c72540a7

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import chromedriver_binary
import re

options = Options()
options.add_argument("--disable-gpu")
options.add_argument("--disable-extensions")
options.add_argument("--proxy-server='direct://'")
options.add_argument("--proxy-bypass-list=*")
options.add_argument("--start-maximized")
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

def main():
    page_transition()

    return 



def page_transition():

    URL = ''

    for page_num in range(1, 8):
        URL = 'https://www.nber.org/papers?endDate=2021-12-04T00%3A00%3A00%2B09%3A00&facet=topics%3ALabor%20Economics&page=' + str(page_num) + '&perPage=100&sortBy=public_date&startDate=2020-04-01T00%3A00%3A00%2B09%3A00'
        
        scraping_nber(URL, page_num)

    return



def scraping_nber(URL, page_num):

    TITLE_CLASS_NAME = 'digest-card__title'

    driver.get(URL)
    driver.set_page_load_timeout(10) # 10秒
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
    
    output_list_to_text(titles_list, page_num, 0)
    output_list_to_text(links_list, page_num, 1)

    # fetch_abstract(links_list, page_num)

    return


# code = {
#     0: titles_list,
#     1: links_list,
#     2: abstracts_list 
# }
def output_list_to_text(li, page_num, code):

    if code == 0:
        titles_list_linebreak = '\n\n'.join(li)

        titles_file_name = 'titles/titles_page' + str(page_num) + '.txt'
        with open(titles_file_name, 'w') as f:
            f.write(titles_list_linebreak)

    elif code == 1:
        links_list_linebreak = '\n\n'.join(li)

        links_file_name = 'links/links_page' + str(page_num) + '.txt'
        with open(links_file_name, 'w') as f:
            f.write(links_list_linebreak)

    else:
        abstracts_list_linebreak = '\n\n'.join(li)

        abstracts_file_name = 'abstracts/abstracts_page' + str(page_num) + '.txt'
        with open(abstracts_file_name, 'w') as f:
            f.write(abstracts_list_linebreak)

    return


def fetch_abstract(links_list, page_num):

    ABST_CLASS_NAME = 'page-header__intro-inner'

    num_of_papers = len(links_list)
    abstracts_list = [0]*num_of_papers

    for i in range(0, num_of_papers):

        link = links_list[i]

        driver.get(link)
        driver.set_page_load_timeout(10)
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'p'))
        )

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        abstract = soup.find(class_ = ABST_CLASS_NAME)

        # abstract.get_text() = '\n\n' + str + '\n'
        abstract_text = abstract.get_text()
        abstract_text = re.sub('\n', '', abstract_text)
        abstracts_list[i] = abstract_text

    output_list_to_text(abstracts_list, page_num, 2)

    return


main()
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as  EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriveC:\Users\admin\PycharmProjects\hello_word\venv\chromedriver_win32\chromedriver.exerWait
from lxml import etree
import pymongo
path = r''
option = webdriver.ChromeOptions()
option.add_argument('disable-infobars')
brower = webdriver.Chrome(executable_path=path, chrome_options=option)
brower.get('http://www.dangdang.com/')
# time.sleep(3)
waite = WebDriverWait(brower, 10)  # 显示等待


def parse():
    html = brower.page_source
    tree = etree.HTML(html)
    li_list = tree.xpath('//*[@id="component_59"]')
    for li in li_list:
        title = li.xpath('./li/a/@title')
        miaoshu = li.xpath('./li/p[@class = "detail"]/text()')
        item = {
            '标题': title,
            '描述': miaoshu,
        }
        print(item)
        return item


def get_mongo(item):
    MOGON_URL = 'localhost'
    MONGO_DB = 'dangdang'
    MONGO_COLLECTION = 'xiaoshuo'
    client = pymongo.MongoClient(MOGON_URL)
    db = client[MONGO_DB]
    collection = db[MONGO_COLLECTION]
    collection.insert(item)
def get_status():
    pass



def main():
        # input = brower.find_element(By.CSS_SELECTOR, '#key_S')
        # buttown = brower.find_element(By.CSS_SELECTOR, '#form_search_new > input.button')
        # input.send_keys('小说')
        # buttown.click()
        try:
            input = waite.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#key_S')))
            buttown = waite.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#form_search_new > input.button')))
            input.send_keys('小说')
            buttown.click()
            item = parse()
            get_mongo(item)
        except TimeoutException:
           print("请求超时")
           main()


if __name__ == '__main__':
    main()

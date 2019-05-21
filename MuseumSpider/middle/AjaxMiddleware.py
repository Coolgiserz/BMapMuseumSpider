from selenium import webdriver
from scrapy.http import HtmlResponse
import time
import random
from selenium.webdriver.chrome.options import Options

class AjaxMiddleware(object):
    def __init__(self):
        self.chrome_options = Options()
        # 设置chrome浏览器无界面模式
        self.chrome_options.add_argument('--headless')
        # driver = webdriver.Phantomjs()  # 指定使用的浏览器
        self.driver = webdriver.Chrome('/Users/zhuge/Softwares/chromedriver/chromedriver74',
                                  options=self.chrome_options)  # 264 73
    def process_request(self,request,spider):
        if spider.name == "bmuseum":

            time.sleep(random.randint(300, 600))
            self.driver.get(request.url)

            # time.sleep(1)
            # js = "var q=document.documentElement.scrollTop=10000"
            # driver.execute_script(js)  # 可执行js，模仿用户操作。此处为将页面拉至最底端。
            # time.sleep(3)
            body = self.driver.page_source
            print("访问" + request.url)
            return HtmlResponse(self.driver.current_url, body=body, encoding='utf-8', request=request)

        else:
            return None

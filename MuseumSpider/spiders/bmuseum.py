# -*- coding: utf-8 -*-
import scrapy
from MuseumSpider.items import MuseumspiderItem
import datetime
from scrapy.http import Request
from scrapy.http import HtmlResponse
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from urllib import parse
import pandas as pd
import numpy as np

'''
 Spider for crawling the museum data on BMap. 





'''
class BmuseumSpider(scrapy.Spider):

    name = 'bmuseum'
    allowed_domains = ['baike.baidu.com']
    start_urls = ['https://baike.baidu.com/museum/guojiabowuguan'] #simple
    def __init__(self):
        #加载URL列表
        self.gallerys = pd.read_excel('/Users/coolcats/PycharmProjects/GeoStatistic/MuseumSpider/json/Gallery-ori.xlsx')
        self.gallerys = self.gallerys[self.gallerys["is3d"]==0]
        self.all_urls = list(self.gallerys["domain"])# url类标，domain，URL
        # self.all_museumIds = self.gallerys["museumId"]
        self.has_crawed = set()
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_path = '/Users/zhuge/Softwares/chromedriver/chromedriver74'
        self.browser = webdriver.Chrome(chrome_path,options=chrome_options)
        self.current_url = self.all_urls.pop()
        super(BmuseumSpider,self).__init__()
        dispatcher.connect(self.spider_close,signals.spider_closed)#当spider关闭、
        print("当前URL：", self.current_url)
    def spider_close(self,spider):
        '''
        Quit the chrome when spider finish
        :param spider:
        :return:
        '''
        print("Close Chrome")
        self.browser.quit()

    def parse(self, response):
        '''
        获取百度博物馆中各地方的url并交给scrapy解析

        :param response:
        :return:
        '''
        # map_layers = response.xpath("//div[@id='mapLayer']")
        # museums_lists = response.xpath("//museum-list")


        bmuseum = MuseumspiderItem()
        museum_name = response.xpath("//span[@class='museum-name']/text()").extract_first()       #展馆名
        museum_meta = response.xpath("//span[@class='museum-abstract']/em/text()").extract()

        if museum_meta:
            gallery_num = museum_meta[0]                                                    #展览馆数
            total_collections = museum_meta[1]                                              #藏品总数
            bmuseum["total_collections"] = total_collections
            bmuseum["galleryNums"] = gallery_num
        # all_sub_museums = response.xpath("//ul[@class='list-wrap']/li")                   #子展馆列表选择器
        branchIds = response.xpath("//ul[@class='list-wrap']/li/@data-value").extract()     #子展馆ID
        branch_names = response.xpath("//ul[@class='list-wrap']/li/dl/dt/text()").extract() #子展馆名
        branch_collection_nums = response.xpath("//ul[@class='list-wrap']/li/dl/dd/span/text()").extract()#子展览馆的展品数
        branch_meta_pic_url = response.xpath("//ul[@class='list-wrap']/li//img/@src").extract()#子展馆图片

        bmuseum["mesuemName"] = museum_name
        bmuseum["mesuemUrl"] = response.url
        # bmuseum["museumId"] = museum_name

        bmuseum["saveNums"] = ','.join(branch_collection_nums)
        bmuseum["galleryNames"] = ','.join(branch_names)
        bmuseum["galleryIds"] = ','.join(branchIds)
        bmuseum["gallery_meta_image"] = ','.join(branch_meta_pic_url)

        yield bmuseum
        #提取下一个URL

        # yield Request(url=self.current_url, callback=self.parse_detail,dont_filter=True)

        if self.all_urls:
            current_domain = self.all_urls.pop()  # 随机取出一个url
            print("当前URL：", current_domain)
            yield Request(url=parse.urljoin(response.url,current_domain),callback=self.parse,dont_filter=True)

    '''暂时废弃parse_detail'''
    def parse_detail(self,response):
        bmuseum = MuseumspiderItem()
        # mesuemName = response.x  # 博物馆名 e.g.鸦片战争博物馆
        # mesuemUrl = scrapy.Field()  # 博物馆URL e.g.https://baike.baidu.com/museum/yapianzhanzheng
        # galleryName = scrapy.Field()  # 展馆名
        museum_meta = response.xpath("//span[@class='museum-abstract']/em/text()").extract()
        if museum_meta:
            gallery_num = museum_meta[0]        #展览馆数
            total_collections = museum_meta[1]  #藏品总数
        # all_sub_museums = response.xpath("//ul[@class='list-wrap']/li") #子展馆列表选择器
        branchIds = response.xpath("//ul[@class='list-wrap']/li/@data-value").extract()#子展馆ID
        branch_names = response.xpath("//ul[@class='list-wrap']/li/dl/dt/text()").extract() #子展馆名
        branch_collection_nums = response.xpath("//ul[@class='list-wrap']/li/dl/dd/span/text()").extract()#子展览馆的展品数
        branch_meta_pic_url = response.xpath("//ul[@class='list-wrap']/li//img/@src").extract()#子展馆图片

        pass
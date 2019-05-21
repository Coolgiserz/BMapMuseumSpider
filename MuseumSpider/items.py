# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MuseumspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # privinceName = scrapy.Field() #省份名  e.g.广东
    # cityName = scrapy.Field()     #城市名  e.g.深圳
    mesuemName = scrapy.Field()   #博物馆名 e.g.鸦片战争博物馆
    mesuemUrl = scrapy.Field()    #博物馆URL e.g.https://baike.baidu.com/museum/yapianzhanzheng
    museumId = scrapy.Field()      #博物馆ID
    total_collections = scrapy.Field()#藏品总数
    galleryNames = scrapy.Field()  #展馆名
    galleryNums = scrapy.Field()  #展馆数

    saveNums = scrapy.Field()      #展馆藏品数
    galleryIds = scrapy.Field()     #展馆ID
    gallery_meta_image = scrapy.Field()   #子展馆图片
    # mesuemSummary = scrapy.Field()#博物馆简介
    # mesuemImage = scrapy.Field()  #博物馆头像
    pass

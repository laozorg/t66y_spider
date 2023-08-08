# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EriccrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class BTItem(scrapy.Item):
    # index
    id = scrapy.Field()
    # 封面名称
    shortName = scrapy.Field()
    # 完整名称包含英文名，年份
    name = scrapy.Field()
    # 网页详情页url
    url = scrapy.Field()
    # 修改时间
    gmt_modify = scrapy.Field()
    # 添加时间
    gmt_create = scrapy.Field()


class BTDetailItem(scrapy.Item):
    # index
    id = scrapy.Field()
    # 完整名称包含英文名，年份
    name = scrapy.Field()
    # 评分
    score = scrapy.Field()
    # 剧情简介
    desc = scrapy.Field()
    # 网页详情页url
    url = scrapy.Field()
    # 图片链接
    imgUrl = scrapy.Field()
    # Bt下载地址
    url_bt_info = scrapy.Field()
    # 迅雷下载地址
    url_thunder_info = scrapy.Field()
    # 修改时间
    gmt_modify = scrapy.Field()
    # 添加时间
    gmt_create = scrapy.Field()

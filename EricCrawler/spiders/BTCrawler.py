# -*- coding: utf-8 -*-
import time
import redis
import re
import scrapy
import logging
from EricCrawler.items import BTItem
from EricCrawler.items import BTDetailItem
from EricCrawler.settings import REDIS_URL, REDIS_PORT, REDIS_URL_PREFIX
from ..utils.webhookutil import update_info


class BtcrawlerSpider(scrapy.Spider):
    """
    抓取比特大雄每日更新电影，后期推送到钉钉和微信公众号
    """
    name = 'BTCrawler'

    download_delay = 1
    allowed_domains = ['www.xl720.com']

    start_urls = ['https://www.xl720.com']

    def start_requests(self):
        """
        复写请求url的方法，定制相应设置
        :return: request
        """
        for url in self.start_urls:
            yield scrapy.Request(url, dont_filter=True, meta={'homePage': True})

    def parse(self, response):
        """
        网页解析内容
        :param response: 抓取的网页返回
        """
        if response.status == 200:
            # pattern=re.compile('最新电影.*？')
            film_info = response.css('.new-home-box ul li')[0:24]
            for film in film_info:
                if film.css('a::attr(href)').extract_first():
                    item = BTItem()
                    item['id'] = film.css('a::attr(href)').re(r'thunder/(\d+).html')[0]
                    item['name'] = film.css('a .posters img::attr(alt)').extract_first()
                    item['shortName'] = film.css('a .cap::text').extract_first()
                    item['url'] = film.css('a::attr(href)').extract_first()
                    item['gmt_create'] = time.time()
                    if item['url'] and self.validate_url(item['url']):
                        yield scrapy.Request(url=item['url'], callback=self.parse_detail_page)
                        yield item

    def parse_detail_page(self, response):
        """
        解析详情页
        :param response:  详情页返回
        """
        if response.status == 200:
            item = BTDetailItem()
            item['id'] = re.findall(r'thunder/(\d+).html', response.url)[0]
            item['name'] = response.css('#mainpic img::attr(alt)').get()
            item['score'] = response.css('#mainpic strong::text').get()
            item['url'] = response.url
            item['imgUrl'] = response.css('#mainpic img::attr(src)').get()
            item['desc'] = ''
            for desc_str in response.css('#link-report *::text').getall():
                item['desc'] += desc_str
            item['url_bt_info'] = {}
            for urlInfo in response.css('.down_btn_cl'):
                quality = urlInfo.css('a::attr(title)').get().split('.')[1]
                item['url_bt_info'][quality] = urlInfo.css('a::attr(href)').get()
            item['url_thunder_info'] = {}
            for urlInfo in response.css('.down_btn_xl'):
                quality = urlInfo.css('a::attr(title)').get().split('.')[1]
                item['url_thunder_info'][quality] = urlInfo.css('a::attr(href)').get()
            update_info(item)
            yield item

    def validate_url(self, url):
        """
            检测url是否已存，去重
        """
        redis_db = redis.Redis(host=REDIS_URL, port=REDIS_PORT)  # 连接redis，相当于MySQL的conn
        redis_url_prefix = REDIS_URL_PREFIX
        # # 判定主页，不加入redis
        if url not in self.start_urls:
            if redis_db.sadd(redis_url_prefix, url) == 0:
                logging.log(logging.INFO, 'Url: ' + url + '已经爬取，跳过。')
                return False
        return True

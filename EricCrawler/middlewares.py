# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
from scrapy import signals
from fake_useragent import UserAgent, FakeUserAgentError


class EriccrawlerSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class EriccrawlerDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class FakeUserAgentDownLoadMiddleWare(object):
    """
    利用fakeUserAgent,给请求随机添加header
    """

    def process_request(self, request, spider):
        # 初始化userAgent
        try:
            ua = UserAgent()
        except FakeUserAgentError:
            pass
        # 请求的request,添加随机请求头
        request.headers['User-Agent'] = ua.random
        request.headers['Accept-Encoding'] = 'gzip, deflate, sdch'
        request.headers['Accept-Language'] = 'zh-CN,zh;q=0.8'
        return None


# class UrlFilterDownLoadMiddleWare(object):
#     """
#     检测url是否已存，去重
#     """
#
#     def __init__(self, redis_url, redis_port, redis_url_prefix):
#         self.redis_db = redis.Redis(host=redis_url, port=redis_port)  # 连接redis，相当于MySQL的conn
#         self.redis_url_prefix = redis_url_prefix
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         return cls(
#             redis_url=crawler.settings.get('REDIS_URL'),
#             redis_port=crawler.settings.get('REDIS_PORT'),
#             redis_url_prefix=crawler.settings.get('REDIS_URL_PREFIX')
#         )
#
#     def process_request(self, request, spider):
#
#         url = request.url
#         # # 判定主页，不加入redis
#         if not url == 'https://www.xl720.com':
#             if self.redis_db.sadd(self.redis_url_prefix, url) == 0:
#                 return scrapy.http.Response(url=url, status=500)
#         return None
#
#     def process_exception(self, request, exception, spider):
#         return None

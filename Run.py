# -*- coding: utf-8 -*-

# @Time    : 2019/8/19 11:17 AM
# @Author  : eric_chou
# @Description  : 文件执行scrapy爬虫，代替命令行执行
import time

from scrapy import cmdline
# from apscheduler.schedulers.background import BackgroundScheduler

def run():
    while True:
        bt_crawler = "scrapy crawl BTCrawler".split()
        cmdline.execute(bt_crawler)
        # time.sleep(30)


if __name__ == '__main__':
    # scheduler = BackgroundScheduler()
    # scheduler.add_job(run, 'interval', seconds=30)
    # scheduler.start()
    run()

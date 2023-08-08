import pymongo
from EricCrawler.items import BTItem
from EricCrawler.items import BTDetailItem


class BTCrawlerPipline(object):

    def __init__(self, mongodb_url, mongodb_db_prefix):
        self.mongodb_url = mongodb_url
        self.mongodb_db_prefix = mongodb_db_prefix

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongodb_url=crawler.settings.get('MONGODB_URL'),
            mongodb_db_prefix=crawler.settings.get('MONGODB_DB_PREFIX')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongodb_url)
        self.db = self.client[self.mongodb_db_prefix]

    def process_item(self, item, spider):
        if isinstance(item, BTItem):
            collection_name = item.__class__.__name__
            self.db[collection_name].insert(dict(item))
            return item
        if isinstance(item, BTDetailItem):
            collection_name = item.__class__.__name__
            self.db[collection_name].insert(dict(item))
            return item

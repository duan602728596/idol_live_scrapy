# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter

from weibo_idol_live.items import WeiboIdolAddLiveItem, WeiboIdolUpdateLiveItem
from weibo_idol_live.spiders.live_spider import LiveSpider
from models.weibo_spider import WeiboSpiderConnect


class WeiboIdolLivePipeline:
    """ 管道 """
    def process_item(self, item: WeiboIdolAddLiveItem | WeiboIdolUpdateLiveItem, spider: LiveSpider) -> None:
        """ 将值保存到数据库 """
        if item.type == 'add':
            spider.logger.info('添加一条数据：' + item['payload']['bid'])
            WeiboSpiderConnect.add_one(item['payload'])
        elif item.type == 'update':
            spider.logger.info('更新一条数据：' + item['bid'])
            WeiboSpiderConnect.update_one(item['bid'], item['payload'])

""" 定义数据库添加和更新的item """

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class WeiboIdolAddLiveItem(Item):
    type: str = 'add'
    payload: Field = Field()


class WeiboIdolUpdateLiveItem(Item):
    type: str = 'update'
    bid: Field = Field()
    payload: Field = Field()

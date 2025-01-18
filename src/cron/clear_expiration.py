""" 定时清除过期的消息 """

from utils.times import get_one_month_ago_timestamp
from models.weibo_spider import WeiboSpiderConnect

one_month_ago_timestamp: int = get_one_month_ago_timestamp()
WeiboSpiderConnect().del_by_time(one_month_ago_timestamp)

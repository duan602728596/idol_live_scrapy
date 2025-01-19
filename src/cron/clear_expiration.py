""" 定时清除过期的消息 """

from utils.times import get_one_month_ago_timestamp
from utils.db import init_db
from utils.times import get_now_timestamp
from models.weibo_spider import WeiboSpiderConnect
from models.log import LogConnect

init_db()

LogConnect.add_one({
    'run_time': get_now_timestamp(),
    'message': '清理过期数据任务开始执行。',
})

one_month_ago_timestamp: int = get_one_month_ago_timestamp()
WeiboSpiderConnect().del_by_time(one_month_ago_timestamp)

LogConnect.add_one({
    'run_time': get_now_timestamp(),
    'message': '清理过期数据任务执行完毕。',
})

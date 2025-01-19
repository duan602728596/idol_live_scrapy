""" 一些时间的处理方法 """

from datetime import datetime, timedelta


def convert_to_timestamp(date_str: str) -> int:
    """ 将字符串转换为时间戳 """
    date_cls: datetime = datetime.strptime(date_str, '%a %b %d %H:%M:%S %z %Y')
    return int(date_cls.timestamp())

def get_one_month_ago_timestamp() -> int:
    """ 获取当前时间一个月以前的时间戳 """
    now: datetime = datetime.now()
    one_month_ago: datetime = now - timedelta(days=31)
    return int(one_month_ago.timestamp())

def get_now_timestamp() -> int:
    """ 获取当前时间戳 """
    now: datetime = datetime.now()
    return int(now.timestamp())

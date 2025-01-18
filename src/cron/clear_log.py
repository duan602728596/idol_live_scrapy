""" 定时清除log """

from os import remove
from os.path import join, basename
from datetime import date
from dateutil.relativedelta import relativedelta
from glob import glob
from utils.env import ROOT_DIR

log_dir: str = join(ROOT_DIR, 'resources/log')
files: list[str] = glob(join(log_dir, '*.log'))
today: date = date.today()


def parse_date_from_filename(filename: str) -> date:
    """ 从文件名中解析出时间 """
    name: str = basename(filename)
    parts: list[str] = name.split('.')[0].split('_')
    year: int = int(parts[0])
    month: int = int(parts[1])
    day: int = int(parts[2])
    return date(year, month, day)


def is_one_month_ago_exact(d: date) -> bool:
    """ 判断是否是一个月之前的日志 """
    one_month_ago: date = today - relativedelta(months=1)
    return d < one_month_ago


for file in files:
    d: date = parse_date_from_filename(file)
    if is_one_month_ago_exact(d):
        try:
            remove(file)
            print(f'文件 {file} 已删除。')
        except FileNotFoundError:
            print(f'文件 {file} 未找到。')

""" 获取爬虫配置 """

from typing import TypedDict
from pathlib import Path
from pandas import DataFrame, read_excel
from utils.env import ROOT_DIR


class SpiderConfigDict(TypedDict):
    """ 读取的excel类型 """
    uid: str
    lfid: str
    area: str
    remark: str


def get_live_spider_config() -> list[SpiderConfigDict]:
    """ 获取爬虫配置 """
    df: DataFrame = read_excel(Path.joinpath(ROOT_DIR, 'resources', 'live_spider_config.xlsx'))
    df.uid = df.uid.astype(str)
    df.lfid = df.lfid.astype(str)
    result: dict[int, SpiderConfigDict] = df.to_dict(orient='index')
    result_list: list[SpiderConfigDict] = []
    for k in result:
        result_list.append(result[k])
    return result_list

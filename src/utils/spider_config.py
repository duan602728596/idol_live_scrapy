""" 获取爬虫配置 """

from typing import TypedDict, Type
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


def model_to_list(model: list) -> list[SpiderConfigDict]:
    """ 转换数据类型 """
    result: list[SpiderConfigDict] = []
    for x in model:
        result.append({
            'uid': str(x.uid),
            'lfid': str(x.lfid),
            'area': str(x.area),
            'remark': str(x.remark),
        })
    return result

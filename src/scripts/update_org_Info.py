""" 将excel表中的主办信息上传到数据库 """

from utils.db import init_db
from utils.spider_config import get_live_spider_config, SpiderConfigDict
from models.org_info import OrgInfoConnect, OrgInfoModel, OrgInfoTestModel


def update_org_info():
    """ 将excel表中的主办信息上传到数据库 """
    init_db()
    live_spider_config: list[SpiderConfigDict] = get_live_spider_config()
    OrgInfoConnect.update_all(live_spider_config)
    OrgInfoConnect.rename_table()


if __name__ == '__main__':
    update_org_info()

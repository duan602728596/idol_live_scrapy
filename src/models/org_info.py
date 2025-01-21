""" 地偶主办信息 """

from typing import Callable, Type
from sqlalchemy import String, text
from sqlalchemy.orm import mapped_column, Mapped, Session
from utils.db import BaseModel, engine_48tools1
from utils.spider_config import SpiderConfigDict


orgInfo_model_create_column: dict[str, Callable] = {
    'uid': lambda: mapped_column(String(30), primary_key=True, nullable=False),
    'lfid': lambda: mapped_column(String(30), nullable=False),
    'area': lambda: mapped_column(String(255), nullable=False),
    'remark': lambda: mapped_column(String(255), nullable=False),
}


class OrgInfoModel(BaseModel):
    """ 定义数据库模型 """
    table_name: str = 'org_info'
    __tablename__: str = table_name
    uid: Mapped[str] = orgInfo_model_create_column['uid']()
    lfid: Mapped[str] = orgInfo_model_create_column['lfid']()
    area: Mapped[str] = orgInfo_model_create_column['area']()
    remark: Mapped[str] = orgInfo_model_create_column['remark']()


class OrgInfoTestModel(BaseModel):
    table_name: str = OrgInfoModel.table_name + '_test'
    __tablename__: str = table_name
    uid: Mapped[str] = orgInfo_model_create_column['uid']()
    lfid: Mapped[str] = orgInfo_model_create_column['lfid']()
    area: Mapped[str] = orgInfo_model_create_column['area']()
    remark: Mapped[str] = orgInfo_model_create_column['remark']()


class OrgInfoConnect:
    """ 地偶主办信息 """
    @staticmethod
    def update_all(update_list: list[SpiderConfigDict]) -> None:
        """ 清空数据库并上传数据 """
        with Session(engine_48tools1) as sess:
            sess.query(OrgInfoTestModel).delete()
            sess.commit()
            for x in update_list:
              sess.add(OrgInfoTestModel(uid=x['uid'], lfid=x['lfid'], area=x['area'], remark=x['remark']))
            sess.commit()

    @staticmethod
    def rename_table() -> None:
        """ 交换表名 """
        prod: str = OrgInfoModel.table_name
        test: str = OrgInfoTestModel.table_name
        temp: str = OrgInfoModel.table_name + '_temp'
        with engine_48tools1.connect() as conn:
            conn.execute(text(f'ALTER TABLE {prod} RENAME TO {temp}')) # 正式 -> 临时
            conn.execute(text(f'ALTER TABLE {test} RENAME TO {prod}')) # 测试 -> 正式
            conn.execute(text(f'ALTER TABLE {temp} RENAME TO {test}')) # 临时 -> 测试
            conn.commit()

    @staticmethod
    def get_all() -> list[Type[OrgInfoModel]]:
        """ 读取所有主办信息 """
        result: list[SpiderConfigDict] = []
        with Session(engine_48tools1) as sess:
            result: list[Type[OrgInfoModel]] = sess.query(OrgInfoModel).all()
        return result

""" 定义数据库的一些方法 """

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import DeclarativeBase
from utils.env import in_test_env, postgres_url


def format_name(n: str) -> str:
    """
    格式化名字
    用于数据库表或者索引表
    """
    return (n + '_test') if in_test_env else n


class BaseModel(DeclarativeBase):
    pass


engine_48tools1: Engine = create_engine(postgres_url, echo=False)


def init_db():
    """ 初始化数据库和表 """
    BaseModel.metadata.create_all(engine_48tools1)

""" 数据库连接 """

from typing import TypedDict
from sqlalchemy import String, Text, JSON, INTEGER, and_, or_
from sqlalchemy.orm import mapped_column, Mapped, Session
from utils.db import BaseModel, engine_48tools1, format_name


class WeiboSpiderType(TypedDict):
    """ 数据库查到的值 """
    aid: str
    bid: str
    uid: str
    screen_name: str
    avatar_hd: str
    raw_text: str
    created_at: int
    edit_at: int | None
    area: str
    pics: list[str] | None


class WeiboSpiderModel(BaseModel):
    """ 定义数据库模型 """
    __tablename__: str = format_name('weibo_spider')
    aid: Mapped[str] = mapped_column(String(30), nullable=False)
    bid: Mapped[str] = mapped_column(String(30), primary_key=True, nullable=False)
    uid: Mapped[str] = mapped_column(String(30), nullable=False)
    screen_name: Mapped[str] = mapped_column(String(30), nullable=False)
    avatar_hd: Mapped[str] = mapped_column(String(255), nullable=False)
    raw_text: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[int] = mapped_column(INTEGER, nullable=False)
    edit_at: Mapped[int | None] = mapped_column(INTEGER)
    area: Mapped[str] = mapped_column(String(255), nullable=False)
    pics: Mapped[list[str]] = mapped_column(JSON)


class WeiboSpiderConnect:
    """ 连接数据库 """
    @staticmethod
    def query_one(bid: str) -> WeiboSpiderModel:
        """ 根据bid查询单个数据 """
        result: WeiboSpiderModel | None = None
        with Session(engine_48tools1) as sess:
            result: WeiboSpiderModel | None = sess.query(
                WeiboSpiderModel.bid, WeiboSpiderModel.created_at, WeiboSpiderModel.edit_at
            ).filter(WeiboSpiderModel.bid == bid).first()
        return result

    @staticmethod
    def update_one(bid: str, update_dict: WeiboSpiderType) -> None:
        """ 更新数据库字段 """
        with Session(engine_48tools1) as sess:
            wbsp: WeiboSpiderModel | None = sess.query(WeiboSpiderModel).filter(WeiboSpiderModel.bid == bid).first()
            if wbsp:
                wbsp.screen_name = update_dict['screen_name']
                wbsp.avatar_hd = update_dict['avatar_hd']
                wbsp.raw_text = update_dict['raw_text']
                wbsp.pics = update_dict['pics']
                wbsp.created_at = update_dict['created_at']
                wbsp.edit_at = update_dict['edit_at']
                wbsp.area = update_dict['area']
                sess.commit()

    @staticmethod
    def add_one(add_dict: WeiboSpiderType) -> None:
        """ 添加数据库字段 """
        with Session(engine_48tools1) as sess:
            wbsp: WeiboSpiderModel = WeiboSpiderModel(
                aid=add_dict['aid'], bid=add_dict['bid'], uid=add_dict['uid'], screen_name=add_dict['screen_name'],
                avatar_hd=add_dict['avatar_hd'], raw_text=add_dict['raw_text'], created_at=add_dict['created_at'],
                edit_at=add_dict['edit_at'], area=add_dict['area'], pics=add_dict['pics'])
            sess.add(wbsp)
            sess.commit()

    @staticmethod
    def del_by_time(t: int):
        """ 根据时间删除过期数据 """
        with Session(engine_48tools1) as sess:
            sess.query(WeiboSpiderModel).filter(or_(
                and_(WeiboSpiderModel.edit_at.isnot(None), WeiboSpiderModel.edit_at < t),
                and_(WeiboSpiderModel.edit_at.is_(None), WeiboSpiderModel.created_at < t)
            )).delete()
            sess.commit()

""" 运行日志信息 """

from typing import TypedDict
from sqlalchemy import String, Integer, UUID
from sqlalchemy.orm import mapped_column, Mapped, Session
from utils.db import BaseModel, engine_48tools1, format_name


class LogType(TypedDict):
    """ 日志消息 """
    run_time: int
    message: str


class LogModel(BaseModel):
    """ 定义日志数据库 """
    __tablename__ = format_name('log')
    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, server_default='uuid_generate_v4()')
    run_time: Mapped[int] = mapped_column(Integer, nullable=False)
    message: Mapped[str] = mapped_column(String(255), nullable=False)


class LogConnect:
    """ 连接数据库 """
    @staticmethod
    def add_one(add_dict: LogType) -> None:
        """ 添加数据库字段 """
        with Session(engine_48tools1) as sess:
            logm: LogModel = LogModel(run_time=add_dict['run_time'], message=add_dict['message'])
            sess.add(logm)
            sess.commit()

    @staticmethod
    def del_by_time(t: int):
        """ 根据时间删除过期数据 """
        with Session(engine_48tools1) as sess:
            sess.query(LogModel).filter(LogModel.run_time < t).delete()
            sess.commit()

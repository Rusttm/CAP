# !!!used SQLAlchemy 2.0.18
from sqlalchemy import create_engine, inspect
from sqlalchemy import UniqueConstraint, PrimaryKeyConstraint
from sqlalchemy import Column, Integer, String, JSON, DateTime
from sqlalchemy import Double, BigInteger, Uuid, Boolean
from sqlalchemy.dialects.postgresql import JSONB, ARRAY, insert
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import DeclarativeBase

from PgsqlAlchemy.ConnAL.ConnALMainClass import ConnALMainClass

__url = ConnALMainClass().get_url()
engine = create_engine(__url)


class Base(DeclarativeBase):
    pass


class ModALBaseService(Base):
    __tablename__ = 'pgsql_service_model'
    position_id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False,
                         comment='Обязательное поле для всех таблиц, автоповышение')
    event_active = Column(Boolean, nullable=False, default=False,
                          comment='требуется ли реакция на сообщение? активно ли оно?')
    event_level = Column(BigInteger, nullable=False, default=10,
                         comment='уровень события: как в логере 0-notset, 10-debug, 20-info, 30-warning, 40-error, 50-critical')
    event_time = Column(DateTime, comment='время события ')
    event_name = Column(String(255), comment='короткое название события')
    event_from = Column(String(255), comment='источник события')
    event_table = Column(String(255), comment='в какой таблице произошло событие?')
    event_to = Column(String(255), nullable=False, default='Telegram', comment='для кого предназначено событие?')
    event_req = Column(String(255), comment='что требуется сделать?')
    event_descr = Column(String(4096), comment='подробное описание события')
    event_reaction = Column(String(4096), comment='ответ -что сделано на событие')
    event_reaction_time = Column(DateTime, comment='время, когда на событие среагировали')
    event_msg = Column(JSONB, comment='сообщение для SocketClient, отправленное событием в виде словаря')
    event_period_start = Column(DateTime, comment='для указания времени обновления С')
    event_period_end = Column(DateTime, comment='для указания времени обновления ПО')


def create_new_table():
    Base.metadata.create_all(engine)


def delete_table():
    Base.metadata.drop_all(engine)


if __name__ == '__main__':
    create_new_table()
# delete_table()

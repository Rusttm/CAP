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

class ModALBaseProfitByCust(Base):
	__tablename__ = 'profit_bycust_model'
	__table_args__ = (UniqueConstraint('id', name='unique_key_id'),)
	position_id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False, comment='Обязательное поле для всех таблиц, автоповышение')
	counterparty = Column(JSONB, unique=True, nullable=False, comment='Краткое представление Покупателя в отчете. Подробнее тут Обязательное при ответе')
	margin = Column(Double, comment='Рентабельность Обязательное при ответе')
	profit = Column(Double, comment='Прибыль Обязательное при ответе')
	returnAvgCheck = Column(Double, comment='Средний чек возврата Обязательное при ответе')
	returnCostSum = Column(Double, comment='Сумма себестоимостей возвратов Обязательное при ответе')
	returnCount = Column(BigInteger, comment='Количество возвратов Обязательное при ответе')
	returnSum = Column(Double, comment='Сумма возвратов Обязательное при ответе')
	salesAvgCheck = Column(Double, comment='Средний чек продаж Обязательное при ответе')
	salesCount = Column(BigInteger, comment='Количество продаж Обязательное при ответе')
	sellCostSum = Column(Double, comment='Сумма себестоимостей продаж Обязательное при ответе')
	sellSum = Column(Double, comment='Сумма продаж Обязательное при ответе')

def create_new_table():
	Base.metadata.create_all(engine)

def delete_table():
	Base.metadata.drop_all(engine)

if __name__ == '__main__':
	create_new_table()
	# delete_table()

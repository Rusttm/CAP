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

class ModALBaseStockAll(Base):
	__tablename__ = 'stockall_model'
	# __table_args__ = (UniqueConstraint('id', name='unique_key_id'),)
	position_id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False, comment='Обязательное поле для всех таблиц, автоповышение')
	article = Column(String(255), comment='Артикул')
	code = Column(String(255), unique=True, nullable=False, comment='Код Обязательное при ответе')
	externalCode = Column(String(255), comment='Внешний код сущности, по которой выводится остаток Обязательное при ответе')
	folder = Column(JSONB, comment='Группа Товара/Модификации/Cерии. Подробнее тут Обязательное при ответе')
	image = Column(JSONB, comment='Метаданные изображения Товара/Модификации/Серии')
	inTransit = Column(Double, comment='Ожидание Обязательное при ответе')
	meta = Column(JSONB, comment='Метаданные Товара/Модификации/Серии по которой выдается остаток Обязательное при ответе')
	name = Column(String(255), comment='Наименование Обязательное при ответе')
	price = Column(Double, comment='Себестоимость')
	quantity = Column(Double, comment='Доступно Обязательное при ответе')
	reserve = Column(Double, comment='Резерв Обязательное при ответе')
	salePrice = Column(Double, comment='Цена продажи')
	stock = Column(Double, comment='Остаток Обязательное при ответе')
	stockDays = Column(BigInteger, comment='Количество дней на складе Обязательное при ответе')
	uom = Column(JSONB, comment='Единица измерения. Подробнее тут Обязательное при ответе')

def create_new_table():
	Base.metadata.create_all(engine)

def delete_table():
	Base.metadata.drop_all(engine)

if __name__ == '__main__':
	create_new_table()
	# delete_table()

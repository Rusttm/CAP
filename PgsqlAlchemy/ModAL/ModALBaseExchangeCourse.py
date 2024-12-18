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

class ModALBaseExchangeCourse(Base):
	__tablename__ = 'exchange_courses_model'
	# __table_args__ = (UniqueConstraint('id', name='unique_key_id'),)
	position_id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False, comment='Обязательное поле для всех таблиц, автоповышение')
	on_date = Column(DateTime, unique=True, nullable=False, comment='Дата на которую берется курс')
	usd_840 = Column(Double, unique=False, nullable=False, comment='Доллар США')
	eur_978 = Column(Double, unique=False, nullable=False, comment='Евро')
	cny_156 = Column(Double, unique=False, nullable=False, comment='Китайских юаней')
	kzt_398 = Column(Double, unique=False, nullable=False, comment='Казахстанских тенге')
	jpy_392 = Column(Double, unique=False, nullable=False, comment='Японских иен')
	try_949 = Column(Double, unique=False, nullable=False, comment='Турецких лир')
	qar_634 = Column(Double, unique=False, nullable=False, comment='Катарский риал')
	aed_784 = Column(Double, unique=False, nullable=False, comment='Дирхам ОАЭ')
	byn_933 = Column(Double, unique=False, nullable=False, comment='Белорусский рубль')

def create_new_table():
	Base.metadata.create_all(engine)

def delete_table():
	Base.metadata.drop_all(engine)

if __name__ == '__main__':
	# create_new_table()
	# delete_table()
	my_dict = {'aed_784': 0.0, 'byn_933': 31.1093, 'cny_156': 9.54298, 'eur_978': 75.6817, 'jpy_392': 0.583901, 'kzt_398': 0.17796299999999998, 'on_date': '2018.11.08', 'qar_634': 0.0, 'try_949': 12.3069, 'usd_840': 66.0918}
	new_obj = ModALBaseExchangeCourse(**my_dict)
	print(new_obj)

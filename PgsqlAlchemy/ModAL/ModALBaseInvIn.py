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

class ModALBaseInvIn(Base):
	__tablename__ = 'invin_model'
	position_id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False, comment='Обязательное поле для всех таблиц, автоповышение')
	accountId = Column(Uuid, comment='ID учетной записи Обязательное при ответе Только для чтения')
	agent = Column(JSONB, nullable=False, comment='Метаданные контрагента Обязательное при ответе Expand')
	applicable = Column(Boolean, comment='Отметка о проведении Обязательное при ответе')
	attributes = Column(MutableList.as_mutable(ARRAY(JSONB)), comment='Коллекция метаданных доп. полей. Поля объекта')
	code = Column(String(255), comment='Код выданного Счета-фактуры полученного')
	contract = Column(JSONB, comment='Метаданные договора Expand')
	created = Column(DateTime, comment='Дата создания Обязательное при ответе Только для чтения')
	deleted = Column(DateTime, comment='Момент последнего удаления Счета-фактуры полученного Только для чтения')
	description = Column(String(4096), comment='Комментарий выданного Счета-фактуры полученного')
	externalCode = Column(String(255), comment='Внешний код выданного Счета-фактуры полученного Обязательное при ответе')
	files = Column(JSONB, comment='Метаданные массива Файлов (Максимальное количество файлов - 100) Обязательное при ответе Expand')
	group = Column(JSONB, comment='Отдел сотрудника Обязательное при ответе Expand')
	id = Column(Uuid, unique=True, nullable=False, comment='ID Счета-фактуры полученного Обязательное при ответе Только для чтения')
	meta = Column(JSONB, comment='Метаданные Счета-фактуры полученного Обязательное при ответе')
	moment = Column(DateTime, comment='Дата документа Обязательное при ответе')
	name = Column(String(255), comment='Наименование выданного Счета-фактуры полученного Обязательное при ответе')
	organization = Column(JSONB, comment='Метаданные юрлица Обязательное при ответе Expand Необходимо при создании')
	owner = Column(JSONB, comment='Владелец (Сотрудник) Обязательное при ответе Expand')
	printed = Column(Boolean, comment='Напечатан ли документ Обязательное при ответе Только для чтения')
	published = Column(Boolean, comment='Опубликован ли документ Обязательное при ответе Только для чтения')
	rate = Column(JSONB, comment='Валюта. Подробнее тут Обязательное при ответе')
	shared = Column(Boolean, comment='Общий доступ Обязательное при ответе')
	state = Column(JSONB, comment='Метаданные статуса Счета-фактуры полученного Expand')
	sum = Column(BigInteger, comment='Сумма Счета-фактуры полученного в установленной валюте Обязательное при ответе Только для чтения')
	syncId = Column(Uuid, comment='ID синхронизации. После заполнения недоступен для изменения')
	supplies = Column(MutableList.as_mutable(ARRAY(JSONB)), comment='Массив ссылок на связанные приемки в формате Метаданных')
	payments = Column(MutableList.as_mutable(ARRAY(JSONB)), comment='Массив ссылок на связанные исходящие платежи в формате Метаданных')
	incomingNumber = Column(String(255), comment='Входящий номер')
	incomingDate = Column(DateTime, comment='Входящая дата')
	updated = Column(DateTime, comment='Момент последнего обновления Счета-фактуры полученного Обязательное при ответе Только для чтения')

def create_new_table():
	Base.metadata.create_all(engine)

def delete_table():
	Base.metadata.drop_all(engine)

if __name__ == '__main__':
	create_new_table()
	# delete_table()

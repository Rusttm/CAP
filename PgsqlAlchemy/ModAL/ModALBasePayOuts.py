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

class ModALBasePayOuts(Base):
	__tablename__ = 'payouts_model'
	# __table_args__ = (UniqueConstraint('id', name='unique_key_id'),)
	position_id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False, comment='Обязательное поле для всех таблиц, автоповышение')
	accountId = Column(Uuid, comment='ID учетной записи Обязательное при ответе Только для чтения')
	agent = Column(JSONB, comment='Метаданные контрагента Обязательное при ответе Expand Необходимо при создании')
	agentAccount = Column(JSONB, comment='Метаданные счета контрагента Expand')
	applicable = Column(Boolean, comment='Отметка о проведении Обязательное при ответе')
	attributes = Column(JSONB, comment='Коллекция метаданных доп. полей. Поля объекта')
	code = Column(String(255), comment='Код Исходящего платежа')
	contract = Column(JSONB, comment='Метаданные договора Expand')
	created = Column(DateTime, comment='Дата создания Обязательное при ответе Только для чтения')
	deleted = Column(DateTime, comment='Момент последнего удаления Исходящего платежа Только для чтения')
	description = Column(String(4096), comment='Комментарий Исходящего платежа')
	expenseItem = Column(JSONB, comment='Метаданные Статьи расходов Обязательное при ответе Expand Необходимо при создании')
	externalCode = Column(String(255), comment='Внешний код Исходящего платежа Обязательное при ответе')
	files = Column(JSONB, comment='Метаданные массива Файлов (Максимальное количество файлов - 100) Обязательное при ответе Expand')
	group = Column(JSONB, comment='Отдел сотрудника Обязательное при ответе Expand')
	id = Column(Uuid, unique=True, nullable=False, comment='ID Исходящегоо платежа Обязательное при ответе Только для чтения')
	meta = Column(JSONB, comment='Метаданные Исходящего платежа Обязательное при ответе')
	moment = Column(DateTime, comment='Дата документа Обязательное при ответе')
	name = Column(String(255), comment='Наименование Исходящего платежа Обязательное при ответе')
	organization = Column(JSONB, comment='Метаданные юрлица Обязательное при ответе Expand Необходимо при создании')
	organizationAccount = Column(JSONB, comment='Метаданные счета юрлица Expand')
	owner = Column(JSONB, comment='Владелец (Сотрудник) Обязательное при ответе Expand')
	paymentPurpose = Column(String(255), comment='Назначение платежа Обязательное при ответе')
	printed = Column(Boolean, comment='Напечатан ли документ Обязательное при ответе Только для чтения')
	project = Column(JSONB, comment='Метаданные проекта Expand')
	published = Column(Boolean, comment='Опубликован ли документ Обязательное при ответе Только для чтения')
	rate = Column(JSONB, comment='Валюта. Подробнее тут Обязательное при ответе')
	salesChannel = Column(JSONB, comment='Метаданные канала продаж Expand')
	shared = Column(Boolean, comment='Общий доступ Обязательное при ответе')
	state = Column(JSONB, comment='Метаданные статуса Исходящего платежа Expand')
	sum = Column(BigInteger, comment='Сумма Входящего платежа в установленной валюте Обязательное при ответе Только для чтения')
	syncId = Column(Uuid, comment='ID синхронизации. После заполнения недоступен для изменения')
	updated = Column(DateTime, comment='Момент последнего обновления Исходящего платежа Обязательное при ответе Только для чтения')
	operations = Column(MutableList.as_mutable(ARRAY(JSONB)), comment='Массив ссылок на связанные операции в формате Метаданных')
	factureOut = Column(String(255), comment='Ссылка на Счет-фактуру выданный, с которым связан этот платеж в формате Метаданных')
	vatSum = Column(Double, comment='Сумма НДС Обязательное при ответе')

def create_new_table():
	Base.metadata.create_all(engine)

def delete_table():
	Base.metadata.drop_all(engine)

if __name__ == '__main__':
	create_new_table()
	# delete_table()

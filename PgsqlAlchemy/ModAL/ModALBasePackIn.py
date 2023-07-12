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

class ModALBasePackIn(Base):
	__tablename__ = 'packin_model'
	# __table_args__ = (UniqueConstraint('id', name='unique_key_id'),)
	position_id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False, comment='Обязательное поле для всех таблиц, автоповышение')
	accountId = Column(Uuid, comment='ID учетной записи Обязательное при ответе Только для чтения Change-handler')
	agent = Column(JSONB, comment='Метаданные контрагента Обязательное при ответе Expand Необходимо при создании Change-handler Update-provider')
	agentAccount = Column(JSONB, comment='Метаданные счета контрагента Expand Change-handler Update-provider')
	applicable = Column(Boolean, comment='Отметка о проведении Обязательное при ответе Change-handler Update-provider')
	attributes = Column(JSONB, comment='Коллекция метаданных доп. полей. Поля объекта Change-handler Update-provider')
	code = Column(String(255), comment='Код Приемки')
	contract = Column(JSONB, comment='Метаданные договора Expand Change-handler Update-provider')
	consignee = Column(JSONB, comment='Метаданные грузополучателя (контрагент или юрлицо) ')
	created = Column(DateTime, comment='Дата создания Обязательное при ответе Только для чтения Change-handler')
	deleted = Column(DateTime, comment='Момент последнего удаления Приемки Только для чтения')
	description = Column(String(4096), comment='Комментарий Приемки Change-handler Update-provider')
	externalCode = Column(String(255), comment='Внешний код Приемки Обязательное при ответе Change-handler')
	files = Column(JSONB, comment='Метаданные массива Файлов (Максимальное количество файлов - 100) Обязательное при ответе Expand')
	group = Column(JSONB, comment='Отдел сотрудника Обязательное при ответе Expand')
	id = Column(Uuid, unique=True, nullable=False, comment='ID Приемки Обязательное при ответе Только для чтения Change-handler')
	incomingDate = Column(DateTime, comment='Входящая дата Change-handler Update-provider')
	incomingNumber = Column(String(255), comment='Входящий номер Change-handler Update-provider')
	meta = Column(JSONB, comment='Метаданные Приемки Обязательное при ответе Change-handler')
	moment = Column(DateTime, comment='Дата документа Обязательное при ответе Change-handler Update-provider')
	name = Column(String(255), comment='Наименование Приемки Обязательное при ответе Change-handler Update-provider')
	organization = Column(JSONB, comment='Метаданные юрлица Обязательное при ответе Expand Необходимо при создании Change-handler Update-provider')
	organizationAccount = Column(JSONB, comment='Метаданные счета юрлица Expand Change-handler Update-provider')
	overhead = Column(JSONB, comment='Накладные расходы. Подробнее тут. Если Позиции Приемки не заданы, то накладные расходы нельзя задать Update-provider')
	owner = Column(JSONB, comment='Владелец (Сотрудник) Обязательное при ответе Expand')
	payedSum = Column(Double, comment='Сумма входящих платежей по Приемке Обязательное при ответе Только для чтения')
	positions = Column(JSONB, comment='Метаданные позиций Приемки Обязательное при ответе Expand Change-handler Update-provider')
	printed = Column(Boolean, comment='Напечатан ли документ Обязательное при ответе Только для чтения')
	project = Column(JSONB, comment='Метаданные проекта Expand Change-handler Update-provider')
	published = Column(Boolean, comment='Опубликован ли документ Обязательное при ответе Только для чтения')
	rate = Column(JSONB, comment='Валюта. Подробнее тут Обязательное при ответе Change-handler Update-provider')
	shared = Column(Boolean, comment='Общий доступ Обязательное при ответе')
	state = Column(JSONB, comment='Метаданные статуса Приемки Expand Change-handler Update-provider')
	store = Column(JSONB, comment='Метаданные склада Обязательное при ответе Expand Необходимо при создании Change-handler Update-provider')
	sum = Column(BigInteger, comment='Сумма Приемки в копейках Обязательное при ответе Только для чтения Change-handler')
	syncId = Column(Uuid, comment='ID синхронизации. После заполнения недоступен для изменения')
	updated = Column(DateTime, comment='Момент последнего обновления Приемки Обязательное при ответе Только для чтения Change-handler')
	vatEnabled = Column(Boolean, comment='Учитывается ли НДС Обязательное при ответе Change-handler Update-provider')
	vatIncluded = Column(Boolean, comment='Включен ли НДС в цену Change-handler Update-provider')
	purchaseOrder = Column(JSONB, comment='Ссылка на связанный заказ поставщику в формате Метаданных')
	factureIn = Column(JSONB, comment='Ссылка на Счет-фактуру полученный, с которым связана эта Приемка в формате Метаданных')
	invoicesIn = Column(MutableList.as_mutable(ARRAY(JSONB)), comment='Массив ссылок на связанные счета поставщиков в формате Метаданных')
	payments = Column(MutableList.as_mutable(ARRAY(JSONB)), comment='Массив ссылок на связанные платежи в формате Метаданных')
	returns = Column(MutableList.as_mutable(ARRAY(JSONB)), comment='Массив ссылок на связанные возвраты в формате Метаданных')
	vatSum = Column(Double, comment='Сумма НДС Обязательное при ответе Только для чтения Change-handler')

def create_new_table():
	Base.metadata.create_all(engine)

def delete_table():
	Base.metadata.drop_all(engine)

if __name__ == '__main__':
	create_new_table()
	# delete_table()

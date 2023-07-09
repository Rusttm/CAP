# !!!used SQLAlchemy 2.0.18
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, JSON, DateTime, Double, BigInteger
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import mapped_column

from PgsqlAlchemy.ConnAL.ConnALMainClass import ConnALMainClass
__url = ConnALMainClass().get_url()
engine = create_engine(__url)

class Base(DeclarativeBase):
	pass

class customers_bal_model(Base):
	__tablename__ = 'customers_bal_model'
	position_id = Column(BigInteger, primary_key=True, autoincrement=True, unique=True, nullable=False, comment='Обязательное поле для всех таблиц, автоповышение')
	averageReceipt = Column(Double, comment='Средний чек Обязательное при ответе')
	balance = Column(Double, comment='Баланс Обязательное при ответе')
	bonusBalance = Column(Double, comment='Баллы Обязательное при ответе')
	counterparty = Column(JSONB, unique=True, nullable=False, comment='Контрагент. Подробнее тут Обязательное при ответе')
	demandsCount = Column(BigInteger, comment='Количество продаж Обязательное при ответе')
	demandsSum = Column(Double, comment='Сумма продаж Обязательное при ответе')
	discountsSum = Column(Double, comment='Сумма скидок Обязательное при ответе')
	firstDemandDate = Column(DateTime, comment='Дата первой продажи Обязательное при ответе')
	lastDemandDate = Column(DateTime, comment='Дата последней продажи Обязательное при ответе')
	lastEventDate = Column(DateTime, comment='Дата последнего события Обязательное при ответе')
	lastEventText = Column(String(255), comment='Текст последнего события Обязательное при ответе')
	meta = Column(JSONB, comment='Метаданные Отчета по данному контрагенту Обязательное при ответе')
	profit = Column(Double, comment='Прибыль Обязательное при ответе')
	returnsCount = Column(BigInteger, comment='Количество возвратов Обязательное при ответе')
	returnsSum = Column(Double, comment='Сумма возвратов Обязательное при ответе')
	updated = Column(DateTime, comment='Момент последнего изменения контрагента Обязательное при ответе')

Base.metadata.create_all(engine)

# Base.metadata.drop_all(engine)
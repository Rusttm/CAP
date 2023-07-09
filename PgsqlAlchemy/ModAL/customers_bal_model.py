# !!!used SQLAlchemy 2.0.18
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, JSON, DateTime, Double, BigInteger
from sqlalchemy.orm import DeclarativeBase

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import mapped_column

from PgsqlAlchemy.ConnAL.ConnALMainClass import ConnALMainClass
__url = ConnALMainClass().get_url()
engine = create_engine(__url)
class Base(DeclarativeBase):
	pass

class customers_bal_fields(Base):
	__tablename__ = 'customers_bal_fields'
	position_id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
	averageReceipt = Column(Double)
	balance = Column(Double)
	bonusBalance = Column(Double)
	counterparty = Column(JSON, unique=True, nullable=False)
	demandsCount = Column(BigInteger)
	demandsSum = Column(Double)
	discountsSum = Column(Double)
	firstDemandDate = Column(DateTime)
	lastDemandDate = Column(DateTime)
	lastEventDate = Column(DateTime)
	lastEventText = Column(String(255))
	meta = Column(JSON)
	profit = Column(Double)
	returnsCount = Column(BigInteger)
	returnsSum = Column(Double)
	updated = Column(DateTime)

Base.metadata.create_all(engine)

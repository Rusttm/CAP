# !!!used SQLAlchemy 2.0.18
from sqlalchemy import create_engine, inspect
from sqlalchemy import Column, Integer, Double, DateTime, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase

from PgsqlAlchemy.ConnAL.ConnALMainClass import ConnALMainClass
__url = ConnALMainClass().get_url()
engine = create_engine(__url)

class Base(DeclarativeBase):
	pass

class ModALBaseDailyProfitY2021(Base):
	__tablename__ = 'daily_profit_model_2021'
	position_id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False, comment='Обязательное поле для всех таблиц, автоповышение')
	counterparty = Column(JSONB, unique=True, nullable=False, comment='Контрагент. Подробнее тут Обязательное при ответе')
	name = Column(String)
	update = Column(DateTime, nullable=False, comment='Дата расчета (конец дня)')
	day_2021_01_01 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_01_02 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_01_03 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_01_04 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_01_05 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_01_06 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_01_07 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_01_08 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_01_09 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_01_10 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_01_11 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_01_12 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_01_13 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_01_14 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_01_15 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_01_16 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_01_17 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_01_18 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_01_19 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_01_20 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_01_21 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_01_22 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_01_23 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_01_24 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_01_25 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_01_26 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_01_27 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_01_28 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_01_29 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_01_30 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_01_31 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_02_01 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_02_02 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_02_03 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_02_04 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_02_05 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_02_06 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_02_07 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_02_08 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_02_09 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_02_10 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_02_11 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_02_12 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_02_13 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_02_14 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_02_15 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_02_16 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_02_17 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_02_18 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_02_19 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_02_20 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_02_21 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_02_22 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_02_23 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_02_24 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_02_25 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_02_26 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_02_27 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_02_28 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_03_01 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_03_02 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_03_03 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_03_04 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_03_05 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_03_06 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_03_07 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_03_08 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_03_09 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_03_10 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_03_11 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_03_12 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_03_13 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_03_14 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_03_15 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_03_16 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_03_17 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_03_18 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_03_19 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_03_20 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_03_21 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_03_22 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_03_23 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_03_24 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_03_25 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_03_26 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_03_27 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_03_28 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_03_29 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_03_30 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_03_31 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_04_01 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_04_02 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_04_03 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_04_04 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_04_05 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_04_06 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_04_07 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_04_08 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_04_09 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_04_10 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_04_11 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_04_12 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_04_13 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_04_14 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_04_15 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_04_16 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_04_17 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_04_18 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_04_19 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_04_20 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_04_21 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_04_22 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_04_23 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_04_24 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_04_25 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_04_26 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_04_27 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_04_28 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_04_29 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_04_30 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_05_01 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_05_02 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_05_03 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_05_04 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_05_05 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_05_06 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_05_07 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_05_08 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_05_09 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_05_10 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_05_11 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_05_12 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_05_13 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_05_14 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_05_15 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_05_16 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_05_17 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_05_18 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_05_19 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_05_20 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_05_21 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_05_22 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_05_23 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_05_24 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_05_25 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_05_26 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_05_27 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_05_28 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_05_29 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_05_30 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_05_31 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_06_01 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_06_02 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_06_03 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_06_04 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_06_05 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_06_06 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_06_07 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_06_08 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_06_09 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_06_10 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_06_11 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_06_12 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_06_13 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_06_14 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_06_15 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_06_16 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_06_17 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_06_18 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_06_19 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_06_20 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_06_21 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_06_22 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_06_23 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_06_24 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_06_25 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_06_26 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_06_27 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_06_28 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_06_29 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_06_30 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_07_01 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_07_02 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_07_03 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_07_04 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_07_05 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_07_06 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_07_07 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_07_08 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_07_09 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_07_10 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_07_11 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_07_12 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_07_13 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_07_14 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_07_15 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_07_16 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_07_17 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_07_18 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_07_19 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_07_20 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_07_21 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_07_22 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_07_23 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_07_24 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_07_25 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_07_26 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_07_27 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_07_28 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_07_29 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_07_30 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_07_31 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_08_01 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_08_02 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_08_03 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_08_04 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_08_05 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_08_06 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_08_07 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_08_08 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_08_09 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_08_10 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_08_11 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_08_12 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_08_13 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_08_14 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_08_15 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_08_16 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_08_17 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_08_18 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_08_19 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_08_20 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_08_21 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_08_22 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_08_23 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_08_24 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_08_25 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_08_26 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_08_27 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_08_28 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_08_29 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_08_30 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_08_31 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_09_01 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_09_02 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_09_03 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_09_04 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_09_05 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_09_06 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_09_07 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_09_08 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_09_09 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_09_10 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_09_11 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_09_12 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_09_13 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_09_14 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_09_15 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_09_16 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_09_17 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_09_18 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_09_19 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_09_20 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_09_21 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_09_22 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_09_23 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_09_24 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_09_25 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_09_26 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_09_27 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_09_28 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_09_29 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_09_30 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_10_01 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_10_02 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_10_03 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_10_04 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_10_05 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_10_06 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_10_07 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_10_08 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_10_09 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_10_10 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_10_11 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_10_12 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_10_13 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_10_14 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_10_15 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_10_16 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_10_17 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_10_18 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_10_19 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_10_20 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_10_21 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_10_22 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_10_23 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_10_24 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_10_25 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_10_26 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_10_27 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_10_28 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_10_29 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_10_30 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_10_31 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_11_01 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_11_02 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_11_03 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_11_04 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_11_05 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_11_06 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_11_07 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_11_08 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_11_09 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_11_10 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_11_11 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_11_12 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_11_13 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_11_14 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_11_15 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_11_16 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_11_17 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_11_18 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_11_19 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_11_20 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_11_21 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_11_22 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_11_23 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_11_24 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_11_25 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_11_26 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_11_27 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_11_28 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_11_29 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_11_30 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_12_01 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_12_02 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_12_03 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_12_04 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_12_05 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_12_06 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_12_07 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_12_08 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_12_09 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_12_10 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_12_11 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_12_12 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_12_13 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_12_14 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_12_15 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_12_16 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_12_17 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_12_18 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_12_19 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_12_20 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_12_21 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_12_22 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_12_23 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_12_24 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_12_25 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_12_26 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_12_27 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_12_28 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_12_29 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_12_30 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2021_12_31 = Column(Double, nullable=False, default=0, comment='прибыль на дату')

def create_new_table():
	Base.metadata.create_all(engine)

def delete_table():
	Base.metadata.drop_all(engine)

if __name__ == '__main__':
	create_new_table()
	# delete_table()

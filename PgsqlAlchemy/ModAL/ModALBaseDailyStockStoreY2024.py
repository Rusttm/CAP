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

class ModALBaseDailyStockStoreY2024(Base):
	__tablename__ = 'daily_stock_store_model_2024'
	position_id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False, comment='Обязательное поле для всех таблиц, автоповышение')
	store = Column(JSONB, unique=True, nullable=False, comment='Контрагент. Подробнее тут Обязательное при ответе')
	name = Column(String)
	update = Column(DateTime, nullable=False, comment='Дата расчета (конец дня)')
	day_2024_01_01 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_01_02 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_01_03 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_01_04 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_01_05 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_01_06 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_01_07 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_01_08 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_01_09 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_01_10 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_01_11 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_01_12 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_01_13 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_01_14 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_01_15 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_01_16 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_01_17 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_01_18 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_01_19 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_01_20 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_01_21 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_01_22 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_01_23 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_01_24 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_01_25 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_01_26 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_01_27 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_01_28 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_01_29 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_01_30 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_01_31 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_02_01 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_02_02 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_02_03 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_02_04 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_02_05 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_02_06 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_02_07 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_02_08 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_02_09 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_02_10 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_02_11 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_02_12 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_02_13 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_02_14 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_02_15 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_02_16 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_02_17 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_02_18 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_02_19 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_02_20 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_02_21 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_02_22 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_02_23 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_02_24 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_02_25 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_02_26 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_02_27 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_02_28 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_02_29 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_03_01 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_03_02 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_03_03 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_03_04 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_03_05 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_03_06 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_03_07 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_03_08 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_03_09 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_03_10 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_03_11 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_03_12 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_03_13 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_03_14 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_03_15 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_03_16 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_03_17 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_03_18 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_03_19 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_03_20 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_03_21 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_03_22 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_03_23 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_03_24 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_03_25 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_03_26 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_03_27 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_03_28 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_03_29 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_03_30 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_03_31 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_04_01 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_04_02 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_04_03 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_04_04 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_04_05 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_04_06 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_04_07 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_04_08 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_04_09 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_04_10 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_04_11 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_04_12 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_04_13 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_04_14 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_04_15 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_04_16 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_04_17 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_04_18 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_04_19 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_04_20 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_04_21 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_04_22 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_04_23 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_04_24 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_04_25 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_04_26 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_04_27 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_04_28 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_04_29 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_04_30 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_05_01 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_05_02 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_05_03 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_05_04 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_05_05 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_05_06 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_05_07 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_05_08 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_05_09 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_05_10 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_05_11 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_05_12 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_05_13 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_05_14 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_05_15 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_05_16 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_05_17 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_05_18 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_05_19 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_05_20 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_05_21 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_05_22 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_05_23 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_05_24 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_05_25 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_05_26 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_05_27 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_05_28 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_05_29 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_05_30 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_05_31 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_06_01 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_06_02 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_06_03 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_06_04 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_06_05 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_06_06 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_06_07 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_06_08 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_06_09 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_06_10 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_06_11 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_06_12 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_06_13 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_06_14 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_06_15 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_06_16 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_06_17 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_06_18 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_06_19 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_06_20 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_06_21 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_06_22 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_06_23 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_06_24 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_06_25 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_06_26 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_06_27 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_06_28 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_06_29 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_06_30 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_07_01 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_07_02 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_07_03 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_07_04 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_07_05 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_07_06 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_07_07 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_07_08 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_07_09 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_07_10 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_07_11 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_07_12 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_07_13 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_07_14 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_07_15 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_07_16 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_07_17 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_07_18 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_07_19 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_07_20 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_07_21 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_07_22 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_07_23 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_07_24 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_07_25 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_07_26 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_07_27 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_07_28 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_07_29 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_07_30 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_07_31 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_08_01 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_08_02 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_08_03 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_08_04 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_08_05 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_08_06 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_08_07 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_08_08 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_08_09 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_08_10 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_08_11 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_08_12 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_08_13 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_08_14 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_08_15 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_08_16 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_08_17 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_08_18 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_08_19 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_08_20 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_08_21 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_08_22 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_08_23 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_08_24 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_08_25 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_08_26 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_08_27 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_08_28 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_08_29 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_08_30 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_08_31 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_09_01 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_09_02 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_09_03 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_09_04 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_09_05 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_09_06 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_09_07 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_09_08 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_09_09 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_09_10 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_09_11 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_09_12 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_09_13 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_09_14 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_09_15 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_09_16 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_09_17 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_09_18 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_09_19 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_09_20 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_09_21 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_09_22 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_09_23 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_09_24 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_09_25 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_09_26 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_09_27 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_09_28 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_09_29 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_09_30 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_10_01 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_10_02 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_10_03 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_10_04 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_10_05 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_10_06 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_10_07 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_10_08 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_10_09 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_10_10 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_10_11 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_10_12 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_10_13 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_10_14 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_10_15 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_10_16 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_10_17 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_10_18 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_10_19 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_10_20 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_10_21 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_10_22 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_10_23 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_10_24 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_10_25 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_10_26 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_10_27 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_10_28 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_10_29 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_10_30 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_10_31 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_11_01 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_11_02 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_11_03 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_11_04 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_11_05 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_11_06 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_11_07 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_11_08 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_11_09 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_11_10 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_11_11 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_11_12 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_11_13 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_11_14 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_11_15 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_11_16 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_11_17 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_11_18 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_11_19 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_11_20 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_11_21 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_11_22 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_11_23 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_11_24 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_11_25 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_11_26 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_11_27 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_11_28 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_11_29 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_11_30 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_12_01 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_12_02 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_12_03 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_12_04 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_12_05 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_12_06 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_12_07 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_12_08 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_12_09 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_12_10 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_12_11 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_12_12 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_12_13 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_12_14 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_12_15 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_12_16 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_12_17 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_12_18 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_12_19 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_12_20 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_12_21 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_12_22 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_12_23 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_12_24 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_12_25 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_12_26 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_12_27 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_12_28 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_12_29 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_12_30 = Column(Double, nullable=False, default=0, comment='прибыль на дату')
	day_2024_12_31 = Column(Double, nullable=False, default=0, comment='прибыль на дату')

def create_new_table():
	Base.metadata.create_all(engine)

def delete_table():
	Base.metadata.drop_all(engine)

if __name__ == '__main__':
	create_new_table()
	# delete_table()

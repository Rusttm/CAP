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

class ModALBaseCust(Base):
	__tablename__ = 'customers_model'
	__table_args__ = (UniqueConstraint('id', name='unique_key_id'),)
	position_id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False, comment='Обязательное поле для всех таблиц, автоповышение')
	accountId = Column(Uuid, comment='ID учетной записи Обязательное при ответе Только для чтения')
	accounts = Column(JSONB, comment='Массив счетов Контрагентов. Подробнее тут Обязательное при ответе Expand')
	actualAddress = Column(String(255), comment='Фактический адрес Контрагента')
	actualAddressFull = Column(JSONB, comment='Фактический адрес Контрагента с детализацией по отдельным полям. Подробнее тут')
	archived = Column(Boolean, comment='Добавлен ли Контрагент в архив Обязательное при ответе')
	attributes = Column(MutableList.as_mutable(ARRAY(JSONB)), comment='Массив метаданных доп. полей')
	bonusPoints = Column(BigInteger, comment='Бонусные баллы по активной бонусной программе Только для чтения')
	bonusProgram = Column(JSONB, comment='Метаданные активной Бонусной программы Expand')
	code = Column(String(255), comment='Код Контрагента')
	companyType = Column(String(255), comment='Тип Контрагента. В зависимости от значения данного поля набор выводимых реквизитов контрагента может меняться. Подробнее тут Обязательное при ответе')
	contactpersons = Column(JSONB, comment='Массив контактных лиц фирмы Контрагента. Подробнее тут Expand')
	created = Column(DateTime, comment='Момент создания Обязательное при ответе')
	description = Column(String(4096), comment='Комментарий к Контрагенту')
	discountCardNumber = Column(String(255), comment='Номер дисконтной карты Контрагента')
	discounts = Column(MutableList.as_mutable(ARRAY(JSONB)), comment='Массив скидок Контрагента. Массив может содержать персональные и накопительные скидки. Персональная скидка выводится, если хотя бы раз изменялся процент скидки для контрагента, значение будет указано в поле personalDiscount')
	email = Column(String(255), comment='Адрес электронной почты')
	externalCode = Column(String(255), comment='Внешний код Контрагента Обязательное при ответе')
	fax = Column(String(255), comment='Номер факса')
	files = Column(JSONB, comment='Метаданные массива Файлов (Максимальное количество файлов - 100) Обязательное при ответе Expand')
	group = Column(JSONB, comment='Отдел сотрудника Обязательное при ответе Expand')
	id = Column(Uuid, unique=True, nullable=False, comment='ID Контрагента Обязательное при ответе Только для чтения')
	meta = Column(JSONB, unique=True, comment='Метаданные Контрагента Обязательное при ответе')
	name = Column(String(255), comment='Наименование Контрагента Обязательное при ответе Необходимо при создании')
	notes = Column(JSONB, comment='Массив событий Контрагента. Подробнее тут Expand')
	owner = Column(JSONB, comment='Владелец (Сотрудник) Expand')
	phone = Column(String(255), comment='Номер городского телефона')
	priceType = Column(JSONB, comment='Тип цены Контрагента. Подробнее тут')
	salesAmount = Column(BigInteger, comment='Сумма продаж Обязательное при ответе Только для чтения')
	shared = Column(Boolean, comment='Общий доступ Обязательное при ответе')
	state = Column(JSONB, comment='Метаданные Статуса Контрагента Expand')
	syncId = Column(Uuid, comment='ID синхронизации После заполнения недоступно для изменения')
	tags = Column(MutableList.as_mutable(ARRAY(String)), comment='Группы контрагента')
	updated = Column(DateTime, comment='Момент последнего обновления Контрагента Обязательное при ответе Только для чтения')
	certificateDate = Column(DateTime, comment='Дата свидетельства')
	certificateNumber = Column(String(255), comment='Номер свидетельства')
	inn = Column(String(255), comment='ИНН')
	kpp = Column(String(255), comment='КПП')
	legalAddress = Column(String(255), comment='Юридический адрес Контрагента')
	legalAddressFull = Column(JSONB, comment='Юридический адрес Контрагента с детализацией по отдельным полям')
	legalFirstName = Column(String(255), comment='Имя для Контрагента типа [Индивидуальный предприниматель, Физическое лицо]. Игнорируется для Контрагентов типа [Юридическое лицо]')
	legalLastName = Column(String(255), comment='Фамилия для Контрагента типа [Индивидуальный предприниматель, Физическое лицо]. Игнорируется для Контрагентов типа [Юридическое лицо]')
	legalMiddleName = Column(String(255), comment='Отчество для Контрагента типа [Индивидуальный предприниматель, Физическое лицо]. Игнорируется для Контрагентов типа [Юридическое лицо]')
	legalTitle = Column(String(4096), comment='Полное наименование для Контрагента типа [Юридическое лицо]. Игнорируется для Контрагентов типа [Индивидуальный предприниматель, Физическое лицо], если передано одно из значений для ФИО и формируется автоматически на основе получаемых ФИО Контрагента')
	ogrn = Column(String(255), comment='ОГРН')
	ogrnip = Column(String(255), comment='ОГРНИП')
	okpo = Column(String(255), comment='ОКПО')

def create_new_table():
	Base.metadata.create_all(engine)

def delete_table():
	Base.metadata.drop_all(engine)

if __name__ == '__main__':
	create_new_table()
	# delete_table()

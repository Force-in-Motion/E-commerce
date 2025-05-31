from sqlalchemy import create_engine, text, Connection, MetaData, Table, Column, Integer, Text, ForeignKey
from sqlalchemy.orm import Session, foreign

# Создаем ключевой объект подключения, в котором указывается url базы данных,
# Который состоит из диалекта, в данном случае это синтаксис для работы с sqlite3,
# затем драйвер, в данном случае это синхронный драйвер pysqlite для работы с sqlite3,
# затем для использования относительного пути к файлу используется ///,
# ну и сам файл базы данных storage.db
# echo=True нужен для отладки и говорит выводить все логи операций с базой в консоль
engine = create_engine('sqlite+pysqlite:///storage.db', echo=True)

# Объект MetaData содержит мета данные базы, то есть данные о том, как данные должны храниться в базе ( информацию о таблицах, столбцах, кортежах и т. д. )
metadata = MetaData()


# Определяем таблицу пользователя и указываем ее столбцы и их параметры
user_table = Table('users', metadata, Column('id', Integer, primary_key=True, autoincrement=True),
                                                   Column('name', Text, nullable=False),
                                                   Column('age', Integer, nullable=False))


# Определяем таблицу пользователя и указываем ее столбцы и их параметры
address = Table('address', metadata, Column('address', Integer, primary_key=True, autoincrement=True),
                                                  Column('email', Text, nullable=False),
                                                  Column('user_id', Integer, ForeignKey('users.id')))

# Создаем таблицы
metadata.create_all(engine)

# Удаляем таблицы
metadata.drop_all(engine)











# engine.connect() - контекстный менеджер, при помощи которого открывается соединение с базой данных
# with engine.connect() as connect:
#     result = connect.execute(text())
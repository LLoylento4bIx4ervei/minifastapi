from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from config import settings


#Строка подключения БД
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}'

#Создание Движка
engine = create_engine(SQLALCHEMY_DATABASE_URL)

#Сессия БД
Sessionlocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

#Создание базового класса для моделей
Base = declarative_base()

#Функция обработки для передачи объекта сессии БД
def get_db():
    db=Sessionlocal()
    try:
        yield db
    finally:
        db.close()




#Коннект БД
while True:
    try:
        conn = psycopg2.connect(database = 'miniproject',password='8bQc0e7axKJ',user='postgres',host='localhost',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('DATABASE CONNECT')
        break
    except Exception:
        print('CONNECTION LOST')
        time.sleep(5) 
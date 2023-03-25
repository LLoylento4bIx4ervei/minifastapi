from database import Base
from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

#Создаем модели, объекты которой буду храниться в БД


class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True,nullable=False)
    name = Column(String,nullable = False)
    last_name = Column(String,nullable=False)
    email = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))


class Post(Base):
    __tablename__ = "post"

    id = Column(Integer,primary_key=True,nullable=False)
    post = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    owner_id = Column(Integer,ForeignKey('users.id',ondelete='CASCADE'),nullable=False)
    owner = relationship('User')


class Vote(Base):
    __tablename__ = "vote"

    user_id = Column(Integer,ForeignKey('users.id',ondelete='CASCADE'),primary_key=True)
    post_id = Column(Integer,ForeignKey('post.id',ondelete='CASCADE'),primary_key=True)
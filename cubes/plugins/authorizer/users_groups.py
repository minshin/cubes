from sqlalchemy import Column, String, BIGINT, INT, create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from .user_groups import Model as User_Groups

Base = declarative_base()

class Model(Base):
    __tablename__ = 'users_groups'
    user_id=Column(BIGINT)
    user_group_id=Column(INT)
    role_id=Column(INT)
    group = relationship('User_Groups',backref='g')
    from .user        import Model as Users
    user = relationship('Users',backref='u')

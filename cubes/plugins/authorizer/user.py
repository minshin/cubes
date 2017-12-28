from sqlalchemy import Column, String, BIGINT, INT, create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from .user_groups import Model as User_Groups

Base = declarative_base()

class Model(Base):
    __tablename__ = 'users'
    id = Column(BIGINT, primary_key=True)
    group_unit = Column(String)
    token_create_time = Column(BIGINT)
    from .users_groups import Model as Users_Groups
    groups = relationship('User_Groups',secondary=Users_Groups.__table__,backref='g')
    relations = relationship('Users_Groups',backref='r')

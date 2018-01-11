from sqlalchemy import Column, String, BIGINT, INT, create_engine, PrimaryKeyConstraint, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Doctor(Base):
    __tablename__='bohe_article_doctor'
    id = Column(INT, primary_key=True)
    user_id =Column(BIGINT)

class Users_Groups(Base):
    __tablename__ = 'users_groups'
    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'user_group_id'),
    )
    user_id=Column(BIGINT,ForeignKey('users.id'))
    user_group_id=Column(INT,ForeignKey('user_groups.id'))
    role_id=Column(INT)
    group = relationship('User_Groups',backref='g',primaryjoin="User_Groups.id==Users_Groups.user_group_id")
    user = relationship('User',backref='u',primaryjoin="User.id==Users_Groups.user_id")

class User(Base):
    __tablename__ = 'users'
    id = Column(BIGINT, primary_key=True)
    group_unit = Column(String)
    token_create_time = Column(BIGINT)
    groups = relationship('User_Groups',secondary=Users_Groups.__table__,backref='u')
    relations = relationship('Users_Groups',backref='r')

class User_Groups(Base):
    __tablename__ = 'user_groups'
    id=Column(INT, primary_key=True)
    code=Column(String)

class Clinic(Base):
    __tablename__ = 'bohe_clinic'
    id = Column(INT, primary_key=True)
    group_unit = Column(String)
    user_id = Column(BIGINT, primary_key=True)

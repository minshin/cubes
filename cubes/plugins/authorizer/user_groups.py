from sqlalchemy import Column, String, BIGINT, INT, create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Model(Base):
    __tablename__ = 'user_groups'
    id=Column(INT, primary_key=True)
    code=Column(String)

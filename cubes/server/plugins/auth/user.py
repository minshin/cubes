from sqlalchemy import Column, String, BIGINT, INT, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Model(Base):
    __tablename__ = "users"
    id=Column(BIGINT, primary_key=True)
    group_unit=Column(String)
    token_create_time=Column(BIGINT)

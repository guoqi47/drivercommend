# -*- coding: UTF-8 -*-
from sqlalchemy import Column, String, create_engine,Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class DriverNo(Base):
    __tablename__ = 'g_team_driver_detail'

    id = Column(Integer, primary_key=True)
    driver_id = Column(String(50))
    lic_no    = Column(String(18))


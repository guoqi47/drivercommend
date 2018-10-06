# -*- coding: UTF-8 -*-
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class ActivityMap(Base):
    __tablename__ = 'g_team_combine_activity_city_map'

    id = Column(Integer, primary_key=True)
    activity_id = Column(Integer)
    city_id = Column(Integer)
    create_time = Column(Integer)






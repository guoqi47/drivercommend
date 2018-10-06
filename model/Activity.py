# -*- coding: UTF-8 -*-
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class Activity(Base):
    __tablename__ = 'g_team_combine_activity'

    id = Column(Integer, primary_key=True)
    activity_id = Column(Integer)
    end_time = Column(Integer)
    recommend_way = Column(Integer)
    start_time = Column(Integer)
    status = Column(Integer)
    team_max_num = Column(Integer)
    team_min_num = Column(Integer)
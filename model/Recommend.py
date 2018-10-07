# -*- coding: UTF-8 -*-
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class Recommend(Base):
    __tablename__ = 'g_team_combine_recommend'

    id = Column(Integer, primary_key=True)
    captain_id = Column(Integer)
    member_id = Column(Integer)
    assign_time = Column(Integer)
    insert_time = Column(Integer)
    update_time = Column(Integer)
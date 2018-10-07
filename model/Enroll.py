# -*- coding: UTF-8 -*-
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class Enroll(Base):
    __tablename__ = 'g_team_combine_enroll_driver'

    id = Column(Integer, primary_key=True)
    activity_id = Column(Integer)
    driver_id = Column(Integer)
    team_id = Column(Integer)
    captain_id = Column(Integer)
    assign_status = Column(Integer)
    apply_status = Column(Integer)
    role_type = Column(Integer)
    captain_assign_status = Column(Integer)
    captain_dispatch_status = Column(Integer)
    recommend_num = Column(Integer)
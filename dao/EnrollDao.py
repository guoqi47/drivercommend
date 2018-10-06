#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('..')

from model.Enroll import *
from sqlalchemy import create_engine
from sqlalchemy import Table, MetaData, Column, Integer, String
from sqlalchemy.orm import mapper, sessionmaker


class EnrollDao(object):
    __tablename__ = 'g_team_combine_enroll_driver'
    def __init__(self,Enroll):
        self.Enroll = Enroll
        self.enroll = Table('g_team_combine_enroll_driver', MetaData(),
                    Column('id', Integer, primary_key=True),
                    Column('activity_id', Integer),
                    Column('driver_id', Integer),
                    Column('team_id', Integer),
                    Column('captain_id', Integer),
                    Column('assign_status', Integer),
                    Column('apply_status', Integer),
                    Column('role_type', Integer),
                    Column('captain_assign_status', Integer),
                    Column('captain_dispatch_status', Integer),
                    Column('recommend_num', Integer)
                )
        mapper(self.Enroll, self.enroll)
        engine = create_engine("mysql+pymysql://root:root@localhost/test",encoding='utf-8', echo=True)
        Session_class = sessionmaker(bind=engine)  # 实例和engine绑定
        self.Session = Session_class()  # 生成session实例，相当于游标


    def get1(self):
        # add1 = Enroll(id=5,activity_id=5,driver_id=5,team_id=5,captain_id=5,
        #               assign_status=5,apply_status=5,
        #               role_type=5,captain_assign_status=5,captain_dispatch_status=5,
        #               recommend_num=5)
        # self.Session.add(add1)

        my_user = self.Session.query(self.enroll).first()  # 查询
        print(my_user)
        print(my_user.activity_id)
        print(my_user.driver_id)



#EnrollDao(Enroll).get1()


       


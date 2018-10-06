# -*- coding: utf-8 -*-
from model.ActivityMap import ActivityMap
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class ActivityMapDao(object):
    _status_for_handle = 1  # 审核通过

    def __init__(self, ActivityMap):
        self.ActivityMap = ActivityMap
        engine = create_engine("mysql+pymysql://root:root@localhost:3306/test", echo=True)
        Session_class = sessionmaker(bind=engine)  # 实例和engine绑定
        self.Session = Session_class()  # 生成session实例，相当于游标

    def getList(self,city_ids):
        return self.Session.query(ActivityMap).filter(self.ActivityMap.city_id.in_(city_ids))












# city_ids 返回activity_ids


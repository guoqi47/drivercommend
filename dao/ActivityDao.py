# -*- coding: utf-8 -*-

from model.Activity import Activity
from dao.ActivityMapDao import ActivityMapDao
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class ActivityDao(object):
    _status_for_handle = 1  # 审核通过

    def __init__(self, Activity):
        self.Activity = Activity
        engine = create_engine("mysql+pymysql://root:root@localhost:3306/test", echo=True)
        Session_class = sessionmaker(bind=engine)  # 实例和engine绑定
        self.Session = Session_class()  # 生成session实例，相当于游标

    def valid(self):
        """
        返回审核通过、组队类型为3的活动范围
        :param query:
        :return:
        """
        return self.Session.query(Activity).filter(self.Activity.status==self._status_for_handle)

    def getList(self, now,activity_ids,isin):
        """
        获取有效活动，now-400可保证在活动结束后再执行一次分配动作
        :param now: 时间戳
        :param activity_ids:排除的id列表
        :param isin:1限定在城市中 0排出城市
        :return: 有效活动
        """

        base = self.valid().filter(Activity.start_time < now, Activity.end_time > now - 400)

        if isin == 1:
            # print(' where_in activity_ids', isin, activity_ids)
            return base.filter(Activity.activity_id.in_(activity_ids)).all()
        else:
            # print(' where_not_in activity_ids', isin, activity_ids)
            return base.filter(~Activity.activity_id.in_(activity_ids)).all()

    def getListForConfStrategy(self,now,city_ids):
        """
        B方案：按照配置方案分配 获取当前时间下的有效活动,根据配置情况，找出其中定制化的活动
        :param now: 时间戳
        :city_ids : 限定的城市
        :isin : 1限定在城市中 0排出城市
        :return: 有效活动collections
        """
        ListAll=[]
        for city_id in city_ids:
            activityCitys=ActivityMapDao.getList([city_id])
            print ('city_id...',city_id)
            activityids=[]
            for i in activityCitys:
                activityids.append(i.activity_id)
            acts= self.getList(now,activityids,1)
            for a in acts:
               a.city_id = city_id
               ListAll.append(a)
        return ListAll

    @classmethod
    def getListForYearAndArea(self,now,city_ids):
        """
        A方案：按照年龄家乡分配 获取当前时间下的有效活动 降级方案 排除定制方案，其余按照原来的年龄地域区分
        :param now: 时间戳
        :city_ids : 限定的城市
        :isin : 1限定在城市中 0排出城市
        :return: 有效活动list
        """
        activityCitys=ActivityMapDao.getList(city_ids)
        activityids=[]
        for i in activityCitys:
            activityids.append(i.activity_id)
            print('activity_id.....',i.activity_id)
        print('activityids',activityids)
        ListAll=self.getList(now,activityids,0) #获取有效活动
        return ListAll


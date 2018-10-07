# -*- coding: utf-8 -*-

from model.Enroll import Enroll
from sqlalchemy import create_engine, func, text
from sqlalchemy.orm import sessionmaker


class EnrollDao(object):
    __timestamps__ = False
    chunkSize = 100

    def __init__(cls, Enroll):
        cls.Enroll = Enroll
        engine = create_engine("mysql+pymysql://root:root@localhost:3306/test", echo=True)
        Session_class = sessionmaker(bind=engine)  # 实例和engine绑定
        cls.Session = Session_class()  # 生成session实例，相当于游标

    def getTeamForAssign(cls, activityId):
        """
        获取所有待分配的队伍：team_id：队伍id，captian_id：原始id，leader_id：队长driver_id,recommend_qty：总推荐队员数，
        member_qty：正式队员数，assign_qty：分配队员数
        :param activityId: 活动id
        :return: 队伍列表
        """
        teams = []
        # for items in cls.select('team_id', 'id as captain_id', 'driver_id as leader_id',
        #                         'recommend_num as recommend_qty') \
        #         .where('activity_id', '=', activityId).captainForAssign().valid().chunk(cls.chunkSize):
        #     teamIds = [item.team_id for item in items]
        #     rows = cls.formal().valid().select(db.raw('team_id,count(*) as qty')).where_in('team_id', teamIds) \
        #         .where('activity_id', '=', activityId).group_by('team_id').get()
        #     formalQty = dict([(row.team_id, row.qty) for row in rows])
        #
        #     for item in items:
        #         item.member_qty = formalQty.get(item.team_id, 0)
        #         teams.append(item)
        # count 使用
        # return cls.Session.query(func.count(Enroll.activity_id), Enroll.activity_id).filter(Enroll.activity_id==activityId).group_by(Enroll.activity_id).all()
        # count之前
        # return cls.captainForAssign().filter(Enroll.activity_id == activityId, Enroll.apply_status == 1)
        return cls.Session.query(Enroll.team_id,Enroll.captain_id,Enroll.driver_id,Enroll.recommend_num,
                                 func.count(Enroll.activity_id).label('member_qty')).\
            group_by(Enroll.team_id,Enroll.captain_id,Enroll.driver_id,Enroll.recommend_num).\
            filter(cls.Enroll.captain_dispatch_status == 0). \
            filter(cls.Enroll.captain_assign_status.in_([0, 1, 2])). \
            filter(cls.Enroll.role_type == 1).filter(Enroll.activity_id == activityId, Enroll.apply_status == 1).all()

        # return teams

    def getDriverForAssign(cls, activityId):
        """
        获取活动中的待分配队员
        :param activityId: 活动id
        :return: 待分配队员colllections
        """
        return cls.MemberForAssign().\
            filter(Enroll.activity_id==activityId).filter(Enroll.apply_status==1).all()


    def getCaptainForAssign(cls, activityId):
        """
        获取待分配的队长
        :param activityId: 活动id
        :return: 队长collections
        """
        return cls.captainForAssign().filter(Enroll.activity_id==activityId).\
            filter(Enroll.apply_status==1).all()


    def getAcceptedOrQuitMemberIds(cls, activityId):  # 暂时没有用chunk;参数做了修改，原为activity
        """
        获取活动中已被接收或退出队伍的队员id
        :param activity: 活动
        :return: 队员id列表
        """
        return cls.Session.query(Enroll.captain_id).filter(Enroll.activity_id==activityId) .\
                filter(Enroll.assign_status.in_([3, 4, 5]))


    def getCompletedOrDissolvedCaptainIds(cls, activityId): # 参数做了修改，原为activity
        """
        获取活动中组队完成或解散的队长id
        :param activity: 活动对象
        :return: 队长id列表
        """
        return cls.Session.query(Enroll.captain_id).filter(Enroll.activity_id==activityId).filter(Enroll.captain_assign_status.in_([3, 4])).\
                all()


    def getCaptainIds(cls, activityId): # 参数做了修改，原为activity
        """
        获取活动中所有队长id
        :param activity: 活动对象
        :return: 队长id列表
        """
        # return cls.where('activity_id', '=', activity.activity_id).lists('id')
        return cls.Session.query(Enroll.captain_id).filter(cls.Enroll.activity_id==activityId).all()

    def captainForAssign(self):
        return self.Session.query(Enroll).filter(self.Enroll.captain_dispatch_status == 0). \
            filter(self.Enroll.captain_assign_status.in_([0, 1, 2])). \
            filter(self.Enroll.role_type == 1)

    def MemberForAssign(self):
        return self.Session.query(Enroll).filter(self.Enroll.assign_status.in_([0, 1, 2])). \
            filter(self.Enroll.role_type == 0)


    def assign(self):
        return self.Session.query(Enroll).filter(self.Enroll.assign_status==2)

    def formal(self):
        # 3:已接受组队
        # 4:已完成组队
        return self.Session.query(Enroll).filter(self.Enroll.assign_status.in_([3, 5]))

    # def valid(self):
    #     # return query.where('apply_status', '=', 1)
    #     return self.Session.query().filter(self.Enroll.apply_status==1)

    def setCaptainAssignStatus(cls, captainId, activityId):
        """
        队伍总推荐数加1：recommend_num ++
        :param captainId: 队长id
        :param activityId: 活动id
        :return: None
        """
        # cls.where('id', '=', captainId).where('activity_id', '=', activityId).increment('recommend_num')
        cls.Session.query(Enroll).filter(cls.Enroll.captain_id==captainId,cls.Enroll.activity_id==activityId).\
            update({Enroll.recommend_num: Enroll.recommend_num+1})
        cls.Session.commit()


    def setAssignDriver(cls, memberId, activityId):
        """
        更新队员分配状态：assign_status : 2 一定要加.where('assign_status','<',2)条件
        :param memberId: 队员id
        :param activityId: 活动id
        :return: None
        """
        # filter(text("assign_status<2"))
        cls.Session.query(Enroll).filter(text("assign_status<2")).filter(Enroll.apply_status==1).\
            filter(Enroll.driver_id==memberId,Enroll.activity_id==activityId).\
            update({Enroll.assign_status: 2}, synchronize_session='fetch')
        cls.Session.commit()


    def get_driverID_ID_map(cls): # 和原函数不一样
        """
        获取活动中的待分配队员
        :param activityId: 活动id
        :return: 待分配队员colllections
        """
        res={}
        for instance in cls.Session.query(Enroll.id,Enroll.driver_id).filter(Enroll.assign_status.in_([0, 1, 2]),
                                   Enroll.role_type==0,Enroll.apply_status==1).all():
            res[instance.id] = instance.driver_id
        return res




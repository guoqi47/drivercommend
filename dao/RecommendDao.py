# -*- coding: utf-8 -*-
from model.Recommend import Recommend
from sqlalchemy import create_engine, text, func
from sqlalchemy.orm import sessionmaker
import time

class RecommendDao(object):

    def __init__(cls, Recommend):
        cls.Recommend = Recommend
        engine = create_engine("mysql+pymysql://root:root@localhost:3306/test", echo=True)
        Session_class = sessionmaker(bind=engine)  # 实例和engine绑定
        cls.Session = Session_class()  # 生成session实例，相当于游标

    def clearByMemberIds(cls, member_ids):
        """
        按队员id从推荐表中删除推荐记录
        :param member_ids: 队员member_id列表
        :return: None
        """
        try:
            # in操作比较特别，需要加synchronize_session=False
            # https://segmentfault.com/q/1010000000130368
            cls.Session.query(Recommend).filter(Recommend.member_id.in_(member_ids)).delete(synchronize_session=False)
            cls.Session.commit()
        except:
            pass

    def clearByCaptainIds(cls, captain_ids):
        """
        按队长id从推荐表中删除推荐记录
        :param captain_ids: 队长id列表
        :return: None
        """
        chunk = 500
        try:
            for i in range(len(captain_ids) / chunk + 1):
                cls.Session.query(Recommend).filter(Recommend.captain_id.in_(captain_ids[chunk * i:chunk * (i + 1)])).\
                    delete(synchronize_session=False)
                cls.Session.commit()
        except:
            pass

    def clearExpiredByCaptainIds(cls, captain_ids):
        """
        删除十二小时之前的推荐记录，按队长id
        :param captain_ids: 队长id范围
        :return: None
        """
        expired_time = time.time() - 3600 * 12
        chunk = 500
        # try:
        for i in range(len(captain_ids) / chunk + 1):
            cls.Session.query(Recommend).filter(text("assign_time < %d"%expired_time)).\
                filter(Recommend.captain_id.in_(captain_ids[chunk * i:chunk * (i + 1)])).\
                delete(synchronize_session=False)
            cls.Session.commit()
        # except:
        #     pass

    def getAssignQtyForTeams(cls, teams):
        """
        统计队伍当前推荐人数
        :param teams: 队伍列表
        :return: 附带推荐队员数的队伍列表
        """
        res = []
        tempMap={}
        captainIds = [team.captain_id for team in teams]
        for instance in cls.Session.query(Recommend.captain_id,func.count('*').label('qty')).\
            filter(Recommend.captain_id.in_(captainIds)).group_by('captain_id').all():
            tempMap[instance.captain_id] = instance.qty

        #加入推荐队员数信息
        for team in teams:
            team.assign_qty = tempMap.get(team.captain_id, 0)
            res.append(team)

        return res

    def getCaptainsForMembers(cls, members):
        """
        统计每个待分配队员当前所在的队伍，及队伍个数，返回待分配队员列表
        :param members: 队员列表
        :return: 附带队长信息的队员列表
        """
        res = []
        for member in members:
            member.captains = cls.Session.query(Recommend.captain_id).filter(Recommend.member_id==member).all()
            member.captainsNum = len(member.captains)
            res.append(member)
        return res

    def addRecommand(cls, memberId, captainId):
        """
        登记表中添加推荐记录
        :param memberId:
        :param captainId:
        :return:
        """
        add_ = Recommend(
            captain_id=captainId,
            member_id=memberId,
            assign_time=int(time.time()),
            insert_time=int(time.time()),
            update_time=int(time.time())
        )
        cls.Session.add(add_)
        cls.Session.commit()
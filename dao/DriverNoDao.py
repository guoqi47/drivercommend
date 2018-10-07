# -*- coding: utf-8 -*-

from model.DriverNo import DriverNo
from sqlalchemy import create_engine
from sqlalchemy.orm import mapper, sessionmaker


class DriverNoDao(object):

    def __init__(cls,DriverNo):
        cls.DriverNo = DriverNo
        engine = create_engine("mysql+pymysql://root:root@localhost:3306/test", echo=True)
        Session_class = sessionmaker(bind=engine)  # 实例和engine绑定
        cls.Session = Session_class()  # 生成session实例，相当于游标

    def getIdcard(cls,driverIds):
        """
        获取身份证号：保证只有合法的身份证号（18位）才会返回'
        :param driverIds:
        :return: {driver_id: lic_no}
        """

        cardId = {}
        for instance in cls.Session.query(DriverNo.driver_id,DriverNo.lic_no).\
            filter(DriverNo.driver_id.in_(driverIds)):
            if len(instance.lic_no)==18:
                cardId[instance.driver_id] = instance.lic_no
        return cardId


#!/usr/bin/env python
# -*- coding: utf-8 -*-
#https://blog.csdn.net/fgf00/article/details/52949973
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
# 创建实例，并连接test库
engine = create_engine("mysql+pymysql://root:Ybaobao1@localhost/test",encoding='utf-8', echo=True)
# echo=True 显示信息
Base = declarative_base()  # 生成orm基类

class User(Base):
    __tablename__ = 'user'  # 表名
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    password = Column(String(64))

Base.metadata.create_all(engine) #创建表结构 （这里是父类调子类）

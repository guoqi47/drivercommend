# -*- coding: UTF-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String ,Enum 
from sqlalchemy.orm import sessionmaker


# 创建实例，并连接test库
engine = create_engine("mysql+pymysql://root:root@localhost/test",encoding='utf-8', echo=True)

Base = declarative_base()  # 生成orm基类

class Student(Base):
    __tablename__ = 'student'  # 表名
    id = Column(Integer, primary_key=True, autoincrement=True)
    stu_id = Column(Integer)
    age = Column(Integer)  # 整型
    gender = Column(Enum('M','F'),nullable=False)

Base.metadata.create_all(engine) #创建表结构 （这里是父类调子类）

# 创建与数据库的会话session class ,注意,这里返回给session的是个class,不是实例
# Session_class = sessionmaker(bind=engine)
# Session = Session_class()  # 生成session实例
# stu_obj = Student(stu_id=27, age=22, gender="M")
# # 添加到session:
# Session.add(stu_obj)
# # 提交即保存到数据库:
# Session.commit() #现此才统一提交，创建数据
# 关闭session:
# Session.close()

#如何查数据
# 有了ORM，查询出来的可以不再是tuple，而是User对象。
Session_class = sessionmaker(bind=engine)
Session = Session_class()  # 生成session实例
# 创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行:
user = Session.query(Student).filter(Student.id=='1').one()

print user.age

#ret = session.query(Users, Favor).filter(Users.id == Favor.nid).all()
## 以下两种 必须表之间有外键关联才能查
#ret = session.query(Person).join(Favor).all()  
#ret = session.query(Person).join(Favor, isouter=True).all()
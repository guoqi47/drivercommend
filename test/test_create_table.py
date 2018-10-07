# -*- coding: UTF-8 -*-
from sqlalchemy import create_engine,Table,Column,Integer,String,MetaData,ForeignKey

engine=create_engine("mysql+pymysql://root:root@localhost:3306/test",echo=True)
metadata=MetaData(engine)

# creat table
user=Table('g_team_combine_recommend',metadata,
    Column('id',Integer,primary_key=True),
    Column('captain_id',Integer),
    Column('member_id', Integer),
    Column('assign_time',Integer),
    Column('insert_time',Integer),
    Column('update_time', Integer)
    )
# address_table = Table('address', metadata,
#     Column('id', Integer, primary_key=True),
#     Column('user_id', None, ForeignKey('user.id')),
#     Column('email', String(128), nullable=False)
#     )
metadata.create_all()

users_table = Table('g_team_combine_recommend', metadata, autoload=True)

# i = users_table.insert()
# # Enroll
# i.execute(activity_id = 2,driver_id =2,team_id=5,captain_id=5,assign_status=5,apply_status=5,
#             role_type=5,captain_assign_status=5,captain_dispatch_status=5,recommend_num=5)
# i.execute(activity_id = 1,driver_id =3,team_id=6,captain_id=6,assign_status=6,apply_status=6,
#             role_type=6,captain_assign_status=6,captain_dispatch_status=6,recommend_num=6)
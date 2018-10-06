# -*- coding: UTF-8 -*-
from sqlalchemy import create_engine,Table,Column,Integer,String,MetaData,ForeignKey

engine=create_engine("mysql+pymysql://root:root@localhost:3306/test",echo=True)
metadata=MetaData(engine)

# creat table
user=Table('g_team_combine_activity_city_map',metadata,
    Column('id',Integer,primary_key=True),
    Column('activity_id',Integer),
    Column('city_id', Integer),
    Column('create_time',Integer)

    )
# address_table = Table('address', metadata,
#     Column('id', Integer, primary_key=True),
#     Column('user_id', None, ForeignKey('user.id')),
#     Column('email', String(128), nullable=False)
#     )
metadata.create_all()

users_table = Table('g_team_combine_activity_city_map', metadata, autoload=True)

i = users_table.insert()
i.execute(activity_id = 2,city_id =2,
          create_time=2)
i.execute(activity_id = 3,city_id =3,
          create_time=3)
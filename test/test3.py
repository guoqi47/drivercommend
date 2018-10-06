from sqlalchemy import create_engine
from sqlalchemy import Table, MetaData, Column, Integer, String
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy import func
# 创建实例，并连接test库
engine = create_engine("mysql+pymysql://root:Ybaobao1@localhost/test",encoding='utf-8', echo=True)

metadata = MetaData()

user = Table('user', metadata,
            Column('id', Integer, primary_key=True),
            Column('name', String(50)),
            Column('password', String(12))
        )

class User(object):
    def __init__(self, name, id, password):
        self.id = id
        self.name = name
        self.password = password

    def __repr__(self): 
        return "<User(name='%s',  password='%s')>" % (self.name, self.password)


# the table metadata is created separately with the Table construct, then associated with the User class via the mapper() function
mapper(User, user)



# 创建与数据库的会话session class ,注意,这里返回给session的是个class,不是实例
Session_class = sessionmaker(bind=engine)  # 实例和engine绑定
Session = Session_class()  # 生成session实例，相当于游标

#user_obj = User(id=29,name="fgfs",password="123456")  # 生成你要创建的数据对象
#print(user_obj.name,user_obj.id)  # 此时还没创建对象呢，不信你打印一下id发现还是None
#Session.add(user_obj)  # 把要创建的数据对象添加到这个session里， 一会统一创建
#print(user_obj.name,user_obj.id) #此时也依然还没创建
#Session.commit() #现此才统一提交，创建数据


my_user = Session.query(User).filter_by(name="fgf").first()  # 查询
print(my_user)

print(Session.query(User.name,User.id).all() )# 获取所有数据





#多条件查询
objs = Session.query(User).filter(User.id>0).filter(User.id<7).all()

#修改
my_user = Session.query(User).filter_by(name="fgfs").first()
my_user.name = "fenggf"  # 查询出来之后直接赋值修改
my_user.passwork = "123qwe"
Session.commit()


#filter_by与filter
my_user1 = Session.query(User).filter(User.id>2).all()
my_user2 = Session.query(User).filter_by(name="fgfs").all()  # filter_by相等用‘=’
my_user3 = Session.query(User).filter(User.id==27).all()  # filter相等用‘==’

print(my_user1,'\n',my_user2,'\n',my_user3)



#回滚
my_user = Session.query(User).filter_by(id=28).first()
my_user.name = "Jack"

fake_user = User(id=30,name='Rain', password='12345')
Session.add(fake_user)

print(Session.query(User).filter(User.name.in_(['Jack','rain'])).all() )  #这时看session里有你刚添加和修改的数据

Session.rollback() #此时你rollback一下

print(Session.query(User).filter(User.name.in_(['Jack','rain'])).all() ) #再查就发现刚才添加的数据没有了。

# Session
# Session.commit()

#统计 count
print(Session.query(User).filter(User.name.like("f%")).count() ) # mysql不区分大小写
#分组 group_by
print(Session.query(User.name,func.count(User.name)).group_by(User.name).all() )


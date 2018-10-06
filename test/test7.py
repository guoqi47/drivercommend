'''
现在来设计一个能描述“图书”与“作者”的关系的表结构，需求是
一本书可以有好几个作者一起出版
一个作者可以写好几本书 
此时你会发现，用之前学的外键好像没办法实现上面的需求了 
那怎么办呢？ 此时，我们可以再搞出一张中间表，就可以了 
这样就相当于通过book_m2m_author表完成了book表和author表之前的多对多关联 
双向一对多，就是多对多。 
用orm如何表示呢？

https://blog.csdn.net/fgf00/article/details/52949973

'''
# 创建表结构
from sqlalchemy import Table, Column, Integer,String,DATE, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
# 第三张表 自己创建。不需要手动管理，orm自动维护
book_m2m_author = Table('book_m2m_author', Base.metadata,
                        Column('book_id',Integer,ForeignKey('books.id')),
                        Column('author_id',Integer,ForeignKey('authors.id')),
                        )
class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer,primary_key=True)
    name = Column(String(64))
    pub_date = Column(DATE)
    # book表不知道第三张表，所以关联一下第三张表
    authors = relationship('Author',secondary=book_m2m_author,backref='books')
    def __repr__(self):
        return self.name

class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    def __repr__(self):
        return self.name

engine = create_engine("mysql+pymysql://root:Ybaobao1@localhost/test",encoding='utf-8', echo=True)

Base.metadata.create_all(engine)  # 创建表结构

Session_class = sessionmaker(bind=engine)  # 创建与数据库的会话session class ,注意,这里返回给session的是个class,不是实例
session = Session_class()  # 生成session实例 #cursor



# 创建书
b1 = Book(name="learn",pub_date="2014-05-2")
b2= Book(name="learn Zhangbility with Alex",pub_date="2015-05-2")
b3 = Book(name="Learn hook up girls with Alex",pub_date="2016-05-2")
# 创建作者
a1 = Author(name="Alex")
a2 = Author(name="Jack")
a3 = Author(name="Rain")
# 关联关系
b1.authors = [a1,a3]
b3.authors = [a1,a2,a3]

session.add_all([b1,b2,b3,a1,a2,a3])
session.commit()

# 重要是查询
author_obj = session.query(Author).filter(Author.name=="alex").first()
print(author_obj.books[0:])
book_obj = session.query(Book).filter(Book.id==2).first()
print(book_obj.authors)



#通过书删除作者
author_obj =session.query(Author).filter_by(name="Jack").first()
book_obj = session.query(Book).filter_by(name="learn").first()
book_obj.authors.remove(author_obj) #从一本书里删除一个作者
session.commit()


#直接删除作者　
#删除作者时，会把这个作者跟所有书的关联关系数据也自动删除
author_obj =session.query(Author).filter_by(name="Alex").first()
# print(author_obj.name , author_obj.books)
session.delete(author_obj)
session.commit()

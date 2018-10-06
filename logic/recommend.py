#!/usr/bin/env python
# -*- coding: utf-8 -*-


#抽象类加抽象方法就等于面向对象编程中的接口
from abc import ABCMeta,abstractmethod
 
class recommend(object):
    __metaclass__ = ABCMeta #指定这是一个抽象类
    @abstractmethod  #抽象方法
    def Lee(self):
        pass

    def Marlon(self):
        pass

class recommendImplDB(recommend):
    def __init__(self):    
        print ('DB interface')

    def Lee(self):
        print ('DB Lee')  

    def Marlon(self):
        print ("DB Marlon")

class recommendImplSrc(recommend): 
    def __init__(self):    
        print ('Src interface') 

    def Lee(self):
        print ('Src Lee')  

    def Marlon(self):
        print ("Src Marlon")

a=recommendImplSrc()
a.Lee()
a.Marlon()
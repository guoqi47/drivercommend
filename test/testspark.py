# -*- coding:utf-8 -*-
from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
import math
appName ="jhl_spark_1" #你的应用程序名称
master= "local"#设置单机
conf = SparkConf().setAppName(appName).setMaster(master)#配置SparkContext
sc = SparkContext(conf=conf)
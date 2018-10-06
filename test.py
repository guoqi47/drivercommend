from model.Enroll import *
from dao.EnrollDao import EnrollDao
from dao.EnrollDao import Enroll
# EnrollDao(Enroll).get1()

# from dao.DriverNoDao import DriverNo
# from dao.DriverNoDao import *
# driverIds=[2,3]
# print DriverNoDao(DriverNo).getIdcard(driverIds).__len__()

from dao.ActivityMapDao import ActivityMapDao
from model.ActivityMap import ActivityMap
print ActivityMapDao(ActivityMap).getList([2,3])

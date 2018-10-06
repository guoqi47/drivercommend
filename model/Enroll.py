#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Enroll(object):
    def __init__(self, id, activity_id, driver_id, team_id, captain_id, assign_status, 
        apply_status, role_type, captain_assign_status, captain_dispatch_status, recommend_num):
        id                     =self.id                     
        activity_id            =self.activity_id            
        driver_id              =self.driver_id              
        team_id                =self.team_id                
        captain_id             =self.captain_id             
        assign_status          =self.assign_status          
        apply_status           =self.apply_status           
        role_type              =self.role_type                       
        captain_assign_status  =self.captain_assign_status  
        captain_dispatch_status=self.captain_dispatch_status
        recommend_num          =self.recommend_num
    def __repr__(self): 
        return "<User(name='%s',  password='%s')>" % (self.team_id, self.activity_id)
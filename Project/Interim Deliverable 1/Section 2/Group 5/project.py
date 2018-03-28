#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 15:57:49 2018

@author: xiaonaiyuan
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

cancelled=pd.read_excel("Cancelled_Courses_1516_1617.xlsx")
cancelled.head()

for row in cancelled.iterrows():   
    term=row['Term']
    
    
    
    
schedule=pd.read_excel('Marshall_Course_Enrollment_1516_1617.xlsx')
cancelled=pd.read_excel('Cancelled_Courses_1516_1617.xlsx')
master=schedule.append(cancelled)
master.to_csv('Merged_Enrollment.csv')
cancelled_courses_department=[]
for index,row in cancelled.iterrows():   
    cancelled_courses_department.append(row['Course Prefix'])       

cancelled_courses_department_list=list(set(cancelled_courses_department))
cancelled_courses_department_dict={}
for i in cancelled_courses_department_list:
    cancelled_courses_department_dict[i]=0
for i in cancelled_courses_department:
    cancelled_courses_department_dict[i]+=1



plt.bar(cancelled_courses_department_dict.keys(), cancelled_courses_department_dict.values(), color='g')
plt.xlabel('Department')
plt.title('Cancelled Courses in Departments')
plt.ylabel('Frequency')
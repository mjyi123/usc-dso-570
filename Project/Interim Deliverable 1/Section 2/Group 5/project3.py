#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  6 10:03:30 2018

@author: xiaonaiyuan
"""

#####Calculate Course popularity and classify them
import pandas as pd
import numpy as np
enrollment=pd.read_excel("Marshall_Course_Enrollment_1516_1617.xlsx")

total_course=[]
register_count=[]
class_seat=[]
enrollment_rate=[]
for index,row in enrollment.iterrows():
    total_course.append(row['Course'])
    register_count.append(row['Reg Count'])
    class_seat.append(row['Seats'])
    enrollment_rate.append(row['Reg Count']/row['Seats'])

enrollment_courses_list=list(set(total_course))
enrollment_courses_dict={}
enrollment_courses_dict_count={}
enrollment_courses_rate={}

for i in enrollment_courses_list:
    enrollment_courses_dict_count[i]=0
for i in enrollment_courses_list:
    enrollment_courses_dict[i]=0
    
for i in range(len(total_course)):
    enrollment_courses_dict_count[total_course[i]]+=1
    enrollment_courses_dict[total_course[i]]+=enrollment_rate[i]
    
for i in enrollment_courses_list:
    enrollment_courses_rate[i]=enrollment_courses_dict[i]/enrollment_courses_dict_count[i]
for i in enrollment_courses_rate:
    if enrollment_courses_rate[i]>1:
        enrollment_courses_rate[i]=1
 
enrollment_courses_rate
popular_course=[]
normal_course=[]
less_popular_course=[]
for i in enrollment_courses_rate:
    if enrollment_courses_rate[i]>0.7:
        popular_course.append(i)
    elif enrollment_courses_rate[i]<0.3:
        less_popular_course.append(i)
    else:
        normal_course.append(i)


print("The number of popular courses is:", len(popular_course))
print("The number of normal courses is:", len(normal_course))
print("The number of less popular courses is:", len(less_popular_course))

#np.array([enrollment_courses_rate[i] for i in enrollment_courses_rate]).argsort()[0,10]


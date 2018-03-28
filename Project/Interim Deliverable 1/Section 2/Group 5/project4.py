#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  6 11:43:41 2018

@author: xiaonaiyuan
"""
import pandas as pd
instructor_course=pd.read_excel("Marshall_Course_Enrollment_1516_1617.xlsx")
instructor_distinct=list(set(instructor_course['First Instructor']))

instructor_student_number_dict={}
for i in instructor_distinct:
    instructor_student_number_dict[i]=0

for i in range(2899):
    instructor_student_number_dict[instructor_course['First Instructor'][i]]+=instructor_course['Reg Count'][i]
    
instructor_student_number_dict_top={}
for i in instructor_student_number_dict:
    if instructor_student_number_dict[i]>1000:
        instructor_student_number_dict_top[i]=instructor_student_number_dict[i]
        
instructor_student_number_dict_top
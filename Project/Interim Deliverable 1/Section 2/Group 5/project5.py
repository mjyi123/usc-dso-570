#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  6 11:19:51 2018

@author: xiaonaiyuan
"""
import pandas as pd


course_selection=pd.read_excel("Student_Course_Selection_1516.xlsx")

major=[]
student_number=[]
for index,row in course_selection.iterrows():
    major.append(row['Major'])
    student_number.append(row['# Students'])

major_distinct=list(set(major))
major_courses_dict={}

for i in major_distinct:
    major_courses_dict[i]=0
for i in range(len(major)):
    major_courses_dict[major[i]] += student_number[i]

major_courses_dict.head()
major_courses_dict_top={}
for i in major_courses_dict:
    if major_courses_dict[i]>30000:
        major_courses_dict_top[i]=major_courses_dict[i]
major_courses_dict_top
plt.bar(major_courses_dict_top.keys(), major_courses_dict_top.values(), color='g')
plt.xticks(fontsize=5)
plt.xlabel('Department')
plt.title('Number of Student Courses in Departments')
plt.ylabel('Students choosing times')
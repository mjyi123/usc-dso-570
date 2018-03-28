#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 19:52:28 2018

@author: xiaonaiyuan
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def convert(inputTime):
    # Code copy pasted from challenge 1, except first convert input to string before splitting
    try:
        hh,mm,ss=str(inputTime).split(':')
        ans=int(hh)+int(mm)/60+int(ss)/3600
    except:
        ans=np.nan
    return ans


def loadDataDict(df,roomSet):
    # Code copy pasted from challenge 2, except adding entries to a list instead of finding beginning and end, and adding empty list for unused classrooms
    ans={}
    # Start with empty lists in all classrooms
    terms=[20153,20161,20162,20163,20171,20172]
    for term in terms:
        for room in roomSet:
            for day in 'MTWHF':
                ans[term,room,day]=[]
    for index,row in df.iterrows():   
        term=row['Term']       # Obtain the corresponding column of each row
        room=row['First Room']
        days=row['First Days'] 
        beg=convert(row['First Begin Time'])   # Convert the begin time strings into decimal numbers using challenge 1
        end=convert(row['First End Time'])     # Convert the begin time strings into decimal numbers using challenge 1
        # Skip rows in which beg and end are np.nan (not a number), and in which the room is not in the capacity file
        #import pdb; pdb.set_trace()
        if np.isnan(beg) or np.isnan(end) or room not in roomSet:  
            continue     # Command to skip this iteration of the loop
        for day in 'MTWHF':   # Iterate through the sequence ['M','T','W','H','F']
            if day in days: 
                ans[term,room,day].append([beg,end])
    
    return ans
                    
def computeUsage(inputList, primeStart,primeEnd):
    # Code copy pasted from challenge 3, except sorting the inputList
    sortedList=sorted(inputList)
    usage=0
    prev=0
    for start,end in sortedList:
        if end<primeStart:
            continue
        if start>primeEnd:
            break
        start=max(prev,start)
        end=max(prev,end)
        overlap=max(0,min(primeEnd,end)-max(primeStart,start))
        usage+=overlap
        prev=end
    return usage/(primeEnd-primeStart)

# Beginning of main code.
primeStart=10
primeEnd=16

# Read in data
schedule=pd.read_excel('Marshall_Course_Enrollment_1516_1617.xlsx')
cancelled=pd.read_excel('Cancelled_Courses_1516_1617.xlsx')
master=schedule.append(cancelled)
capacities=pd.read_excel('Marshall_Room_Capacity_Chart.xlsx')

# Set rooms to focus on to be those in the capacity file.
roomSet=set(capacities.Room)

# Load the data from the master DataFrame into a dictionary of the format in challenge 2
dataDict=loadDataDict(master,roomSet)

# Create a list of lists, corresponding to the data we want to dump out. 
lines=[]
for term,room,day in loadDataDict(master,roomSet):
    # Each row of the output data has columns being term, room, day, utilization
    lines.append([term,room,day,computeUsage(dataDict[term,room,day],primeStart,primeEnd)])

# Store data back into a dataframe
output=pd.DataFrame(lines,columns=['Term','Room','Day','Utilization'])

# Output to a file
output.to_csv('RoomUsage.csv')

def average(seq, total=0.0): 
  num = 0 
  for item in seq: 
    total += item 
    num += 1 
  return total / num

average(output['Utilization'])
















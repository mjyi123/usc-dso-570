# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# import required packages
import pandas as pd
import numpy as np
import os

# set the working directory
path="/Users/srivijay/Desktop/Classes/Spring 18/Optimization & Probability class/Final Project/Cleandata"
os.chdir(path)

# Read files using pandas
xl = pd.ExcelFile("Department_Allocations_20171.xlsx")

xl.sheet_names
[u'Sheet1']
df = xl.parse("Sheet1")
df.head()


xl_1 = pd.ExcelFile("Marshall_Course_Enrollment_1516_1617.xlsx")

xl_1.sheet_names
[u'Schedules',u'Codebook']
df_1 = xl_1.parse("Schedules")
df_1.head()

# Select only required rows 
df_1 = df_1[(df_1.Term == 20171)]

# Select only required fields
df_1 = df_1[['FirstRoom', 'First Days', 'First Begin Time','First End Time','Course Prefix','Department']]

df = df[['Room','Days','Start Time','End Time','Department']]

# recode department names

df_1["Department"] = df_1["Department"].replace('IBEAR Program', 'IBEAR')

df["Department"] = df["Department"].replace('CMC','BUCO')


# change time
def convertTime(x,n) :
  split= str(x).split(' ')
  df=pd.DataFrame(split)
  df.columns =['hrs','AMPM']

  split_hrs=str(df[["hrs"]]).split=(':')
  m=np.array(map(str.strip, split_hrs))
  df[["hrs"]]=int(m[:,1])+int(m[:,2])/60 

  df[["hrs"]][df[["AMPM"]]=='PM' & df[["hrs"]]<12]=df[["hrs"]][df[["AMPM"]]=='PM' & df[["hrs"]]<12]+12
  df[["hrs"]][df[["AMPM"]]=='AM' & df[["hrs"]]>12]=df[["hrs"]][df[["AMPM"]]=='AM' & df[["hrs"]]>12]-12
  return(df[["hrs"]])

df[["Start"]]=convertTime(df[["Start Time"]],2)
df[["End"]]=convertTime(df[["End Time"]],2)


#recode & remove missing value before convert
df_1[["First Begin Time"]][df_1[["First Begin Time"]]=='' | df_1[["First Begin Time"]]=='TBA']=NA
df_1[["First End Time"]][df_1[["First End Time"]]=='' | df_1[["First End Time"]]=='TBA']=NA
df_1=df_1[(isnull(df_1[["First Begin Time"]])==0 & isnull(df_1[["First End Time"]])==0)]

df_1[["Start"]]=convertTime(df_1[["First Begin Time"]],3)
df_1[["End"]]=convertTime(df_1[["First End Time"]],3)


# Melt data according to days
days=c('M','T','W','H','F','S','U')

def grep(l, s):
   return [i for i in l if s in i]

for i in (days) :
  df[[i]]=NA
  index=grep(df[["Days"]],i)
  df[index,i]=i

for i in (days) :
  df_1[[i]]=NA
  index=grep(df_1[["First Days"]],i)
  enr[index,i]=i

df_melt=pd.melt(df, var_name = days)
df_melt=df_melt[isnull(df_melt[["value"]])==0,]
df_1_melt= pd.melt(df_1, var_name = days)
df_1_melt=df_1_melt[isnull(df_1_melt[["value"]])==0,]

# Calculated % match
#f=function(x){}

df_melt[["id"]]=paste(df_melt[["Room"]],df_melt[["value"]], df_melt[["Department"]],sep = '-')
df_1_melt[["id"]]=paste(df_1_melt[["FirstRoom"]],df_1_melt[["value"]], df_1_melt[["Department"]],sep = '-')
id=unique(df_melt[["id"]],df_1_melt[["id"]])
intersect(df_melt[["id"]], df_1_melt[["id"]])

overlap=0
for i in (intersect(df_melt[["id"]], df_1_melt[["id"]])) :
  query = IRanges(int(df_melt[df_melt[["id"]]==i,'Start']*60), int(df_melt[df_melt[["id"]]==i,'End']*60))
  subject = IRanges(int(df_1_melt[df_1_melt[["id"]]==i,'Start']*60), int(df_1_melt[df_1_melt[["id"]]==i,'End']*60))
  overlap = overlap + sum(width(subsetByOverlaps(query,subject)))
  # print(query)
  # print(subject)
  # print(overlap)

overlap #46,383

n_df=sum(df_melt[["End"]]*60 - df_melt[["Start"]]*60) #133,404

n_assign=sum(df_melt[["End"]][df_melt[["Department"]]!='Unassigned']*60 -
      df_melt[["Start"]][df_melt[["Department"]]!='Unassigned']*60) #102204

match=overlap/n_assign
match
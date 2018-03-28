setwd('~/Google Drive/Courses/DSO570 - Data, Model and Effective Decisions - Spring 2018/Final Project/Cleandata')

# alc=read.delim('Department_Allocations_20171.txt', header = T)
# enr=read.delim('Marshall_Course_Enrollment_1516_1617.txt', header = T)

library(gdata)
alc=read.delim('Department_Allocations_20171.txt', header = T) 
enr=read.xls('Marshall_Course_Enrollment_1516_1617.xlsx', sheet = 1, header = T)

enr=enr[enr$Term==20171, c('FirstRoom', 'First.Days', 'First.Begin.Time','First.End.Time','Course.Prefix','Department')]
alc=alc[,c(1,3:6)]

#recode department names
library(plyr)
enr$Department=mapvalues(enr$Department, from=c('IBEAR Program'), to=c('IBEAR'))
levels(enr$Department)

alc$Department=revalue(alc$Department, c("CMC"="BUCO"))
levels(alc$Department)

table(alc$Department)
table(enr$Department)

# change time
convertTime=function(x,n) {
  split=strsplit(as.character(x), split=' ')
  df=data.frame(matrix(unlist(split), ncol=2, byrow = T))
  colnames(df)=c('hrs','AMPM')

  split.hrs=strsplit(as.character(df$hrs), split=':')
  m=matrix(unlist(split.hrs), ncol=n, byrow = T)
  df$hrs=as.numeric(m[,1])+as.numeric(m[,2])/60 

  df$hrs[df$AMPM=='PM' & df$hrs<12]=df$hrs[df$AMPM=='PM' & df$hrs<12]+12
  df$hrs[df$AMPM=='AM' & df$hrs>12]=df$hrs[df$AMPM=='AM' & df$hrs>12]-12
  return(df$hrs)
}

alc$Start=convertTime(alc$Start.Time,2)
alc$End=convertTime(alc$End.Time,2)

#recode & remove missing value before convert
enr$First.Begin.Time[enr$First.Begin.Time=='' | enr$First.Begin.Time=='TBA']=NA
enr$First.End.Time[enr$First.End.Time=='' | enr$First.End.Time=='TBA']=NA
enr=enr[is.na(enr$First.Begin.Time)==0 & is.na(enr$First.End.Time)==0,]

enr$Start=convertTime(enr$First.Begin.Time,3)
enr$End=convertTime(enr$First.End.Time,3)

# Melt data according to days
days=c('M','T','W','H','F','S','U')
for (i in days) {
  alc[,i]=NA
  index=grep(i, alc$Days)
  alc[index,i]=i
}
for (i in days) {
  enr[,i]=NA
  index=grep(i, enr$First.Days)
  enr[index,i]=i
}

library(reshape2)
alc.melt=melt(alc, measure.vars = days)
alc.melt=alc.melt[is.na(alc.melt$value)==0,]
enr.melt=melt(enr, measure.vars = days)
enr.melt=enr.melt[is.na(enr.melt$value)==0,]

# alc.melt[alc.melt$Room=='JFF236' & alc.melt$value=='M',]$Start
# enr.melt[enr.melt$FirstRoom=='JFF236' & enr.melt$value=='M',]$Start

# Calculated % match
library(IRanges)

alc.melt$id=paste(alc.melt$Room,alc.melt$value, alc.melt$Department,sep = '-')
enr.melt$id=paste(enr.melt$FirstRoom,enr.melt$value, enr.melt$Department,sep = '-')
id=unique(c(alc.melt$id,enr.melt$id))
# intersect(alc.melt$id, enr.melt$id)

overlap=0
for (i in id) {
  query = IRanges(as.integer(alc.melt[alc.melt$id==i,'Start']*60), as.integer(alc.melt[alc.melt$id==i,'End']*60))
  subject = IRanges(as.integer(enr.melt[enr.melt$id==i,'Start']*60), as.integer(enr.melt[enr.melt$id==i,'End']*60))
  overlap = overlap + sum(width(intersect(query,subject)))
  # print(query)
  # print(subject)
  # print(overlap)
}
overlap #43,854

n.alc=sum(alc.melt$End*60 - alc.melt$Start*60) #133,404

n.assign=sum(alc.melt$End[alc.melt$Department!='Unassigned']*60 -
      alc.melt$Start[alc.melt$Department!='Unassigned']*60) #102204

match=overlap/n.assign
match

table(alc.melt$Department[alc.melt$Department!='Unassigned'])
table(alc.melt$Room[alc.melt$Department!='Unassigned'])

## Data visualization

# calculate intersected hours for each slot individually
alc.melt$match=NA
for (i in 1:nrow(alc.melt)) {
  query = IRanges(as.integer(alc.melt[i,'Start']*60), as.integer(alc.melt[i,'End']*60))
  subject = IRanges(as.integer(enr.melt[enr.melt$id==alc.melt[i,'id'],'Start']*60), as.integer(enr.melt[enr.melt$id==alc.melt[i,'id'],'End']*60))
  alc.melt$match[i]=max(0,width(intersect(query,subject)))/60
}

alc.melt$width=alc.melt$End-alc.melt$Start

# Calculate AMI by department
data=data.frame(Department=c('All', levels(alc.melt$Department)))
rownames(data)=data$Department
for (i in data$Department) {
  data$AMI[data$Department==i] = 
    sum(alc.melt$match[alc.melt$Department==i]) /
    sum(alc.melt$width[alc.melt$Department==i])
}
data['All', 'AMI']=match

# plot
library(ggplot2)
order=data$Department[c(1:7,11,12,8:10,13:16)]
ggplot(data,aes(x=Department, y=AMI)) + 
  geom_bar(stat='identity', fill = ifelse(data$Department=='All','tomato','darkgrey')) +
  scale_x_discrete(limits=order) +
  theme(axis.text.x = element_text(size=10, angle = 45)) 
  
  
  

# output processed data
write.table(enr.melt, file = 'enrollment.txt', sep = '\t', quote = F)
write.table(alc.melt, file = 'allocation.txt', sep = '\t', quote = F)

# table(paste(alc.melt$Room,alc.melt$value, alc.melt$Department,sep = '-'))

# library(gridExtra)
# library(grid)
# #pdf("test.pdf", height=11, width=8.5)
# table1=as.matrix(table(alc$Department))
# table2=as.matrix(table(enr$Department))
# t3=as.matrix(table(enr$Course.Prefix))
# t4=as.matrix(table(alc$Room))
# t5=as.matrix(table(enr$First.Room))
# t6=as.matrix(table(alc$Days))
# t7=as.matrix(table(enr$First.Days))
# 
# dev.new()
# grid.table(table1)
# 
# dev.new()
# grid.table(table2)
# 
# dev.new()
# grid.table(t3)
# 
# dev.new()
# grid.table(t(t4))
# dev.new()
# grid.table(t5)
# dev.new()
# grid.table(t6)
# dev.new()
# grid.table(t7)
# 
# write.table(t(t4), file = 'tables.txt', sep = '\t', quote = F)
# write.table(t(t5), file = 'tables.txt', sep = '\t', quote = F, append = T)
# write.table(t(t6), file = 'tables.txt', sep = '\t', quote = F, append = T)
# write.table(t(t7), file = 'tables.txt', sep = '\t', quote = F, append = T)
# 
# 
# dev.off()
# 
# library(lubridate)


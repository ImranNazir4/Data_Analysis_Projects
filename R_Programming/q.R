library(readr)
ni <- read.csv("R/national-identity.csv")
#class(ni)
View(national_identity)
#ni=data(ni)
attach(ni)
#mean(ni$age)
#summary(ni)
#hist(age)
#hist(log(age))
library(ggplot2)
ggplot(ni,aes(x=age,y=nat_id_1))+geom_point()

fact=condition
vect=c(fact)
vect

nat_id_mean=mean(nat_id_1)+mean(nat_id_2)+mean(nat_id_3)+mean(nat_id_4)
nat_id_mean=nat_id_mean/4
nat_id_mean

hist(colMeans(ni[ , 5:8]))

hist(age)
hist(meana)

ni$Mean_nat_id=(nat_id_1+nat_id_2+nat_id_3+nat_id_4)/4
ni$Mean_nat_id
  hist(ni$Mean_nat_id)
  hist(log(ni$Mean_nat_id))
sd(ni$Mean_nat_id)  

install.packages('e1071')

library(e1071)

skewness(ni$Mean_nat_id)
kurtosis(ni$Mean_nat_id)
    
ni$Added_Column <- "Value"

ni$Domestic <- (ni$condition="domestic"((nat_id_1+nat_id_2+nat_id_3+nat_id_4)/4))



library("magrittr") # package installations are only needed the first time you use it
library("dplyr")  



domestic<-1:500
foreign<-1:500
i=1
j=1
for (row in 1:nrow(ni))
  {
  
  d= ni[row,]
  print(d$condition)
}

domestic











domestic_nat<-1:250
foreign_nat<-1:250
i=1
j=1
for (row in 1:nrow(nat_id))
{
  d= nat_id[row,]
  if(d$condition=="domestic")
  {
    domestic_nat[i]=((d$nat_id_1+d$nat_id_2+d$nat_id_3+d$nat_id_4)/4)
    i=i+1
  }
  if(d$condition=="foreign")
  {
    foreign_nat[j]=((d$nat_id_1+d$nat_id_2+d$nat_id_3+d$nat_id_4)/4)
    j=j+1
  }
}
domestic_nat[1:i-1]
foreign_nat[1:j-1]


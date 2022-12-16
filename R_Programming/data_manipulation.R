library(readr)
train <- read_csv("R/train.csv")
#View(train)
attach(train)
library(dplyr)

train %>% select(1,4,3)  #extract given column number
train %>% select(1:4)
train %>% select("Order Date","Ship Date")
train %>% select(starts_with("O"))
train %>% select(ends_with("e"))

train %>% filter(`Ship Mode`=='Second Class')

train %>% filter(`Ship Mode`=='Second Class' & `Postal Code`==42420)


train %>% select("Ship Mode","Postal Code")  %>% train %>% filter(`Ship Mode`=='Second Class' & `Postal Code`==42420)

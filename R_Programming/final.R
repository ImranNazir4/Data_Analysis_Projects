library(readr)  #install.packages("readr")-> command to install this package
nat_id <- read_csv("R/national-identity.csv")   #Reading the Data Source  and storing in the variable
view(nat_id)
#View(national_identity)   #un-comment this if you want to view the data

#<--------------------------------------First Point----------------------------------->

#converting "conditon" column to vector
fact=nat_id$condition
fact=factor(fact)
fact
levels(fact)           #getting unique values from condtion column

#<--------------------------------------First Ends----------------------------------->



#<--------------------------------------Second Point----------------------------------->


#Calculate participant mean scores on the 4-item national identity measure.

domestic_mean=0
foreign_mean=0
i=1
j=1
for (row in 1:nrow(nat_id))
{
  d=nat_id[row,]
  if(d$condition=="domestic")
  {
    domestic_mean=domestic_mean+(d$nat_id_1+d$nat_id_2+d$nat_id_3+d$nat_id_4)
  i=i+1
  }
  domestic_mean=  domestic_mean/(i-1)
  
  
  if(d$condition=="foreign")
  {
    foreign_mean=(d$nat_id_1+d$nat_id_2+d$nat_id_3+d$nat_id_4)
    j=j+1
  }
  foreign_mean=foreign_mean/(i-1)
}

#mean of each condition in the column conditon

domestic_mean
foreign_mean

#boxplots   with error bars

#error bars
#error bars are the 95% confidence interval, the bottom and top of the box are the 25th and 75th percentiles,
#the line inside the box is the 50th percentile (median), and any outliers are shown as open circles.

library(ggplot2)  #required package


df <- data.frame(domestic_mean)
gplot(df, aes(y = domestic_mean)) + 
  stat_boxplot(geom = "errorbar",
               width = 0.15) + geom_boxplot()


df <- data.frame(foreign_mean)
gplot(df, aes(y = foreign_mean)) + 
  stat_boxplot(geom = "errorbar",
               width = 0.15) + geom_boxplot()




#<--------------------------------------Second Ends----------------------------------->


#<--------------------------------------Third Point----------------------------------->


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


#Means

mean(domestic_nat[1:i-1])
mean(foreign_nat[1:j-1])

#Standard Deviation

sd(domestic_nat[1:i-1])
sd(foreign_nat[1:j-1])



#Descriptive Statistics
describe(domestic_nat[1:i-1])
describe(foreign_nat[1:j-1])



#Skewness

library(e1071)  #required package   #install.packages("e1071")-> command to install this package

#The skewness value can be positive or negative, or even undefined. 
#If skewness is between -1 and -0.5 or between 0.5 and 1, the distribution is moderately skewed.
#If skewness is between -0.5 and 0.5,
#the distribution is approximately symmetric.

skewness(domestic_nat[1:i-1])
skewness(foreign_mean)


library(e1071)  #required package

#A standard normal distribution has kurtosis of 3 and is recognized as mesokurtic.
#An increased kurtosis (>3) can be visualized as a thin "bell" with a high peak 
#whereas a decreased kurtosis corresponds to a broadening of the peak and "thickening" of the tails.
#Kurtosis >3 is recognized as leptokurtic and <3.

kurtosis(domestic_nat[1:i-1])
kurtosis(foreign_nat[1:j-1])





#<--------------------------------------Third End----------------------------------->


#<--------------------------------------Fourth Point----------------------------------->


#Shapiro-Wilk test 
#used for checking whether data is normally distributed or not
#H0:Data is Normally Distributed (Null Hypothesis)
#H1:Data is Not Normally Distributed (Alternative Hypothesis)


#value of the Shapiro-Wilk Test is greater than 0.05, the data is normal.
#If it is below 0.05, the data significantly deviate from a normal distribution.
#If you need to use skewness and kurtosis values to determine normality, rather the Shapiro-Wilk test,
#you will find these in our enhanced testing for normality guide

#for domestic population
shapiro.test(domestic_nat[1:i-1])

#for foreign population
shapiro.test(foreign_nat[1:j-1])

#you can accept and reject null hypothesis based on final results

#<--------------------------------------Fourth End----------------------------------->



#<--------------------------------------Fifth Point----------------------------------->


#Wilch Test
#he Welch t-test is an adaptation of Student's t-test. It is used to
#compare the means of two groups of samples when the variances are different.

#We want to compare relationship the domestic scores and foreign national scores.



t.test(domestic_nat[1:i-1],foreign_nat[1:j-1])



#How do you interpret t test results?
#Higher values of the (p)t-value, also called (p)t-score, indicate that a large difference exists between the two sample sets.
#The smaller the t-value, the more similarity exists between the two sample sets. A large t-score indicates that the groups are different.
#A small t-score indicates that the groups are similar


#<--------------------------------------Fifth End----------------------------------->



#<--------------------------------------Sixth Point----------------------------------->



#Cohen's d test 

cohen.d(domestic_nat[1:i-1],foreign_nat[1:j-1] , pooled=TRUE, paired=FALSE, na.rm=FALSE, 
        hedges.correction = FALSE, conf.level = 0.95, noncentral = FALSE)


#Cohen's d. Cohen's d is an appropriate effect size for the comparison between two means
#Cohen suggested that d = 0.2 be considered a 'small' effect size, 0.5 represents a 'medium' effect size and 0.8 a 'large' effect size.


#<--------------------------------------Sixth End----------------------------------->

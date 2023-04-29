#importing dependencies
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#reading the data according to last digit of student id
df=pd.read_csv('data6.csv',names=['weight'])

#converting the data into array
data=np.array(df.values.reshape(-1))

#creating histogram from given data
plt.hist(data,bins=10)
plt.title('New Born Babies Weights Distribution')

#mean
W=np.mean(data)
print(W)

#standard deviation
S=np.std(data)
print(S)


# # Method 1 - Z Score
#The given data is well normally distributed so we can apply zcore method to calculate value of X

z_table=1.28   #z table value corresponds to 90% area
X=W+(z_table*S)
print(X)

#visualizing the results
plt.hist(data,bins=10)
plt.axvline(W,color='red',label='W')
plt.axvline(X,color='black',label='X')
plt.legend()

# # Cross Verification
X= 100 * np.sum(data > 3.897068) / len(data)
print(X)

#9.5 rounded to 10 which mean 10% values are greater than this 3.8970688822935893 value


# # Method 2 : Percentile
#Our taget is to find 90th percentile so that we can find values that are greater than X

percentile=np.percentile(data,90)   #90th percentile
print(percentile)

#visualization of results
plt.hist(data,bins=10)
plt.axvline(W,color='red',label='W')
plt.axvline(percentile,color='black',label='X')
plt.legend()


# # Cross Verification

X= 100 * np.sum(data > 3.870394) / len(data)
print(X)
# 10% values are greater than 3.870394 this

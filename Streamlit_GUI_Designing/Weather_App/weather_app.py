#loading packahes
import pandas as pd
import numpy as np
import streamlit as st
import pickle as pkl
import seaborn as sns
import matplotlib.pyplot as plt

#loading models
rf_regressor=pkl.load(open("rf_regressor.sav", "rb"))
minmax_scaler=pkl.load(open("minmax_scaler.sav", "rb"))


st.set_page_config(layout="wide")
st.title("ETP Quotidien Predictor Application")
#sidebar
menu=["Predictive Modelling","Metrics"]

selected_menu=st.sidebar.selectbox("Select",menu)
if selected_menu=="Predictive Modelling":
	st.header("Enter Details")
	col1,col2,col3,col4=st.columns(4)
	with col1:
		feat1 = st.date_input("Date/heure")
	with col2:
		feat2 = st.number_input("moy_Temp[°C]")
	with col3:
		feat3 = st.number_input("max_Temp[°C]")
	with col4:
		feat4 = st.number_input("min_Temp[°C]")
	col5,col6,col7,col8=st.columns(4)
	with col5:
		feat5 = st.number_input("moy_DewPoint[°C]")
	with col6:
		feat6 = st.number_input("min_DewPoint[°C]")
	with col7:
		feat7 = st.number_input("moy_SolarRadiation[W/m2]")
	with col8:
	 	feat8 = st.number_input("moy_VPD[kPa]")
	col9,col10,col11,col12=st.columns(4)
	with col9:
		feat9 = st.number_input("min_VPD[kPa]")
	with col10:
		feat10 = st.number_input("moy_RelativeHumidity[%]")
	with col11:
		feat11 = st.number_input("max_RelativeHumidity[%]")
	with col12:
		feat12 = st.number_input("min_RelativeHumidity[%]")
	col13,col14,col15,col16=st.columns(4)
	with col13:
		feat13 = st.number_input("Somme_Precipitation[mm]")
	with col14:
		feat14 = st.number_input("moy_WindSpeed[m/s]")
	with col15:
		feat15 = st.number_input("max_WindSpeed[m/s]")
	with col16:
		feat16 = st.number_input("max_WindSpeedMax[m/s]")
	st.write("")
	st.write("")
	st.write("")
	year,month,day=str(feat1).split("-")
	input_feat=[feat2,feat3,feat4,feat5,feat6,feat7,feat8,feat9,feat10,feat11,feat12,feat13,feat14,feat15,feat16,int(year),int(month),int(day)]
	scaled_data=minmax_scaler.transform([input_feat])
	col1,col2,col3,col4,col5=st.columns(5)
#making predictions
	if st.button("Submit"):
		result=rf_regressor.predict(scaled_data)
		st.title("Predicted ETP Quotidien")
		st.subheader(result[0])
#metrics
elif selected_menu=="Metrics":
	st.subheader("Model Accuracy Metrics")
	metrics=[0.9960,0.9818,0.2184,0.1514,0.9818]
	metrics_lables=["Training Accuracy","Testing Accuracy","RMSE","MAE","R Square"]
	fig = plt.figure(figsize=(15,5))
	sns.barplot(x =metrics_lables, y=metrics)
	plt.title("Model Metrics")
	st.pyplot(fig)
	st.title("Average Distribution of Data Features")
	st.write("")
	st.write("")
	data=pd.read_csv("preprocessed_data.csv")
	avg_temps=data.groupby(['year']).mean()
	col1,col2=st.columns(2)
	with col1:
		fig = plt.figure(figsize=(15,5))
		sns.lineplot(x=avg_temps.index,y=avg_temps['moy_Temp[°C]'],color='blue')
		plt.title('Average moy_Temp[°C] over the years')
		st.pyplot(fig)
	with col2:
		fig = plt.figure(figsize=(15,5))
		sns.lineplot(x=avg_temps.index,y=avg_temps['max_Temp[°C]'])
		plt.title('Average moy_Temp[°C] over the years')
		st.pyplot(fig)
	col3,col4=st.columns(2)
	with col3:
		fig = plt.figure(figsize=(15,5))
		sns.lineplot(x=avg_temps.index,y=avg_temps['min_Temp[°C]'],color='green')
		plt.title('Average min_Temp[°C] over the years')
		st.pyplot(fig)
	with col4:
		fig = plt.figure(figsize=(15,5))
		sns.lineplot(x=avg_temps.index,y=avg_temps['moy_DewPoint[°C]'],color='purple')
		plt.title('Average moy_DewPoint[°C] over the years')
		st.pyplot(fig)
	col5,col6=st.columns(2)
	with col5:
		fig = plt.figure(figsize=(15,5))
		sns.lineplot(x=avg_temps.index,y=avg_temps['min_DewPoint[°C]'])
		plt.title('Average min_DewPoint[°C] over the years')
		st.pyplot(fig)
	with col6:
		fig = plt.figure(figsize=(15,5))
		sns.lineplot(x=avg_temps.index,y=avg_temps['moy_SolarRadiation[W/m2]'],color='red')
		plt.title('Average moy_SolarRadiation[W/m2] over the years')
		st.pyplot(fig)
	col6,col7=st.columns(2)
	with col6:
		fig = plt.figure(figsize=(15,5))
		sns.lineplot(x=avg_temps.index,y=avg_temps['moy_VPD[kPa]'],color='purple')
		plt.title('Average moy_VPD[kPa] over the years')
		st.pyplot(fig)
	with col7:
		fig = plt.figure(figsize=(15,5))
		sns.lineplot(x=avg_temps.index,y=avg_temps['min_VPD[kPa]'])
		plt.title('Average min_VPD[kPa] over the years')
		st.pyplot(fig)
	col8,col9=st.columns(2)
	with col8:
		fig = plt.figure(figsize=(15,5))
		sns.lineplot(x=avg_temps.index,y=avg_temps['moy_RelativeHumidity[%]'],color='violet')
		plt.title('Average moy_RelativeHumidity[%] over the years')
		st.pyplot(fig)
	with col9:
		fig = plt.figure(figsize=(15,5))
		sns.lineplot(x=avg_temps.index,y=avg_temps['max_RelativeHumidity[%]'],color='green')
		plt.title('Average max_RelativeHumidity[%] over the years')
		st.pyplot(fig)
	col10,col11=st.columns(2)
	with col10:
		fig = plt.figure(figsize=(15,5))
		sns.lineplot(x=avg_temps.index,y=avg_temps['min_RelativeHumidity[%]'],color='black')
		plt.title('Average min_RelativeHumidity[%] over the years')
		st.pyplot(fig)
	with col11:
		fig = plt.figure(figsize=(15,5))
		sns.lineplot(x=avg_temps.index,y=avg_temps['Somme_Precipitation[mm]'])
		plt.title('Average Somme_Precipitation[mm] over the years')
		st.pyplot(fig)
	col12,col13=st.columns(2)
	with col12:
		fig = plt.figure(figsize=(15,5))
		sns.lineplot(x=avg_temps.index,y=avg_temps['moy_WindSpeed[m/s]'],color='blue')
		plt.title('Average moy_WindSpeed[m/s] over the years')
		st.pyplot(fig)
	with col13:
		fig = plt.figure(figsize=(15,5))
		sns.lineplot(x=avg_temps.index,y=avg_temps['max_WindSpeed[m/s]'],color='green')
		plt.title('Average max_WindSpeed[m/s] over the years')
		st.pyplot(fig)
	col14,col15=st.columns(2)
	with col14:
		fig = plt.figure(figsize=(15,5))
		sns.lineplot(x=avg_temps.index,y=avg_temps['max_WindSpeedMax[m/s]'])
		plt.title('Average max_WindSpeedMax[m/s] over the years')
		st.pyplot(fig)
	with col15:
		fig = plt.figure(figsize=(15,5))
		sns.lineplot(x=avg_temps.index,y=avg_temps['ETP quotidien [mm]'],color='purple')
		plt.title('Average ETP quotidien [mm] over the years')
		st.pyplot(fig)


import pickle as pkl
import numpy as np
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import time
model = pkl.load(open("finalized_model.sav", "rb"))
student_df=pd.read_excel("ALL COMBINED.xlsx",engine='openpyxl')
add_selectbox = st.sidebar.selectbox("Students Section",(["CGPA Prediction","Student Dashboard","Explore a Student"]))



if add_selectbox=="CGPA Prediction":
   #cpga prediction
   st.title("CGPA Prediction")
   #with st.form("my_form", clear_on_submit=False):
   st.header("Enter Details")
   std_hrs = st.number_input("Enter study hours per week",min_value=15, max_value=50)
   sem1 = st.number_input("Enter GPA of  1st Semester",min_value=2.0, max_value=10.0)
   sem2 = st.number_input("Enter GPA of  2nd Semester",min_value=2.0, max_value=10.0)
   sem3 = st.number_input("Enter GPA of  3rd Semester",min_value=2.0, max_value=10.0)

   data = np.array([std_hrs, sem1, sem2, sem3]).reshape((1, -1))

   # Every form must have a submit button.
   #  submitted = st.form_submit_button("Submit")
   if st.button("Submit"):
      with st.spinner("Loading..."):
           time.sleep(1)
      res = model.predict(data)
      st.subheader(f"Predicted CPGA is {round(res[0], 3)}")



      x=["Study Hrs","Semester 1","Semester 2","Semester 3","CGPA"]
      y=[std_hrs,sem1,sem2,sem3,round(res[0], 3)]
      fig,ax=plt.subplots()
      sns.barplot(x,y)
      #ax.bar(x,y,color="purple")
      for container in ax.containers:
         ax.bar_label(container)
      plt.title("Student Summary")
      st.pyplot(fig)


      fig,ax=plt.subplots()
      ax.plot(x[1:],y[1:],'o-',color="red")
      ax.bar(x[1:],y[1:],color="black")
      
      for container in ax.containers:
         ax.bar_label(container)
      plt.xticks(rotation='vertical')
      plt.title("GPA Trend")
      st.pyplot(fig)




# studend dashboard
elif add_selectbox=="Student Dashboard":
   st.title("Welcome to Students Section")
   st.write("")
   st.write("")
   st.write("")
   no_of_std=student_df["Name"].dropna().shape[0]
   avg_std_hrs=round(sum(student_df["Study Hours"].dropna())/student_df["Study Hours"].dropna().shape[0],2)
   avg_sgpa_sem1=round(sum(student_df["SGPA_SEMESTER1"].dropna())/student_df["SGPA_SEMESTER1"].dropna().shape[0],2)
   avg_sgpa_sem2=round(sum(student_df["SGPA_SEMESTER2"].dropna())/student_df["SGPA_SEMESTER2"].dropna().shape[0],2)
   avg_sgpa_sem3=round(sum(student_df["SGPA_SEMESTER3"].dropna())/student_df["SGPA_SEMESTER3"].dropna().shape[0],2)
   avg_sgpa_sem4=round(sum(student_df["SGPA_SEMESTER4"].dropna())/student_df["SGPA_SEMESTER4"].dropna().shape[0],2)
   kpi_list=[no_of_std,avg_std_hrs,avg_sgpa_sem1,avg_sgpa_sem2,avg_sgpa_sem2,avg_sgpa_sem3]
   kpi_list_cat=["no_of_std","avg_std_hrs","avg_sgpa_sem1","avg_sgpa_sem2","avg_sgpa_sem2","avg_sgpa_sem3"]
   st.subheader("Overall Student Key Performance")
   fig,ax=plt.subplots(figsize=(12,8))
   ax.bar(kpi_list_cat,kpi_list,color="black")
   for container in ax.containers:
      ax.bar_label(container)
   plt.title("Overall Summary")
   st.pyplot(fig)

   col1,col2=st.columns(2)

   with col1:
      st.subheader("Top Boards")
      board=student_df['BOARD'].value_counts()[0:5]
      x=board.index
      y=board.values
      fig,ax=plt.subplots()
      ax.pie(y,labels=x,autopct="%0.2f")
      plt.xticks(rotation='vertical')
      plt.title("Top 5 Boards")
      st.pyplot(fig)

   with col2:
      st.subheader("Top Streams")
      board=student_df['STREAM'].value_counts()[0:5]
      x=board.index
      y=board.values
      fig,ax=plt.subplots()
      ax.pie(y,labels=x,autopct="%0.2f")
      plt.xticks(rotation='vertical')
      plt.title("Top 5 Streams")
      st.pyplot(fig)

   st.subheader("Top Fields of Interest")

   fig,ax=plt.subplots(figsize=(15,8))
   fld_of_intrst=student_df["FIELD_OF_INTEREST"].value_counts()[0:10]
   x=fld_of_intrst.index
   y=fld_of_intrst.values
   sns.barplot(x,y)
   #ax.bar(kpi_list_cat,kpi_list,color="violet")
   for container in ax.containers:
      ax.bar_label(container)
   plt.title("Field of Interest")
   st.pyplot(fig)

   st.subheader("Field of Interest and SPGA Standings of each Semester")

   field_cpga = student_df.groupby('FIELD_OF_INTEREST').mean()
   field_cpga = field_cpga.reset_index()
   st.table(field_cpga[["FIELD_OF_INTEREST","SGPA_SEMESTER1", "SGPA_SEMESTER2", "SGPA_SEMESTER3", "SGPA_SEMESTER4"]])

#explore a student
elif add_selectbox=="Explore a Student":
   st.title("Explore a Student")
   selected_std=st.selectbox("Select a Student",student_df["Name"].dropna().unique())
   col1,col2,col3,col4,col5=st.columns(5)
   with col1:
      st.write("Name")
      v=student_df[student_df["Name"]==selected_std]
      st.subheader(student_df[student_df["Name"]==selected_std]["Name"].values[0])
   with col2:
      st.write("Study Hours")
      st.subheader(student_df[student_df["Name"]==selected_std]["Study Hours"].values[0])
   with col3:
      st.write("Board")
      st.subheader(student_df[student_df["Name"]==selected_std]["BOARD"].values[0])
   with col4:
      st.write("Stream")
      st.subheader(student_df[student_df["Name"]==selected_std]["STREAM"].values[0])
   with col5:
      st.write("Field of Interest")
      st.subheader(student_df[student_df["Name"]==selected_std]["FIELD_OF_INTEREST"].values[0])

   st.table(student_df[student_df["Name"]==selected_std][["SGPA_SEMESTER1","SGPA_SEMESTER2","SGPA_SEMESTER3","SGPA_SEMESTER4"]])
   cgpa_df=student_df[student_df["Name"]==selected_std][["SGPA_SEMESTER1","SGPA_SEMESTER2","SGPA_SEMESTER3"]]

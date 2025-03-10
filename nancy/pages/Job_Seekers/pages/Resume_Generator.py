import streamlit as st
from project.database import Database
from  project.authenticate import authenticater
from  project.utils import utils
import project.pdf_generator
au = authenticater()
ss = utils()


    
if ss.flag:


    #flag to check if button is clicked
    check_all_flag=0
    check_user_flag=0

    flag=0
   
    db = Database()  
    email = st.text_input('Email Address',value="")
    

    
    if st.checkbox('Check user',key="check_user"):
      check_user_flag=1
      
    
   
    
    if check_user_flag and not email:
     
     st.warning("Please enter your email")
    else:
     if check_user_flag and not au.does_user_exist(email):
      
      st.warning('Use your registered email! please')
     elif check_user_flag and not au.does_userdata_exist(email):
        
        st.warning('No records found with this email.')
        st.warning('If you are a new user kindly visit New Form page.')
     elif check_user_flag and  au.does_userdata_exist(email):
        flag=1      

    if flag:
      project.pdf_generator.main(email)  
      



else:#prevent unordered page access
    st.warning("Cannot access this page directly.")
    st.warning(" Please login in the  Home page first then you may obtain a downloaded copy of your resume.")
        
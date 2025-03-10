import streamlit as st
from project.database import Database
from project.authenticate import authenticater
from project.utils import utils
import logging

db = Database()  
db.create_login_tables()
db.create_form_tables()
au = authenticater()
ss = utils()
def app():
  try:
    ss.init_session_state()
    st.session_state['signout'] = False
    st.session_state['email_placeholder'] = ''
    st.session_state['password_placeholder'] = ''
    if not st.session_state['signout'] and not st.session_state.logged_in:
          choice = st.selectbox('Login/Signup', ['Login', 'Sign up'])
          st.session_state.selected_option = choice
          email = st.text_input('Email Address', value=st.session_state.email_placeholder)
          password = st.text_input('Password', type='password', value=st.session_state.password_placeholder)
          if (st.session_state.selected_option == 'Sign up' and st.session_state['show_signup']):
            username = st.text_input("Enter your username")
            signup_button = st.button('Create my account')
            if signup_button and username and password and email and st.session_state.selected_option == 'Sign up':
              try:
                  if au.does_user_exist(email):
                     st.warning('Sorry, this email is already registered. Please choose a different one.')
                  elif not au.is_valid_email(email):
                     st.warning("Oops! It seems like you've entered an invalid email address. Please double-check and try again.")
                  else:
                    hashed_password = au.hash_password(password)
                    insert_query = "INSERT INTO user_credentials (username, email, password) VALUES (%s, %s, %s)"
                    db.execute_query(insert_query, (username, email, hashed_password))
                    db.commit()
                    st.success('Congratulations! Your account has been successfully created. Welcome to our community!')
                    st.balloons()
                    st.markdown('Now, please log in using your email and password.')
                    st.session_state['show_login'] = False
                    st.session_state['show_signup'] = False
              except Exception as e:
                    st.warning('Error creating account: {}'.format(str(e)))
            elif signup_button:
                   st.warning('Please make sure to fill in all the required details before signing up.')
          if choice == 'Login':
            if "forgot_password" not in st.session_state:
                  st.session_state.forgot_password = False
            def callback():
              st.session_state['forgot_password'] = True
            if(
                st.button("Forgot password",on_click=callback) 
                or st.session_state.forgot_password
              ):
              email = st.text_input('Please enter your email address:')
              if st.button('Send reset link'):
                reset_token = None 
                if au.does_user_exist(email):
                    reset_token=au.generate_reset_token()
                    st.session_state['Send_reset_link'] = True
                    st.session_state['reset_password_triggered']= True
                    au.send_password_reset_email(email, reset_token)
                    #st.experimental_set_query_params(token=reset_token)
                else:
                    st.warning("Oops! We couldn't find an account with that email address. Please double-check your email or sign up for a new account.")
                    st.session_state['Send_reset_link'] = False
            login = st.button('Login')
            if login and email and password:
              au.authenticate_user(email, password)
            elif login:
              st.warning('Please make sure to fill in all the required details before signing up.')
    if st.session_state.logged_in:
      ss.flag = True
      #username = st.session_state.username
      st.title(f'Welcome back!')
      
      st.session_state['signout'] = True
      st.button('Sign out', on_click=ss.sign_out)
      #session_state.logged_in = False
  except KeyError as ke:
    st.title(" ")
app()
 
            


  
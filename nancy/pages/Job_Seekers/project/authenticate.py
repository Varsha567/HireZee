from project.database import Database
import streamlit as st
import hashlib
import re
import uuid
from project.utils import utils
import ssl
import smtplib
from project.utils import utils
ss = utils()
def hash_password1(password):
        return hashlib.sha256(password.encode()).hexdigest()
class authenticater :
    def is_valid_github_link(self,project_link):
        # GitHub repository URL pattern
        github_pattern = r"^https://github.com/[\w-]+/[\w-]+(\.git)?$"
        # Check if the input matches the GitHub repository URL pattern
        match_result = bool(re.match(github_pattern, project_link.strip()))
        return match_result
    def is_valid_name(self,name):
        name_pattern = r"^[A-Za-z'-]+$"
        return bool(re.match(name_pattern, name))
    def generate_reset_token(self):
        return str(uuid.uuid4())
    def hash_password(self,password):
        return hashlib.sha256(password.encode()).hexdigest()
    def does_user_exist(self,email):
        db = Database()  
        try:
            query = "SELECT * FROM user_credentials WHERE email = %s "
            #db.execute_query(query,(email,))
            user = db.fetch_one(query,(email,))
            return user is not None
        except Exception as e:
            st.warning('Failed: {}'.format(str(e)))
    def authenticate_user(self,email, password):
        db = Database() 
        try:
            hashed_password = hash_password1(password)
            query = "SELECT * FROM user_credentials WHERE email = %s AND password = %s"
            #db.execute_query(query, (email, hashed_password))
            user = db.fetch_one(query,(email, hashed_password))
            if user:
              st.session_state.username = user[0]
              st.session_state['email'] = email
              ss.login_state()
              st.snow()
            else:
              st.warning("Oops! It looks like there's no account associated with that email address. Please double-check your email or sign up for a new account.")

            
        except Exception as e:
            st.warning('Login Failed: {}'.format(str(e)))
    def is_valid_email(self,email):
        # Define a regular expression pattern for a basic email format check
        pattern = r'^\S+@\S+\.\S+$'
        return re.match(pattern, email) is not None
    def is_valid_phone_number(self,phone_number):
        # Use a simple regular expression for a 10-digit phone number
      pattern = re.compile(r'^\d{10}$')
      return bool(pattern.match(phone_number))
    def does_userdata_exist(self,email):
        db = Database() 
        try:
            query = "SELECT * FROM user_data WHERE email = %s"
            #user = db.execute_query(query,(email,))
            user = db.fetch_one(query, (email,))
            
            return user is not None

        except Exception as e:
            st.warning('Failed: {}'.format(str(e)))
    def send_password_reset_email(self,email, reset_token):
        db = Database() 
        insert_token_query = "INSERT INTO password_reset (email, reset_token) VALUES (%s, %s)"
        db.execute_query(insert_token_query, (email, reset_token))
        db. commit()
        sender_email = "prameelalangu@gmail.com"  # Replace with your email
        sender_password = "dqhfuymjeligvipn"  # Replace with your email passwordC:\Users\17036\Desktop\varsha\pages\pages\reset.py
        receiver_email = email
        body =f"Enter this code is reset page:{reset_token}"
        subject = f"Password Reset from {sender_email}"
        message = f"Subject: {subject}\n\nFrom: {sender_email}\n\n{body}"
        context = ssl.create_default_context()
        #query_params = st.experimental_get_query_params()
        #action_param = query_params.get("action", [None])[0]
        #print(action_param)
        if reset_token :
            #if action == "set_values":
            # Perform actions to set values based on the query parameter
            reset=reset_token
            ss.forgot_password(reset)
            #print("Setting values...")
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, receiver_email, message)
                st.success("Password reset email sent successfully. Check your email for the CODE. Enter the CODE on the password reset page to complete the process.")
        except Exception as e:
            st.error(f"Error sending email: {e}")
    def is_valid_all(self,input_string):
    
        pattern = re.compile(r'[0-9#$%^&*()!@~<>?/\|_+=\[\]{}"\'\\]')
        return bool(pattern.search(input_string))
    def is_valid_award(self,input_string):
        pattern = re.compile(r'[#$%^&*()!@~<>?/\|_+=\[\]{}"\'\\]')
        return  bool(pattern.search(input_string))
    def is_valid_company(self,input_string):
        pattern = re.compile(r'[#$%^*()!@~<>?/\|_+=\[\]{}"\'\\]')
        return  bool(pattern.search(input_string))
    def is_valid_objective(self,input_string, max_length=150):
        pattern = re.compile(r'[0-9#$%^&*()!@~<>?/\|_+=\[\]{}"\'\\]')
        if not bool(pattern.search(input_string)):
            if len(input_string) <= max_length:
                return True
        else:
            return False

    
    
    
    
    


    
   
    



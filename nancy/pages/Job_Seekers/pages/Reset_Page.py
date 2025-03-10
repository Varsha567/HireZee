import streamlit as st
import os
import mysql.connector
import importlib
from project.utils import utils
from project.authenticate import authenticater
from project.database import Database

au = authenticater()

def reset_password(token):
        # Set up MySQL connection 
    #st.write(f"Resetting password for token: {token}")
    if deep_instance.flag1:
        
        db = Database()
        st.title("Reset Password page")
        query = "SELECT email FROM password_reset WHERE reset_token = %s"
        #db.execute_query(query, (token,))
        user = db.fetch_one(query,(token,))
        
        if user:
            
            new_token = st.text_input("Enter your unique token:")
            new_password = st.text_input("Enter your new password", type="password")
            confirm_password = st.text_input("Confirm your new password", type="password")
            reset_button=st.button("Reset Password")
            if   reset_button and new_token == token :
                if new_password == confirm_password:
                    # Update the user's password in the database
                    hashed_password = au.hash_password(new_password)
                    update_query = "UPDATE user_credentials SET password = %s WHERE email = %s"
                    db.execute_query(update_query, (hashed_password, user[0]))
                    db.commit()
                    st.success("Password reset successful. Please refresh the page to log in with your new password.")
                    deep_instance.password_set()
                    delete_query = "DELETE FROM password_reset  WHERE email = %s"
                    try:
                        db.execute_query(delete_query, (user[0],))
                        db.commit()
                    except Exception as e:
                        print(f"Error deleting from password_reset: {e}")
                else:
                    st.warning("Passwords do not match. Please try again.")
            elif  reset_button:
                st.warning("Invalid reset token. Please use the link from your email.")
        else:
                st.warning("Invalid reset token. Please use the link from your email.")
            
        
    else:
        st.warning("Access denied. This page is meant for password reset requests")

deep_instance = utils()

if deep_instance.flag1:
    
    token = deep_instance.resetT
    reset_password(token)
else:
    st.warning("Access denied. This page is meant for password reset requests")

    
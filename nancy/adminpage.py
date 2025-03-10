import streamlit as st
import json
from streamlit_lottie import st_lottie
import requests

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

# Function to apply local CSS styles
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Function to display the title of the page
def display_title():
    st.markdown("<h1 style='text-align: center; font-size: 2.5em;'>WELCOME TO HIREZEE</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; font-size: 1.5em;'>hire & get hired</h3>", unsafe_allow_html=True)

# Function to display the admin information section
def display_admin_info():
    st.header("ADMIN INFO")
    st.markdown("<h3 style='color: brown;'>hire easy with our hirezee</h3>", unsafe_allow_html=True)
    st.write(
        """
        - hirezee provides advanced screening of resumes beneficial for many companies.
        - you can fetch details of candidates based on your requirements.
        - contact the person that matched your options and hire easily.

        If you are an admin and want to hire candidates for a job, you can proceed further by clicking admin authenticate.
        """
    )

# Function to display Lottie animation for hiring
def display_hiring_animation(lottie_hiring):
    st_lottie(
        lottie_hiring,
        speed=1,
        reverse=False,
        loop=True,
        quality="high",
        height=300,
        width=None,
        key=None,
    )

def display_admin_authentication_button():
    if st.button('Admin Authenticate'):
        st.markdown("[Click for Authentication](http://localhost:8503/)", unsafe_allow_html=True)

# Function to display the contact form
def display_contact_form():
    contact_form = """
    <form action="https://formsubmit.co/gattikoppulasindhu0@gmail.com" method="POST">
         <input type ="hidden" name="_captcha" value="false">
         <input type="text" name="name" placeholder="Your Name" required>
         <input type="email" name="email" placeholder="Your Email" required>
         <textarea name="message" placeholder="Your message goes here" required></textarea>
         <button type="submit">Send</button>
    </form>
    """
    st.header("Contact Us for Queries")
    st.markdown(contact_form, unsafe_allow_html=True)

# Main function to run the Streamlit app
def run_hirezee_app():
    st.set_page_config(page_title="hirezee", page_icon=":computer:", layout="wide")
    
    local_css("style.css")
    
    lottie_hiring = load_lottiefile("hiring.json")

    display_title()
    st.write("##")
    st.write("---")

    l_column, r_column = st.columns((2, 1))
    with l_column:
        display_admin_info()

    with r_column:
        display_hiring_animation(lottie_hiring)

    st.write("#")
    display_admin_authentication_button()
    st.write("#")
    st.write("---")

    left,right =st.columns(2)
    with left:
        display_contact_form()
    with right:
        st.empty()

# Run the app
if __name__ == '__main__':
    run_hirezee_app()

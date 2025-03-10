import streamlit as st
import json
from streamlit_lottie import st_lottie


def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def set_page_configuration():
    st.set_page_config(page_title="hirezee", page_icon=":computer:", layout="wide")

def set_custom_css():
    custom_css = """
        <style>
            body {
                background-color: black;
                color: white;
            }
        </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

def display_welcome_message():
    style_title = """
        <h1 style='
        text-align :center;
        font-size:2.5em;'>
        WELCOME TO HIREZEE
        </h1>
        <h3 style='
        text-align :center;
        font-size:1.5em;'>
        Hire & get hired
        </h3>
    """
    st.markdown(style_title, unsafe_allow_html=True)
    st.write("##")
    st.write("---")

def display_user_info():
    left_column, right_column = st.columns((2, 1))
    with left_column:
        st.header("USER INFO")
        st.write("##")
        st.markdown("<h3 style='color:brown;'>find easy with Hirezee </h3>", unsafe_allow_html=True)
        st.write(
            """
            - Candidates looking for a job can now feel free to submit your resumes.
            - your skills can avail opportunities from any end.
            - can increase the scope of getting selected at high rates with "HIREZEE".

            if you are a user and want to search for a job "can proceed further by clicking user authenticate".
            """
        )
    with right_column:
        st_lottie(
            lottie_coding,
            speed=1,
            reverse=False,
            loop=True,
            quality="low",
            height=300,
            width=None,
            key=None,
        )

def display_user_authentication_button():
    st.write("#")
    if st.button('user authenticate'):
        st.markdown("[click for authentication](http://localhost:8501/)", unsafe_allow_html=True)
    st.write("---")
    st.write("##")

def display_contact_form():
    contact_form = """
    <form action="https://formsubmit.co/hirezee123@gmail.com" method="POST">
         <input type ="hidden" name="_captcha" value="false">
         <input type="text" name="name" placeholder="your name" required>
         <input type="email" name="email" placeholder="your email" required>
         <textarea name="message" placeholder="your message goes here" required></textarea>
         <button type="submit">Send</button>
    </form>
    """
    left, right = st.columns(2)
    with left:
        st.header("contact us for queries")
        st.markdown(contact_form, unsafe_allow_html=True)
    with right:
        st.empty()

if __name__ == "__main__":
    set_page_configuration()
    local_css("style.css")
    lottie_coding = load_lottiefile("coding.json")
    set_custom_css()
    display_welcome_message()
    display_user_info()
    display_user_authentication_button()
    display_contact_form()
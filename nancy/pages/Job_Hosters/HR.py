import ssl
import streamlit as st
import mysql.connector
import hashlib
import uuid
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from  Job Seekers.project.match_module import main

# Set up MySQL connection
db_config = {
    "host": st.secrets["host"],
    "user": st.secrets["user"],
    "password": st.secrets["password"],
    "database": st.secrets["database"]
}

db_connection = mysql.connector.connect(**db_config)
cursor = db_connection.cursor()

# Create "hr_credentials table if it doesn't exist
create_table_query = """
    CREATE TABLE IF NOT EXISTS hr_credentials (
        username VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL PRIMARY KEY,
        password VARCHAR(255) NOT NULL
    )
"""
cursor.execute(create_table_query)
db_connection.commit()

# Create 'admin_requirements' table if it doesn't exist
create_admin_table_query = """
    CREATE TABLE IF NOT EXISTS HR_REQUIREMENTS (
        HR_EMAIL VARCHAR(255) NOT NULL,
        AGE_REQ VARCHAR(255) NOT NULL,
        GENDER_REQ VARCHAR(255) NOT NULL,
        skills VARCHAR(255) NOT NULL,
        LOCATION_REQ VARCHAR(255) NOT NULL,
        languages VARCHAR(255) NOT NULL DEFAULT 'ENGLISH',
        EXPERIENCE_REQ VARCHAR(255) NOT NULL,
        SALARY_REQ VARCHAR(255) NOT NULL
        )"""

cursor.execute(create_admin_table_query)
db_connection.commit()

def init_session_state():
    return {
        'signedout': False,
        'signout': False,
        'username': '',
        'useremail': '',
        'show_admin_form': False,
        'submit_requirements_state': False
    }

# Initialize session state
st.session_state.update(init_session_state())

# Function to send password reset email
def send_password_reset_email(email, token):
    sender_email = st.secrets["mail_id"]  # Replace with your email
    sender_password =st.secrets["app_pswd"]   # Replace with your email password
    receiver_email = email

    body = f"Click the following link to reset your password: http://localhost:8504/reset?token={token}"
    subject = f"Password Reset from {sender_email}"

    message = f"Subject: {subject}\n\nFrom: {sender_email}\n\n{body}"

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message)
            st.success("Password reset email sent. Check your email.")
    except Exception as e:
        st.error(f"Error sending email: {e}")

# Function to generate a unique token for password reset
def generate_reset_token():
    return str(uuid.uuid4())

# Function to display signup error message
def display_signup_error_message(error):
    if "Duplicate entry" in str(error):
        st.warning("An account with this email already exists. Please choose a different email or login.")

# Function to sign out
def sign_out():
    st.session_state['signout'] = False
    st.session_state['username'] = ''
    st.session_state['show_admin_form'] = False

# Function to authenticate user
def authenticate_user(email, password):
    try:
        query = "SELECT * FROM hr_credentials WHERE email = %s AND password = %s"
        cursor.execute(query, (email, password))
        user = cursor.fetchone()

        if user:
            st.session_state['username'] = user[0]
            st.session_state['useremail'] = user[1]
            st.session_state['signedout'] = True
            st.session_state['signout'] = True
            st.session_state['show_admin_form'] = True
            st.success('Login Successful!')
        else:
            st.warning('Login Failed.Ensure you have entered the correct credentials ')
    except Exception as e:
        st.warning('Login Failed: {}'.format(str(e)))

# Function to submit HR requirements
def submit_requirements():
    st.session_state.disabled = True

# Function to close MySQL connection
def close_db_connection():
    db_connection.close()

# Function to submit HR requirements
def req(age_requirement, skills_requirement, gender_requirements, location_requirement, languages_requirement,
        EXPERIENCE_requirement, salary_requirement):
    user_email = st.session_state['useremail']
    try:
        age_req_str = f"{age_requirement[0]}-{age_requirement[1]}"
        skills_req_str = ",".join(skills_requirement).replace("-M", "").replace("-O", "") if skills_requirement else ""
        languages_req_str = ",".join(languages_requirement).replace("-M", "").replace("-O", "") if languages_requirement else ""
        salary_req_str = salary_requirement.replace("-M", "").replace("-O", "") if salary_requirement else ""
        exp_req_str = "".join(EXPERIENCE_requirement)

        insert_admin_query = """
            INSERT INTO hr_requirements (HR_EMAIL, AGE_REQ,GENDER_REQ,skills,LOCATION_REQ,languages,EXPERIENCE_REQ,SALARY_REQ)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(insert_admin_query, (
            user_email, age_req_str, gender_requirements, skills_req_str, location_requirement,
            languages_req_str, exp_req_str, salary_req_str
        ))
        db_connection.commit()
        #st.success("HR Requirements submitted successfully!")
    except Exception as e:
        st.error(f"Error inserting data: {e}")


# Run the app
def app():
    if not st.session_state["signedout"]:
        choice = st.selectbox('Login/Signup', ['Login', 'Sign up'])
        email = st.text_input('Email Address')
        password = st.text_input('Password', type='password')

        if choice == 'Sign up':
            username = st.text_input("Enter your unique username")
            signup_button = st.button('Create my account')
            if signup_button and username and password and email:
                try:
                    insert_query = "INSERT INTO hr_credentials (username, email, password) VALUES (%s, %s, %s)"
                    cursor.execute(insert_query, (username, email, password))
                    db_connection.commit()
                    st.success('Account created successfully!')
                    st.markdown('Please Login using your email and password')
                    st.balloons()
                except Exception as e:
                    display_signup_error_message(e)
            elif signup_button:
                st.warning('Enter all Details!')
        else:
            if st.checkbox("Login"):
                authenticate_user(email, password)
                

    if "reset_password_clicked" not in st.session_state:
        st.session_state.reset_password_clicked = False
    forgot_email = ""
    reset_password_clicked = False

    if st.button('Forgot Password?'):
        st.session_state.reset_password_clicked = True

    if st.session_state.reset_password_clicked:
        forgot_email = st.text_input("Enter your email for password reset")
        reset_password_clicked = st.button("RESET PASSWORD")




    if st.session_state.reset_password_clicked and reset_password_clicked:
        if forgot_email != "":
            reset_token = generate_reset_token()
            st.write(forgot_email)
            send_password_reset_email(forgot_email, reset_token)
            st.success("Password reset email sent. Check your email.")
            st.session_state.reset_password_clicked = False
        else:
            st.warning("Enter email")

    if st.session_state['show_admin_form']:
        form_submitted = st.session_state.get("form_submitted", False)

        with st.form(key="admin_requirements_form"):
            st.subheader("HR Requirements")
            age_requirement = st.slider("Age Requirement", min_value=18, max_value=65,
                                        value=st.session_state.get("age", (18, 65)), step=1)
            gender_requirement = st.selectbox("Gender Requirement", ["Male", "Female"], key="gender")
            skills_requirement = st.multiselect("Skills Requirement", ["C", "C++", "Java", "Python", "SQL", "HTML", "CSS",\
       "JavaScript", "React", "Angular", "Vue.js", "Node.js", "Django", "Flask", "RDBMS", "SQL queries",  "MongoDB",\
         "Cassandra", "TCP/IP", "HTTP", "HTTPS", "DNS", "Firewalls", "VPNs", "AWS", "Microsoft Azure", "Google Cloud Platform (GCP)",\
           "Cloud architecture and design", "Network security", "Penetration testing", "SSL/TLS", "CI/CD", "Docker", \
            "Kubernetes", "Jenkins", "Ansible", "Agile", "Scrum", "Kanban", "Waterfall", "Linux", "Windows", "macOS", \
              "Git", "SVN", "Tableau", "Power BI", "TensorFlow", "PyTorch", "NLP", "Computer Vision", "Deep learning",\
                 "Android", "iOS (Swift)", "OOP"],key="skills_multiselect")
            location_requirement = st.selectbox("Location Requirement", ["Bengaluru", "Hyderabad", "Pune","chennai","Kochi"],
                                                key="location_dropdown")
            languages_requirement = st.multiselect("Languages Requirement", [
        "Hindi", "Telugu", "English", "Spanish", "Chinese", "Arabic",
        "Bengali", "Portuguese", "Russian", "Japanese", "Punjabi", "Marathi",
        "Tamil", "Urdu", "Turkish", "Vietnamese", "French", "German",
        "Italian", "Korean", "Dutch", "Thai", "Indonesian", "Malay",
        "Greek", "Hebrew", "Swedish", "Polish", "Czech", "Hungarian",
        "Romanian", "Finnish", "Bulgarian", "Croatian", "Serbian", "Slovak",
        "Slovenian", "Norwegian", "Danish", "Icelandic", "Farsi", "Malayalam"],
                                                   key="languages_multiselect")
            EXPERIENCE_requirement = st.selectbox("experiences Requirement", ["fresher", "1-2", "2-3", "more than 3"],
                                                   key="exe_multiselect")
            salary_requirement = st.text_input("Salary Requirement", key="salary_text_input")

            if st.form_submit_button("SUBMIT HR REQUIREMENTS"):
                if salary_requirement.isdigit():
                    req(age_requirement, skills_requirement, gender_requirement,location_requirement,languages_requirement,EXPERIENCE_requirement,salary_requirement)
                    st.session_state.form_submitted = True
                else:
                    st.warning("Enter Salary in Numbers")


        if form_submitted:
            st.success("HR Requirements submitted successfully!")

        if st.button("Match requirements"):
            main(email)
            st.markdown("[Click for applicants](http://localhost:8503/)", unsafe_allow_html=True)

                

# Run the app
app()
# Close MySQL connection when Streamlit app is closed
close_db_connection()
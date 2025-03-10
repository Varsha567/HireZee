import streamlit as st
from project.database import Database
from project.authenticate import authenticater
from project.utils import utils
au = authenticater() 
ss = utils()

if ss.flag:
    import pandas as pd 
   
    # Set up MySQL connection
    
    db = Database() 
    if "form_submit" not in st.session_state:
        st.session_state.form_submit = False
    def callback():
        st.session_state.form_submit = True
    with st.form(key='my_form'):
      st.title('Registration Form')
      # creating a form
      #my_form=st.form(key='form-1')
      # creating input fields
      FName=st.text_input(label="First Name*")
      LName=st.text_input('Last Name')
      Age=st.slider('Age*',18,40)
      email=st.text_input('Email Id*')
      phone=st.text_input("Contact Number*")
      location=st.selectbox("Location", ["Bengaluru", "Hyderabad", "Pune","chennai","Kochi"])
      # creating radio button 
      gender=st.radio('Gender*',('Male','Female'))
      selected_skills = st.multiselect("Select Skills", ["C", "C++", "Java", "Python", "SQL", "HTML", "CSS",\
       "JavaScript", "React", "Angular", "Vue.js", "Node.js", "Django", "Flask", "RDBMS", "SQL queries",  "MongoDB",\
         "Cassandra", "TCP/IP", "HTTP", "HTTPS", "DNS", "Firewalls", "VPNs", "AWS", "Microsoft Azure", "Google Cloud Platform (GCP)",\
           "Cloud architecture and design", "Network security", "Penetration testing", "SSL/TLS", "CI/CD", "Docker", \
            "Kubernetes", "Jenkins", "Ansible", "Agile", "Scrum", "Kanban", "Waterfall", "Linux", "Windows", "macOS", \
              "Git", "SVN", "Tableau", "Power BI", "TensorFlow", "PyTorch", "NLP", "Computer Vision", "Deep learning",\
                 "Android", "iOS (Swift)", "OOP"])
    
      skills = ", ".join(selected_skills)
      salary=st.slider('Salary Expectations:',min_value=0.0, max_value=100000.0, step=1000.0)
      hobies = st.text_input("Hobbies")
      strengths = st.text_input("Strengths")
      #timing = st.selectbox("Which shift timing is suitable for you?*",["2 pm-11 pm/3pm-12 am","4 pm - 1 am","others"])
      objective = st.text_input("Objective")
      projects = st.text_input("Project (GitHub Link)")
      awards = st.text_input("Awards/Achievements")
      experience = st.number_input("Experience(in years):", value=0, min_value=0)
      #languages = st.text_input("Languages Known")
      selected_languages = st.multiselect("Languages Known", [
        "Hindi", "Telugu", "English", "Spanish", "Chinese", "Arabic",
        "Bengali", "Portuguese", "Russian", "Japanese", "Punjabi", "Marathi",
        "Tamil", "Urdu", "Turkish", "Vietnamese", "French", "German",
        "Italian", "Korean", "Dutch", "Thai", "Indonesian", "Malay",
        "Greek", "Hebrew", "Swedish", "Polish", "Czech", "Hungarian",
        "Romanian", "Finnish", "Bulgarian", "Croatian", "Serbian", "Slovak",
        "Slovenian", "Norwegian", "Danish", "Icelandic", "Farsi", "Malayalam"
      ])
      languages = ", ".join(selected_languages)
      company = st.text_input("List of companies worked")
      st.title("Education")
      # State variables for dynamic updates
      education_type = st.selectbox("Enter Educational Details",["B.E/B.TECH-CS/IT","B.E/B.TECH-OTHERS"\
        ,"BCA","BBA","MCA","MBA","Any Graduate - IT/CS","Any Masters - IT/CS","Others"])

      submit=st.form_submit_button('Submit')
      
      #if submit and au.is_valid_name(FName) and au.is_valid_name(LName) and Age and email and hobies and company and au.is_valid_languages_input(languages) and  experience and awards and strengths and objective and au.is_valid_github_link(projects) and au.is_valid_phone_number(phone) and gender and skills and education_type:
      if submit and FName and LName and email and strengths and awards and hobies and skills and projects:
          st.session_state['submit'] = True
          FName = FName.upper()
          LName = LName.upper()
          location = location.upper()
          company = company.upper()
          gender=gender.upper()  # Assuming location is a string field
          skills = skills.upper()
          education_type=education_type.upper()
          hobies = hobies.upper()
          languages = languages.upper()
          awards = awards.upper()
          strengths = strengths.upper()
          objective = objective.upper()
          if email == st.session_state['email']:
            if not au.does_user_exist(email):
                st.warning('This email is not registered. Please enter a valid email or sign up if you are a new user.')
            elif au.does_userdata_exist(email):
                st.warning('This email has already submitted a form. If you want to update the form, click on "Update Form".')
            elif not au.is_valid_name(FName):
                st.warning('Invalid input for First Name. Please enter a valid first name.')
            elif not au.is_valid_name(LName):
                st.warning('Invalid input for Last Name. Please enter a valid last name.')
            elif not au.is_valid_phone_number(phone):
                st.warning('Invalid input for Phone Number. Please enter a valid 10-digit phone number.')
            elif  au.is_valid_all(hobies):
                st.warning('Invalid input for Hobbies. Please enter valid hobbies separated by commas.')
            elif  au.is_valid_all(strengths):
                st.warning('Invalid input for Strengths. Please enter valid strengths separated by commas.')
            elif  au.is_valid_award(awards):
                st.warning('Invalid input for Awards. Please enter valid awards separated by commas.')
            elif  au.is_valid_company(company):
                st.warning('Invalid input for Company. Please enter valid companies separated by commas.')# &  , are exceptional
            elif  not au.is_valid_objective(objective):
                st.warning('Invalid input for Objective. Make sure it does not exceed the maximum length of 150 characters or contain invalid characters.')
            elif not au.is_valid_github_link(projects):
                st.warning('Invalid input for project. Please enter a URL in the form of "https://github.com".')

            else:
                    insert_query = "INSERT INTO user_data(FName, LName, Age, email, phone, location, gender, skills, salary, education_type, hobies, strengths, objective, projects, awards, experience, company, languages) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    db.execute_query(insert_query, (FName, LName, Age, email, phone, location, gender, skills, salary, education_type, hobies, strengths, objective, projects, awards, experience, company, languages))
                    db.commit()
                    st.success("Thank you! Your form has been successfully submitted.")
                    callback()
          else:
            st.warning("This email is not logged in . Use your login email please")     
                
      elif submit:
            st.warning("Please make sure to fill in all the required details before submiting the form!")

    
    
else:
   st.warning("Please log in first to access this page.")

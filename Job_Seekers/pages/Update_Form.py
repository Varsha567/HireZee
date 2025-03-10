import streamlit as st
from project.database import Database
from project.authenticate import authenticater
from project.utils import utils
au = authenticater()
ss = utils()  

# Set up MySQL connection

def update_form(email_update):
  with st.form(key='update_form'):
    query = "SELECT * FROM user_data WHERE email = %s"
    db.execute_query(query, (email_update,))
    current_data = db.fetch_one(query,(email_update,))
    location_options = ["BENGALURU", "HYDERABAD", "PUNE", "CHENNAI", "KOCHI"]
    location_index = location_options.index(current_data[5]) if current_data[5] in location_options else 0  
    gender_options = ['FEMALE','MALE']
    gender_index=gender_options.index(current_data[6]) if current_data[6] in gender_options else 0
    current_skills = current_data[7].split(', ') if current_data[7] else []
    #print("Current Skills from Database:", current_skills)

    # Replace with your actual skill options
    skills_options = ["C", "C++", "Java", "Python", "SQL", "HTML", "CSS", "JavaScript", "React", "Angular", "Vue.js", "Node.js", "Django", "Flask", "RDBMS", "SQL queries",  "MongoDB", "Cassandra", "TCP/IP", "HTTP", "HTTPS", "DNS", "Firewalls", "VPNs", "AWS", "Microsoft Azure", "Google Cloud Platform (GCP)", "Cloud architecture and design", "Network security", "Penetration testing", "SSL/TLS", "CI/CD", "Docker", "Kubernetes", "Jenkins", "Ansible", "Agile", "Scrum", "Kanban", "Waterfall", "Linux", "Windows", "macOS", "Git", "SVN", "Tableau", "Power BI", "TensorFlow", "PyTorch", "NLP", "Computer Vision", "Deep learning", "Android", "iOS (Swift)", "OOP"]
      # Ensure default values are part of skills_options
    skills_options_uppercase = [skill.upper() for skill in skills_options]
    default_skills = [skill for skill in current_skills if skill in skills_options_uppercase]
    #print("Default Skills After Filtering:", default_skills)
    education_options = ["B.E/B.TECH-CS/IT","B.E/B.TECH-OTHERS","BCA","BBA","MCA","MBA","Any Graduate - IT/CS","Any Masters - IT/CS","Others"]
    
    education_index= education_options.index(current_data[8]) if current_data[8] in location_options else 0
    current_languages = current_data[17].split(', ') if current_data[17] else []
    languages_options = [
        "Hindi", "Telugu", "English", "Spanish", "Chinese", "Arabic",
        "Bengali", "Portuguese", "Russian", "Japanese", "Punjabi", "Marathi",
        "Tamil", "Urdu", "Turkish", "Vietnamese", "French", "German",
        "Italian", "Korean", "Dutch", "Thai", "Indonesian", "Malay",
        "Greek", "Hebrew", "Swedish", "Polish", "Czech", "Hungarian",
        "Romanian", "Finnish", "Bulgarian", "Croatian", "Serbian", "Slovak",
        "Slovenian", "Norwegian", "Danish", "Icelandic", "Farsi", "Malayalam"
      ]
    languages_options_uppercase = [languages.upper() for languages in languages_options]
    default_languages = [languages for languages in current_languages if languages in languages_options_uppercase]
    new_data = {
                    'FName': st.text_input('FName', value=current_data[0]),
                    'LName': st.text_input('LName', value=current_data[1]),
                    'Age': st.slider('Age', min_value=18, max_value=40, value=current_data[2]),
                    'phone': st.text_input('New Phone', value=current_data[4]),
                    'location':st.selectbox("New Location", location_options, index=location_index),
                    'gender': st.radio('Gender', gender_options, index=gender_index),
                    'skills': st.multiselect('New Skills', skills_options_uppercase, default=default_skills),
                    'education_type': st.selectbox("Education level", education_options, index=education_index),
                    'salary': st.slider('Salary Expectations:',min_value=0.0, max_value=100000.0, step=1000.0, value=current_data[9]),
                    'hobies' : st.text_input('Hobies' , value=current_data[10]),
                    'strengths': st.text_input('Strengths',value=current_data[11]),
                    'objective':st.text_input('Objective',value=current_data[12]),
                    'projects':st.text_input('Projects',value=current_data[13]),
                    'awards' : st.text_input('Awards/Achievements',value=current_data[14]),
                    'experience':st.number_input('Experience',value=int(current_data[15]),min_value=0),
                    'company' : st.text_input('Companys Worked',value=current_data[16]),
                    'languages': st.multiselect('languages Known', languages_options_uppercase, default=default_languages)

                }
                    
    current_skills = ', '.join(current_skills)
    current_languages = ', '.join(current_languages)
    update=st.form_submit_button("Request Update")
    #if update and au.is_valid_phone_number(new_data['phone']) and au.is_valid_name(new_data['FName']) and au.is_valid_github_link(new_data['projects']) and au.is_valid_name(new_data['LName']) and au.is_valid_languages_input(new_data['languages']):
    
    if update:
      
          if not au.is_valid_name(new_data['FName']):
            st.warning('Invalid input for First Name. Please enter a valid first name.')
          elif not au.is_valid_name(new_data['LName']):
              st.warning('Invalid input for Last Name. Please enter a valid last name.')
          elif  au.is_valid_all(new_data['hobies']):
              st.warning('Invalid input for Hobbies. Please enter valid hobbies separated by commas.')
          elif  au.is_valid_all(new_data['strengths']):
              st.warning('Invalid input for Strengths. Please enter valid strengths separated by commas.')
          elif  au.is_valid_award(new_data['awards']):
              st.warning('Invalid input for Awards. Please enter valid awards separated by commas.')
          elif  au.is_valid_company(new_data['company']):
              st.warning('Invalid input for Company. Please enter valid companies separated by commas.')# &  , are exceptional
          
          elif not au.is_valid_phone_number(new_data['phone']):
              st.warning('Invalid input for Phone Number. Please enter a valid 10-digit phone number.')
          elif  not au.is_valid_objective(new_data['objective']):
              st.warning('Invalid input for Objective. Make sure it does not exceed the maximum length of 150 characters or contain invalid characters.')
          elif not au.is_valid_github_link(new_data['projects']):
              st.warning('Invalid input for project. Please enter a URL in the form of "https://example.com".')

      #print("something")
          else:
            updated_data = {
                      'FName': new_data['FName'].upper(),
                      'LName': new_data['LName'].upper(),
                      'Age': new_data['Age'],
                      'phone': new_data['phone'],
                      'location': new_data['location'].upper(),
                      'gender': new_data['gender'].upper(),
                      'skills': ', '.join(map(str, new_data['skills'])).upper(),
                      'education_type': new_data['education_type'].upper(),
                      'salary': new_data['salary'],
                      'hobies': new_data['hobies'].upper(),
                      'strengths':new_data['strengths'].upper(),
                      'objective': new_data['objective'].upper(),
                      'projects': new_data['projects'],
                      'awards': new_data['awards'].upper(),
                      'experience':new_data['experience'],
                      'company':new_data['company'].upper(),
                      'languages': ', '.join(map(str, new_data['languages'])).upper(),
                    }

            query = "UPDATE user_data SET FName = %s, LName = %s, Age = %s, phone = %s, location = %s, gender = %s,skills = %s, education_type = %s, salary = %s, hobies = %s,strengths = %s, objective = %s, projects = %s,awards = %s, experience = %s, company = %s, languages = %s WHERE email = %s"
            db.execute_query(query, (updated_data['FName'], updated_data['LName'], updated_data['Age'],updated_data['phone'], updated_data['location'], updated_data['gender'],updated_data['skills'], updated_data['education_type'], updated_data['salary'],updated_data['hobies'], updated_data['strengths'],updated_data['objective'], updated_data['projects'],updated_data['awards'],updated_data['experience'], updated_data['company'], updated_data['languages'],email_update))
            db.commit()
            st.success("Successfully updated your form")
if ss.flag:
  db = Database() 
  st.title('Update Form')
  email_update = st.text_input('Email Id* (to update existing record)')
  check_update = st.checkbox("check for update") 
      
  if check_update and not email_update:
    st.warning("Please enter your email before checking for an update.")
  elif check_update and email_update:
    if email_update == st.session_state['email']:
      if not au.does_user_exist(email_update):
        st.warning('This email is not registered. Please enter a valid email or sign up if you are a new user.')
      elif not au.does_userdata_exist(email_update):
        st.warning('No form found with this email. Please check the entered email or sign up if you are a new user.')
      else:
        st.success("You Can Update Your Form")
        update_form(email_update)
    else:
      st.warning("This email is not logged in . Use your login email please")

                  
else:
  st.warning("Please log in first to access this page.")
import os
import pandas as pd
import streamlit as st
import mysql.connector
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# Establish a connection to database
def est_connection(conn,cursor):
  conn = mysql.connector.connect(
  host=st.secrets["host"],
  user=st.secrets["user"],
  password=st.secrets["password"],
  database=st.secrets["database"])
  cursor = conn.cursor() # Create a cursor that interacts with db
  return conn,cursor
  
 # for executing query  
def execute_query(cursor,q_str):
  cursor.execute(q_str)
  return None  

#function for creating dataframes
def create_df(cursor):
  #Fetch data
  result = cursor.fetchall()
  #Convert the result to a DataFrame 
  df= pd.DataFrame(result, columns=[col[0] for col in cursor.description])
  return df



def data_extractor(cursor,ID): #extract data from DB
  stringq='SELECT * FROM USER_DATA WHERE EMAIL='+"'"+str(ID)+"'"
  execute_query(cursor,stringq)
       
  df_PDF= create_df(cursor)   # Convert the result to a DataFrame
  return df_PDF
      
          
def button_click(df):
  display_flag=0
  if 'redirect' not in st.session_state: #create redirect variable if it does not exist in session
   st.session_state['redirect'] = False  #initialise it to false

  display_flag=create_button(df)

   
  if display_flag:   # Check if  flag is true, then display success message
   st.success(f"PDF generated successfully!")
  return None  

def create_button(df):
  if st.button("Create Resume", key="create_resume"):
   create_resume_pdf(df)
   flag=1         
   return flag  
  

def create_file(df):
  
  text=str(df['FName'].iloc[0]).strip() # Remove leading/trailing spaces    
  pdf_filename = f"{text}_resume.pdf"
  folder_path = "downloads"  #location where the resumes will be downloaded
  if not os.path.exists(folder_path):
    os.makedirs(folder_path)
  path = os.path.join(folder_path, pdf_filename)
  c = canvas.Canvas(path, pagesize=letter)
  return c  

def create_resume_pdf(df):
    c=create_file(df)
    resume_content(c,df)
    return None

def resume_content(c, df):
    
    content_list = [("First name:","FName"),
    ("Last name:","LName"),                
    ("Age:", "Age"),
    ("Gender:", "gender"),
    ("Phone:", "phone"),
    ("Email:", "email"),
    ("Salary Expectation:", "salary"),
    ("Experience:", "experience"),
    ("Skills:", "skills"),
    ("Location Preferred:", "location"),
    ("List of Companies:", "company"),
    ("Languages:", "languages"),
    ("Objective","objective"),
    ("Education","education_type"),
    ("Projects","projects"),
    ("Hobbies","hobies"),
    ("Strengths","strengths")
    ]
    
    
    c.rect(25,25,560,750)
    start_y = 750  # Starting Y position for drawing

    for label, column_name in content_list:
        c.setFont("Times-Bold", 12)
        c.drawString(50, start_y, f"{label}")
        c.setFont("Times-Roman", 12)
        c.drawString(250, start_y, f"{df[column_name].iloc[0]}")
        start_y -= 20  # Move to the next line
  
    c.save()
    return None

def main(ID):
  try:
    conn=None
    cursor=None
       
    (conn,cursor)=est_connection(conn,cursor)  #establish connection to DB
    
    df_PDF=data_extractor(cursor,ID)
  
    
    #execute button functionality
    button_click(df_PDF)
        
  except PermissionError as p:
    err_str="""Error occurred: 
    The following might have occurred: \n
    1.Please close the opened resume file (if any) and try again. \n 
    2.Please grant the required permissions."""
    st.write(err_str)  # Handle PermissionError

  except OSError as o:
    
    st.write(f"OS error occurred: {o}") # Handle OSError
  
  except Exception as e:
    st.error(f"Error occurred: {e}") # other exceptions
        
  finally:
    #close the connection
    if conn:
      conn.close()
               
    if cursor:
      cursor.close()
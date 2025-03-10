import streamlit as st
import pandas as pd
import mysql.connector
conn=None
def est_connection(cursor):
  global conn
  conn = mysql.connector.connect(
  host=st.secrets["host"],
  user=st.secrets["user"],
  password=st.secrets["password"],
  database=st.secrets["database"])
  cursor = conn.cursor() # Create a cursor that interacts with db
  return cursor

def execute_query(cursor,q_str):
  
  cursor.execute(q_str)
  return None  
def match_multivalued_attr(df_HR,df_USER,attr_name):  #function to match multi valued mandatory attr
  list_var=[]
  tokens_HR =   extract_tokens(df_HR,attr_name)  
  for index, row in df_USER.iterrows():         # Iterating through rows using iterrows()
    
    text=row[attr_name]                 #extract  attr from row
    text=str(text)  
    tokens_USER = text.split(',')        
    flag=match_tokens(tokens_USER,tokens_HR) 
    if flag==1:
      list_var.append(str(row['email']))
  return list_var

#function for finding tuples matching both multivalued attr
def find_ids(cursor,lst_1,lst_2):
  unique_elements = set(lst_1 + lst_2)
  for item_1 in unique_elements:
    if item_1 in lst_1 and item_1 in lst_2:
      q_str="INSERT INTO  MATCHED_DATA VALUES("+"'"+ item_1+"'"+")"
      execute_query(cursor,q_str)
      conn.commit()
  return None     
       
#function for creating matched_data table
def create_table(cursor):
  q_str="DROP TABLE IF EXISTS MATCHED_DATA;"
  execute_query(cursor,q_str)  #logic to flush table for each match
  q_str='CREATE TABLE MATCHED_DATA(LOGIN_ID VARCHAR(50) PRIMARY KEY)'
  execute_query(cursor,q_str)  #create a table called matched_data
  return None 

#function for creating dataframes
def create_df(cursor):
  result = cursor.fetchall()  #Fetch data
  #Convert the result to a DataFrame 
  df= pd.DataFrame(result, columns=[col[0] for col in cursor.description])
  return df

def display_df(str,df):
  st.title(str)
  st.write(df)
  return None

def match_singlevalued_attr(df,attr):
  m_flag=0
  text=str(df[attr].iloc[0])
  if (text[len(text)-1]=='M'):
    m_flag=1
    text=text[:-2]
  return m_flag,text  

def extract_tokens(df,attr_name):
   if not  df.empty:
    text=df[attr_name].iloc[0]   #extract  attr from row
    text=str(text)  
    tokens = text.split(',')         # Splits based on periods
    return tokens

def match_tokens(t_U,t_H):
  if t_U:
    t_flag=0
    for item in t_H:      
      item=str(item)
      if item[len( item)-1]=='M':
        item=item[:-2]
        if item in t_U:
          t_flag=1
        else:
          t_flag=0
          break  
      else:
        t_flag=1  
    return t_flag
    
def query_for_singlevalued(df):    #function to  match single valued mandatory attr
  query=" SELECT * FROM USER_DATA WHERE"   #form the sql query which will be executed later
  q_f=0      
  (flag,text)=match_singlevalued_attr(df,'GENDER_REQ')  #match the gender
  if flag==1: 
    q_f=1
    query=query + " GENDER_REQ = '"+text+"' AND"

  (flag,text)=match_singlevalued_attr(df,'SALARY_REQ')   #match the salary 
  if flag==1:
    q_f=1
    query=query + " SALARY_REQ <= "+text+" AND"

        
  (flag,text)=match_singlevalued_attr(df,'LOCATION_REQ')  #match the location
  if flag==1:
    q_f=1
    query=query + " LOCATION_REQ = '"+text+"' AND"

       
  (flag,text)=match_singlevalued_attr(df,'EXPERIENCE_REQ')  #match the experience 
  if flag==1:
    q_f=1
    query=query + " EXPERIENCE_REQ >= "+text  

  if query.endswith('AND'):    #Check if the string ends with 'AND' and remove it if present
    query=query[:-3]  # Removing the last 3 characters

  if q_f==0:  #to remove "WHERE" in the query 
    query=query[:-5]

  query=query+";"

  #st.write(query)
  return query 

def match(ID):
  global conn 
  try:
    

    cursor=None
       
    (cursor)=est_connection(cursor)  #establish connection to DB
       
    execute_query(cursor,"SELECT * FROM HR_REQUIREMENTS WHERE HR_EMAIL="+"'"+str(ID)+"'")  # Execute  query with  placeholder for  ID
    
    df_HR = create_df(cursor) # Convert the result to a DataFrame 

    #display_df('HR req',df_HR)
    
    query=query_for_singlevalued(df_HR) #for elimination of tuples on basis of single valued mandatory attr

    execute_query(cursor,query) #Execute the filtering query 
    
    df_USER = create_df(cursor)    #Convert the result to a DataFrame 
       
    #display_df('Filtered data',df_USER)  #Display data 

    list_1=match_multivalued_attr(df_HR,df_USER,'languages') #match languages

    list_2=match_multivalued_attr(df_HR,df_USER,'skills')  #match skills

    create_table(cursor)  #create matched_data table
           
    find_ids(cursor,list_1,list_2)       

    execute_query(cursor,'SELECT * FROM MATCHED_DATA;')   #testing multiple attr match

    df_RESULT =create_df(cursor)   # Convert the result to a DataFrame

    #display_df('MATCHED DATA',df_RESULT)

    return None
        
    
  except Exception as e:   
    st.error("Error occurred:"+str(e))
        
  finally:
    if conn:      #close the connection
      conn.close()
    if cursor:    #close the cursor
      cursor.close() 
      #st.success("DB connection closed")

def main(id):

  match(id)
  return None      

  
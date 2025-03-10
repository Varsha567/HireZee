import mysql.connector
import streamlit as st
class Database:
    
    def __init__(self): #constructor no need to change arguments
        self.host = st.secrets["host"]
        self.user = st.secrets["user"]
        self.password = st.secrets["password"]
        self.database_name = st.secrets["database"]
        # Call the connect method during the initialization 
        self.connect()

    def is_connected(self):
        return self.connection.is_connected()
    def commit(self):
        self.connection.commit()
    def connect(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database_name
        )
        self.cursor = self.connection.cursor()

    def close_connection(self):
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            #print("Database connection closed.")
# Instantiating the Database class with default or specified connection details
    def create_login_tables(self):
        create_table_query = """
            CREATE TABLE IF NOT EXISTS user_credentials (
                username VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL PRIMARY KEY,
                password VARCHAR(255) NOT NULL
                
            )
        """
        create_table_query1 = """
            CREATE TABLE IF NOT EXISTS password_reset (
                email VARCHAR(255) NOT NULL PRIMARY KEY,
                reset_token VARCHAR(255) NOT NULL
            )
        """
        self.execute_query(create_table_query)
        self.execute_query(create_table_query1)
    def execute_query(self, query, values=None):
        try:
            self.connect()
            if values:
                self.cursor.execute(query, values)
            else:
                self.cursor.execute(query)
        except Exception as e:
            print(f"Error executing query(here): {e}")
        
    '''def execute_query(self, query, values=None, fetch_results=False):
            try:
                self.connect()
                if values:
                    self.cursor.execute(query, values)
                else:
                    self.cursor.execute(query)

                if fetch_results:
                    results = self.cursor.fetchall()
                    return results
                else:
                    self.connection.commit()  # For non-SELECT queries, commit the changes

            except Exception as e:
                print(f"Error executing query: {e}")'''
    def fetch_one(self, query, values=None):
        result = None
        try:
            self.connect()
            if values:
                self.cursor.execute(query, values)
            else:
                self.cursor.execute(query)
            result = self.cursor.fetchone()
            return result

        except Exception as e:
            print(f"Error fetching data: {e}")
    def fetch_all(self, query, values=None):
        results = None
        try:
            self.connect()
            if values:
                self.cursor.execute(query, values)
            else:
                self.cursor.execute(query)
            results = self.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching data: {e}")
        
        return results
    def create_form_tables(self):
         create_table_query = """
    CREATE TABLE IF NOT EXISTS user_data (
        FName VARCHAR(255) NOT NULL,
        LName VARCHAR(255) NOT NULL,
        Age INTEGER(3) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE, 
        phone VARCHAR(15) UNIQUE NOT NULL,
        location VARCHAR(255) NOT NULL DEFAULT 'NA',
        gender VARCHAR(10) NOT NULL,
        skills VARCHAR(255) NOT NULL,
        education_type VARCHAR(255) NOT NULL,
        salary DOUBLE NOT NULL DEFAULT 0,
        hobies VARCHAR(255) NOT NULL,
        strengths VARCHAR(255) NOT NULL,
        objective VARCHAR(255) NOT NULL DEFAULT 'NA',
        projects VARCHAR(255) NOT NULL DEFAULT 'NA',
        awards VARCHAR(255) NOT NULL,
        experience VARCHAR(255) NOT NULL,
        company VARCHAR(255) NOT NULL,
        languages VARCHAR(255) NOT NULL,
        FOREIGN KEY(email) REFERENCES user_credentials(email)
        )
        """
         self.execute_query(create_table_query)

   
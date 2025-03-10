import streamlit as st
import mysql.connector
import pandas as pd
from streamlit_lottie import st_lottie
import json


def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def set_page_configuration():
    st.set_page_config(page_title="hirezee", page_icon=":computer:", layout="wide")

class Result_not_found(Exception):
   "raised when data in matched table is null"
   pass

def set_page_background_opacity(opacity=0.2):
    page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"]{{
    background-image:url(https://www.wallpapertip.com/wmimgs/83-838296_web-designer-professional-website-background-images.jpg);
    background-size:cover;
    margin: 0;
    padding: 0;
    height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    background-color: rgba(255, 255, 255, {opacity});
    }}
    [data-testid="stHeader"]{{
    background-color:rgba(0,0,0,0);
    }}
    [data-testid="element-container"]{{
    background-color:rgba(0,0,0,0);
    }}
    [data-testid="stTableStyledTable"]{{
    border-collapse:collapse;
    text-align:left;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

def display_candidates_list():
    styling_title = """
        <h1 style='
        text-align :center;
        font-size:2.5em;'>
        CANDIDATES LIST
        </h1>
        """
    st.markdown(styling_title, unsafe_allow_html=True)

    with open("nancy/designing.css") as source_des:
        st.markdown(f"<style>{source_des.read()}</style>", unsafe_allow_html=True)
    st.markdown("---")

    try:
        db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': '1234',
            'database': 'master_db',
        }

        con = mysql.connector.connect(**db_config)
        cursor = con.cursor()

        try:
            cursor.execute("select *from user_data where email IN (select email from matched_data)")
            matching_rows = cursor.fetchall()

            if not matching_rows:
                raise Result_not_found

            set_page_background_opacity()

            df = pd.DataFrame(matching_rows, columns=cursor.column_names)
            df = df.drop(columns=['index'], axis=1, errors='ignore')

            table_style = df.style \
                .set_table_styles([
                    {'selector': 'thead', 'props': [('background-color', 'lightblue')]},
                    {'selector': 'td, th', 'props': [('text-align', 'center'), ('color', 'white')]}
                ]) \
                .set_table_styles([{
                    'selector': 'th',  # for the header
                    'props': [('color', 'white')]
                }])
            st.table(table_style)
            st.write("---")

        except Result_not_found:
            st.write("##")
            st_lottie(
                load_lottiefile("nancy/loading.json"),
                speed=1,
                reverse=False,
                loop=True,
                quality="low",
                height=300,
                width=None,
                key=None,
            )
            message = """
            <h3 style='
            text-align :center;
            font-size:1.5em;'>
            NO ONE MATCHES YOUR REQUIREMENTS
            </h3>
            """
            st.markdown(message, unsafe_allow_html=True)

    except Exception as e:
        st.write("Unable to load the database")

    finally:
        cursor.close()
        con.close()

if __name__ == "__main__":
    set_page_configuration()
    display_candidates_list()

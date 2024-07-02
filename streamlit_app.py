import streamlit as st
#from dotenv import load_dotenv
import os
import psycopg2 as psql
import requests

#load_dotenv()

#KEY = os.getenv('STEAM_API_KEY')
KEY=st.secrets['key']

#User = os.getenv('User')
User=st.secrets['User']
    
P#assword = os.getenv('Password')
Password=st.secrets['Password']

#Host = os.getenv('Host')
Host=st.secrets['Host']

#Database = os.getenv('Database')
Database=st.secrets['Database']

#Port = os.getenv('Port')
Port=st.secrets['Port']


conn = psql.connect(
    database=Database,
    user=User,
    host=Host,
    password=Password,
    port=Port
)

cur = conn.cursor()

# Streamlit app
st.title("Steam Profile Tracker")

with st.sidebar:
    user_name = st.text_input("Search for a user", placeholder="John Doe")
    st.write("Recently Viewed Users")

if user_name:
    # Query the database for the entered user name
    sql = """
    SELECT user_name, avatar_url, game_name1, game_img1, game_url1, playtime1,
           game_name2, game_img2, game_url2, playtime2,
           game_name3, game_img3, game_url3, playtime3
    FROM student.de10ATCapstoneProject
    WHERE user_name = %s
    """
    cur.execute(sql, (user_name,))
    rows = cur.fetchall()

    if rows:
        user_data = rows[0]
        
        # Display user name and avatar URL in the User header
        st.header("User")
        st.write(f"User Name: {user_data[0]}")
        st.image(user_data[1], width=100, caption=user_data[0])
        
        # Display the 3 games under the profile in a row under the Game Library
        st.header("Game Library")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader(user_data[2])
            st.image(user_data[3], width=150)
            st.write(f"[Link to game]({user_data[4]})")
            st.write(f"Playtime: {user_data[5]} hours")

        with col2:
            st.subheader(user_data[6])
            st.image(user_data[7], width=150)
            st.write(f"[Link to game]({user_data[8]})")
            st.write(f"Playtime: {user_data[9]} hours")

        with col3:
            st.subheader(user_data[10])
            st.image(user_data[11], width=150)
            st.write(f"[Link to game]({user_data[12]})")
            st.write(f"Playtime: {user_data[13]} hours")
    else:
        st.write("User not found.")

cur.close()
conn.close()

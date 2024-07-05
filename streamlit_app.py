import streamlit as st
from dotenv import load_dotenv
import os
import psycopg2 as psql

load_dotenv()

KEY = os.getenv('STEAM_API_KEY')
User = os.getenv('User')
Password = os.getenv('Password')
Host = os.getenv('Host')
Database = os.getenv('Database')
Port = os.getenv('Port')

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

# Sidebar user input
with st.sidebar:
    user_name = st.text_input("Search for a user", placeholder="John Doe")
    st.write("Recently Viewed Users")

    # Fetch the list of users from the database
    cur.execute("SELECT DISTINCT user_name FROM student.de10ATCapstoneProject")
    users = cur.fetchall()
    user_list = [user[0] for user in users]

    selected_user = st.selectbox("Select a user", user_list)

# Determine the user to search
search_user = user_name if user_name else selected_user

if search_user:
    # Query the database for the selected user name
    sql = """
    SELECT user_name, avatar_url, game_name1, game_img1, game_url1, playtime1,
           game_name2, game_img2, game_url2, playtime2,
           game_name3, game_img3, game_url3, playtime3
    FROM student.de10ATCapstoneProject
    WHERE user_name = %s
    """
    cur.execute(sql, (search_user,))
    rows = cur.fetchall()

    if rows:
        user_data = rows[0]
        
        # Display user name and avatar URL in the User header
        st.header("User")
        st.write(f"User Name: {user_data[0]}")
        st.image(user_data[1], width=100, caption=user_data[0])
        
        # Display the 3 games under the profile in rows under the Game Library
        st.header("Game Library")

        # Game 1
        st.subheader(user_data[2])
        st.image(user_data[3], width=150)
        st.write(f"[Link to game]({user_data[4]})")
        st.write(f"Playtime: {user_data[5]} hours")
        
        # Game 2
        st.subheader(user_data[6])
        st.image(user_data[7], width=150)
        st.write(f"[Link to game]({user_data[8]})")
        st.write(f"Playtime: {user_data[9]} hours")
        
        # Game 3
        st.subheader(user_data[10])
        st.image(user_data[11], width=150)
        st.write(f"[Link to game]({user_data[12]})")
        st.write(f"Playtime: {user_data[13]} hours")
    else:
        st.write("User not found.")

cur.close()
conn.close()

st.header("Game Recommendations")
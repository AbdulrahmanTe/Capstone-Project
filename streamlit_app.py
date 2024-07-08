import streamlit as st
from dotenv import load_dotenv
import os
import psycopg2 as psql
from steam_web_api import Steam
import numpy as np

load_dotenv()

KEY = os.getenv('STEAM_API_KEY')
User = os.getenv('User')
Password = os.getenv('Password')
Host = os.getenv('Host')
Database = os.getenv('Database')
Port = os.getenv('Port')

steam = Steam(KEY)

def getUserDetails(userName):
    try:
        userDetails = steam.users.search_user(userName)
        if userDetails == 'No match':
            print("There is no user with this name")
            return None
        else:
            steamId = userDetails['player']['steamid']
            gamesDetails = steam.users.get_owned_games(steamId)
            sorted_games = sorted(gamesDetails['games'], key=lambda x: x['playtime_forever'], reverse=True)
            gamesList = []
            for game in sorted_games[:5]:
                game_info = steam.apps.search_games(game['name'])
                if game_info['apps']:
                    game_data = game_info['apps'][0]
                    game_details = {
                        'gamesImg': game_data['img'],
                        'gameLink': game_data['link'],
                        'gameName': game['name'],
                        'Playtime': game['playtime_forever']
                    }
                    gamesList.append(game_details)

            return (userDetails['player']['personaname'], userDetails['player']['steamid'], userDetails['player']['avatarfull'],
                    gamesList[0]['gameName'], gamesList[0]['gamesImg'], gamesList[0]['gameLink'], gamesList[0]['Playtime'],
                    gamesList[1]['gameName'], gamesList[1]['gamesImg'], gamesList[1]['gameLink'], gamesList[1]['Playtime'],
                    gamesList[2]['gameName'], gamesList[2]['gamesImg'], gamesList[2]['gameLink'], gamesList[2]['Playtime'])
    except AttributeError:
        return 'Error', np.NAN, np.NAN, np.NAN, np.NAN, np.NAN, np.NAN, np.NAN, np.NAN, np.NAN, np.NAN, np.NAN, np.NAN, np.NAN, np.NAN

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
        st.write(f"Playtime: {round(user_data[5]/60)} Hours")
        
        # Game 2
        st.subheader(user_data[6])
        st.image(user_data[7], width=150)
        st.write(f"[Link to game]({user_data[8]})")
        st.write(f"Playtime: {round(user_data[9]/60)} Hours")
        
        # Game 3
        st.subheader(user_data[10])
        st.image(user_data[11], width=150)
        st.write(f"[Link to game]({user_data[12]})")
        st.write(f"Playtime: {round(user_data[13]/60)} Hours")
    else:
        # If user is not found in the database, fetch the details and insert them
        st.write("User not found in the database. Fetching details...")
        user_details = getUserDetails(search_user)
        
        if user_details:
            st.write("User details fetched successfully.")
            user_data = user_details
            # Insert user details into the database
            insert_sql = """
            INSERT INTO student.de10ATCapstoneProject (
                user_name, steam_id, avatar_url, game_name1, game_img1, game_url1, playtime1,
                game_name2, game_img2, game_url2, playtime2,
                game_name3, game_img3, game_url3, playtime3
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cur.execute(insert_sql, user_data)
            conn.commit()
            
            # Display user name and avatar URL in the User header
            st.header("User")
            st.write(f"User Name: {user_data[0]}")
            st.image(user_data[2], width=100, caption=user_data[0])
            
            # Display the 3 games under the profile in rows under the Game Library
            st.header("Game Library")

            # Game 1
            st.subheader(user_data[3])
            st.image(user_data[4], width=150)
            st.write(f"[Link to game]({user_data[5]})")
            st.write(f"Playtime: {round(user_data[6]/60)} Hours")
            
            # Game 2
            st.subheader(user_data[7])
            st.image(user_data[8], width=150)
            st.write(f"[Link to game]({user_data[9]})")
            st.write(f"Playtime: {round(user_data[10]/60)} Hours")
            
            # Game 3
            st.subheader(user_data[11])
            st.image(user_data[12], width=150)
            st.write(f"[Link to game]({user_data[13]})")
            st.write(f"Playtime: {round(user_data[14]/60)} Hours")
        else:
            st.write("There is no account found with that Username.")

cur.close()
conn.close()

st.header("Game Recommendations")

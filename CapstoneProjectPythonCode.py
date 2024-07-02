from dotenv import load_dotenv
import os
import psycopg2 as psql
import pprint
import numpy as np
import requests
from pprint import pprint
from steam_web_api import Steam
import pandas as pd

load_dotenv()

KEY=os.getenv('STEAM_API_KEY')
User=os.getenv('User')
Password=os.getenv('Password')
Host=os.getenv('Host')
Database=os.getenv('Database')
Port=os.getenv('Port')
steam = Steam(KEY)

def getUserDetails(userName):
    try:
        userDetails=steam.users.search_user(userName)
        if userDetails== 'No match':
            print("There is no user with this name")
        else:
            steamId=userDetails['player']['steamid']
            ##print(steamId)
            gamesDetails = steam.users.get_owned_games(steamId)
            ##pprint(gamesDetails)
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


            return userDetails['player']['personaname'], userDetails['player']['steamid'],userDetails['player']['avatarfull'],gamesList[0]['gameName'],gamesList[0]['gamesImg'],gamesList[0]['gameLink'],gamesList[0]['Playtime'],gamesList[1]['gameName'],gamesList[1]['gamesImg'],gamesList[1]['gameLink'],gamesList[1]['Playtime'],gamesList[2]['gameName'],gamesList[2]['gamesImg'],gamesList[2]['gameLink'],gamesList[2]['Playtime']
    except AttributeError:
        return 'Error', np.NAN, np.NAN, np.NAN, np.NAN, np.NAN, np.NAN, np.NAN , np.NAN, np.NAN, np.NAN, np.NAN , np.NAN, np.NAN, np.NAN, np.NAN 
    

conn = psql.connect(
    database=Database,
    user=User,
    host=Host,
    password=Password,
    port=Port
)

cur = conn.cursor()


cur.execute("SELECT user_name FROM student.de10ATCapstoneProject")
user_names = cur.fetchall()

for user_name_tuple in user_names:
    user_name = user_name_tuple[0]
    userData = getUserDetails(user_name)
    if userData:
        sql = """
        UPDATE student.de10ATCapstoneProject SET steam_id = %s, avatar_url = %s, game_name1 = %s, game_img1 = %s, game_url1 = %s, playtime1 = %s,game_name2 = %s, game_img2 = %s, game_url2 = %s, playtime2 = %s,game_name3 = %s, game_img3 = %s, game_url3 = %s, playtime3 = %s
        WHERE user_name = %s
        """

        
        cur.execute(sql, (
            userData[1], userData[2], userData[3], userData[4], userData[5], userData[6],
            userData[7], userData[8], userData[9], userData[10], userData[11], userData[12],
            userData[13], userData[14], userData[0]
        ))

        conn.commit()

cur.close()
conn.close()
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

cur=conn.cursor()
Test=['SuperAbz','shadeisalive','Deejayah']
for x in Test:
    userData=getUserDetails(x)

    sql = """
    INSERT INTO student.de10ATCapstoneProject (user_name, steam_id, avatar_url, game_name1,game_img1,game_url1,playtime1,game_name2, game_img2, game_url2, playtime2,game_name3, game_img3, game_url3, playtime3)
    VALUES (%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s)
    """

    # Execute the query with parameters
    cur.execute(sql, (
        userData[0],
        userData[1],
        userData[2],
        userData[3],
        userData[4],
        userData[5],
        userData[6],
        userData[7],
        userData[8],
        userData[9],
        userData[10],
        userData[11],
        userData[12],
        userData[13],
        userData[14]
    ))

    conn.commit()


cur.close()
conn.close()
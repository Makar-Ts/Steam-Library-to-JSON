from xmlrpc.client import boolean
import requests
import configparser
import time
import json
import sys
import os

start_time = time.time()

config = configparser.ConfigParser()
config.read("local/config.ini") # load config

games = []

request = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={
                            config["Secure"]["WebAPIToken"]
                        }&steamid={
                            config["Secure"]["AccountSteamID"]
                        }&format=json" # get all games from Steam library

response = requests.get(request, timeout=200)
if response.status_code == 200: # 200 = success
    data = response.json()
    for game in data["response"]["games"]:
        print(f"Parcing game: {game['appid']}")
        if game['playtime_forever'] == 0 and config["Main"]["SkipGamesWithZeroPlaytime"] == "1": # if game never played
            print("Playtime is 0, continue...")
            continue
        
        request = f"https://store.steampowered.com/api/appdetails?appids={game['appid']}" # get details about the game
        response = requests.get(request, timeout=200) 
        
        if response.status_code != 200: # if response incorrect
            print("Response code is " + response.status_code + ", continue...")
            continue
        
        data = response.json()
        
        if not data[str(game['appid'])]['success']: 
            print("Responce status is not success, continue...")
            continue
        
        games.append({
            "appid":        game['appid'],
            "name":         data[str(game['appid'])]['data']['name'],
            "playtime":     round(game['playtime_forever']/60, 3), # minutes to hours
            "release_date": data[str(game['appid'])]['data']['release_date']["date"] if not data[str(game['appid'])]['data']['release_date']["coming_soon"] else None,
            "developers":   ", ".join(data[str(game['appid'])]['data']['developers']),
            "categories":   ", ".join(map(lambda x: x["description"], data[str(game['appid'])]['data']['categories'])) if 'categories' in data[str(game['appid'])]['data'] else None,
            "genres":       ", ".join(map(lambda x: x["description"], data[str(game['appid'])]['data']['genres']))
        })
else:
    print("Steam response failed, check your config")
    sys.exit(1)


with open(os.path.join(sys.path[0], 'output.json'), 'w') as f: # write output
    f.write(json.dumps(games))

print(f"Time taken: {time.time()-start_time}")
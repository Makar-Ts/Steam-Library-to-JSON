import requests
import configparser
import time
import json
import sys
import os

start_time = time.time()

config = configparser.ConfigParser()
config.read("local/config.ini")

games = []

request = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={
                            config["Secure"]["WebAPIToken"]
                        }&steamid={
                            config["Secure"]["AccountSteamID"]
                        }&format=json"

response = requests.get(request, timeout=200)
if response.status_code == 200:
    data = response.json()
    for game in data["response"]["games"]:
        print(f"Parcing game: {game['appid']}")
        if game['playtime_forever'] == 0:
            print("Playtime is 0, continue...")
            continue
        
        request = f"https://store.steampowered.com/api/appdetails?appids={game['appid']}"
        response = requests.get(request, timeout=200) 
        
        if response.status_code != 200: 
            print("Response code is " + response.status_code + ", continue...")
            continue
        
        data = response.json()
        
        if not data[str(game['appid'])]['success']:
            print("Responce status is not success, continue...")
            continue
        
        games.append({
            "appid":        game['appid'],
            "name":         data[str(game['appid'])]['data']['name'],
            "playtime":     round(game['playtime_forever']/60, 3),
            "release_date": data[str(game['appid'])]['data']['release_date']["date"] if not data[str(game['appid'])]['data']['release_date']["coming_soon"] else None,
            "developers":   ", ".join(data[str(game['appid'])]['data']['developers']),
            "categories":   ", ".join(map(lambda x: x["description"], data[str(game['appid'])]['data']['categories'])) if 'categories' in data[str(game['appid'])]['data'] else None,
            "genres":       ", ".join(map(lambda x: x["description"], data[str(game['appid'])]['data']['genres']))
        })
else:
    print("Steam response failed, check your config")
    sys.exit(1)


with open(os.path.join(sys.path[0], 'output.json'), 'w') as f:
    f.write(json.dumps(games))

print(f"Time taken: {time.time()-start_time}")
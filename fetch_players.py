import requests
import json
import os

url = 'https://api.xfl.com/scoring/v3.30/players'

params = {
    'access_token':''

filepath = "raw_data/player_data.json"
try:
    r = requests.get(url, params=params)
    r.raise_for_status()
    players_json = json.dumps(r.text, indent=4, sort_keys=True)
    try:
        if not os.path.exists(filepath):
            with open(filepath, "w+") as players_file:
                players_file.write(players_json)
        print(f"{filepath} generated!")
    except IOError as err:
        print(err)
except requests.exceptions.HTTPError as err:
    raise SystemExit(err)

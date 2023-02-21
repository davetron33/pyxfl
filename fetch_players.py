import requests
import json
import pandas as pd

url = 'https://api.xfl.com/scoring/v3.30/players'

params = {
    'access_token':'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJuYW1laWQiOiI2M2YyNzM4ZTkyNWEwZjViMjFhMWExNjgiLCJ1bmlxdWVfbmFtZSI6InhmbHdlYnVzZXIiLCJyb2xlIjpbIk5ITFBST0QiLCJQVUJMSUMiLCJYRkxVU0VSIiwiWEZMREVWIiwiWEZMUFJPRCIsIlNDT1JJTkdfUFVTSCIsIlNDT1JJTkdfUkVTVCJdLCJuYmYiOjE2NzY5MjY0ODgsImV4cCI6MTY3NzE4NTY4OCwiaWF0IjoxNjc2OTI2NDg4fQ.iOj39tXxS4USA2kpj6PthA5sDx7tc0tWiJMbGJtLaic89BahnoJpVvIXybePMksy02zh0n-CrHRJX1XHiQpDAg'
}
filepath = "raw_data/player_data.json"

'''
TODO: Create fetch module, de-duplicate fetch_players and fetch_games. Refactor both into cli parameters.
'''
try:
    r = requests.get(url, params=params)
    r.raise_for_status()
    players_json = json.dumps(r.text, indent=4, sort_keys=True)
except requests.exceptions.HTTPError as err:
    raise SystemExit(err)

players = json.loads(players_json)
player_data = pd.read_json(players)
player_data.to_csv("processed_data/players.csv")
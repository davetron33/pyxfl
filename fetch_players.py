import requests
import json
import pandas as pd

url = 'https://api.xfl.com/scoring/v3.30/players'
params = {
    'scope':'Season',
    'access_token':'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJuYW1laWQiOiI2M2YyNzM4ZTkyNWEwZjViMjFhMWExNjgiLCJ1bmlxdWVfbmFtZSI6InhmbHdlYnVzZXIiLCJyb2xlIjpbIlhGTFBST0QiLCJQVUJMSUMiLCJYRkxVU0VSIiwiWEZMREVWIiwiWEZMUFJPRCIsIlNDT1JJTkdfUFVTSCIsIlNDT1JJTkdfUkVTVCIsIlhGTFRFU1QiXSwibmJmIjoxNjc3NDk1NjUyLCJleHAiOjE2Nzc3NTQ4NTIsImlhdCI6MTY3NzQ5NTY1Mn0.DZ-W5sH-o--wt2k8YfNEqmeqMV9FymuvM9jZZrkIAnjbnMEXfWSRfjxfT6faikQESMWRh758NLUuTOu5_IsYaQ'
}

try:
    r = requests.get(url, params=params)
    r.raise_for_status()
    stat_response = json.dumps(r.text, indent=4, sort_keys=True)
except requests.exceptions.HTTPError as err:
    raise SystemExit(err)

response = json.loads(stat_response)
processed_data = pd.read_json(response)

processed_data.to_csv("processed_data/player_stats.csv")


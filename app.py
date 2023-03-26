import pandas as pd
import requests
import json
import os

token = os.getenv('access_token')
players_endpoint = 'https://api.xfl.com/scoring/v3.30/players'
teams_endpoint = 'https://api.xfl.com/scoring/v3.30/teams'
stats_endpoint = 'https://api.xfl.com/scoring/v3.30/playerstats'


class xfl:

    global api_params
    api_params = {
        'access_token': f'{token}'
        }

    def __init__(self, token):
        self.url = players_endpoint
        self.token = token
        pass

    def list_players(self):
        url = self.url

        try:
            r = requests.get(url, params=api_params)
            r.raise_for_status()

            api_response = json.dumps(r.text, indent=4, sort_keys=True)
            response = json.loads(api_response)

            global players
            players = pd.read_json(response)
            players["Player"] = players['FirstName'].astype(str) + " " + players['LastName']

            mutate_player_frame = [
                    'FirstName',
                    'LastName',
                    'NAbbrev',
                    'PositionLongName',
                    'DOB',
                    'POB',
                    'Hometown',
                    'Country',
                    'Headshot',
                    'Initials',
                    'TrackingId',
                    'Affiliate',
                    'CloudHeadshotURL',
                    'SquadId'
                    ]

            [players.pop(col) for col in mutate_player_frame]
            cols = list(players.columns)
            cols.reverse()

            players.iloc[:, []]
            print(players[cols])
            pass
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

    def get_stats_combined(self, scope=""):
        url = stats_endpoint
        self.scope = scope

        scope = {'scope': f'{scope}'}
        api_params.update(scope)

        try:
            r = requests.get(url, params=api_params)
            r.raise_for_status()

            api_response = json.dumps(r.text, indent=4, sort_keys=True)
            response = json.loads(api_response)

            global player_stats
            player_stats = pd.read_json(response).fillna(0)

            print(player_stats)
            pass
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        pass

    def get_teams(self):
        url = teams_endpoint

        try:
            r = requests.get(url, params=api_params)
            r.raise_for_status()

            api_response = json.dumps(r.text, indent=4, sort_keys=True)
            response = json.loads(api_response)

            global player_stats
            teams = pd.read_json(response).fillna(0)

            print(teams)
            pass
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        pass

        pass


# create a new instance of the xfl-api object
xfl = xfl(token)

# list all players in the XFL (returns as a pandas data frame)
players = xfl.list_players()
print(players)

# list all teams
teams = xfl.get_teams()
print(teams)

# get combined season stats stats
player_stats = xfl.get_stats_combined("season")
print(player_stats)

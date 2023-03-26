import pandas as pd
import requests
import argparse
import json
import os

# initialize a few happy variables. variables are cool.
token = os.getenv('access_token')
players_endpoint = 'https://api.xfl.com/scoring/v3.30/players'
teams_endpoint = 'https://api.xfl.com/scoring/v3.30/teams'
stats_endpoint = 'https://api.xfl.com/scoring/v3.30/playerstats'

# class xfl is the powerhouse of the cell.


class xfl:

    '''
    api_params is a global variable because it is well traveled.
    and by well traveled I mean we will reuse this dictionary later on
    and add keys to it.
    '''
    global api_params
    api_params = {
        'access_token': f'{token}'
        }

    def __init__(self, token):
        self.url = players_endpoint
        self.token = token
        pass

    # get_players returns a dataframe of all players in the xfl
    # regardless of injury status. The primary key is 'OfficialId'
    def get_players(self):
        url = self.url

        try:
            # hello api? It's me, Margaret.
            r = requests.get(url, params=api_params)
            r.raise_for_status()

            api_response = json.dumps(r.text, indent=4, sort_keys=True)
            response = json.loads(api_response)

            global players
            players = pd.read_json(response)

            # concatenating player first and last name.
            players["Player"] = players['FirstName'].astype(str) + " " + players['LastName']

            # removes extraneous columns from the player data frame.
            # to add them back, give them some time to say goodbye to their
            # friends, and then remove them from the list.
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

            # bye felicia.
            [players.pop(col) for col in mutate_player_frame]

            # reordering columns so player name is first.
            cols = list(players.columns)
            cols.reverse()
            players = players[cols]

            # tada! we have a nice dataframe full of players.
            print(players)
            pass
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

    # get_stats_combined retrieves all overall counting stats.
    # OfficialId is the primary key, and is associated with the same
    # column in get_players() method.
    def get_stats_combined(self, scope=""):
        url = stats_endpoint
        self.scope = scope

        # Told you we'd be updating this dictionary later.
        scope = {'scope': f'{scope}'}
        api_params.update(scope)
        try:
            r = requests.get(url, params=api_params)
            r.raise_for_status()

            api_response = json.dumps(r.text, indent=4, sort_keys=True)
            response = json.loads(api_response)

            global player_stats
            player_stats = pd.read_json(response).fillna(0)

            print(type(player_stats))
            pass
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        pass

    # get_teams returns a list of all teams.
    # as usual, OfficialId is the primary key.
    def get_teams(self):
        url = teams_endpoint

        try:
            r = requests.get(url, params=api_params)
            r.raise_for_status()

            api_response = json.dumps(r.text, indent=4, sort_keys=True)
            response = json.loads(api_response)

            global teams
            teams = pd.read_json(response).fillna(0)

            print(teams)
            pass
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        pass


# x gon' give it to ya.
x = xfl(token)

players = x.get_players()
print(players)

teams = x.get_teams()
print(teams)

player_stats = x.get_stats_combined("season")
print(player_stats)

import pandas as pd
from sqlalchemy import create_engine
import requests
import json
import os

# initialize sqlite3 connection

# initialize a few happy variables. variables are cool.
token = os.getenv('access_token')

psql_host = os.getenv('psql_host')
psql_user = os.getenv('psql_user')
psql_pass = os.getenv('psql_pass')
psql_data = 'pyxfl'

engine = create_engine(f'postgresql://{psql_user}:{psql_pass}@{psql_host}/{psql_data}')

# TODO: Instead use a list for the different endpoints and one url for the base path of the api.
players_endpoint    =   'https://api.xfl.com/scoring/v3.30/players'
teams_endpoint      =   'https://api.xfl.com/scoring/v3.30/teams'
stats_endpoint      =   'https://api.xfl.com/scoring/v3.30/playerstats'
games_list_endpoint =   'https://api.xfl.com/scoring/v3.30/games'

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

    def get_stuff(self):
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
            players = pd.read_json(response).set_index('OfficialId')

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

            # tada! we have a nice dataframe full of player
            return players
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)


# TODO: These next three functions could use some DRY.
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
            player_stats = pd.read_json(response).fillna(0).set_index('OfficialId')

            return player_stats
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
            teams = pd.read_json(response).fillna(0).set_index('OfficialId')

            return teams
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        pass

    # TODO: def get_games():

    def get_games(self):
        url = games_list_endpoint

        try:
            r = requests.get(url, params=api_params)
            r.raise_for_status()
            api_response = json.dumps(r.text, indent=4, sort_keys=True)
            response = json.loads(api_response)

            global teams
            games_list = pd.read_json(response).fillna(0).set_index('OfficialCode')

            return games_list
            pass
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        pass

    def get_gamedata(self):
        pass

    
    # TODO: For each game in games, get stats and generate a data frame.


# example usage

# x gon' give it to ya.
x = xfl(token)

# get a list of all xfl players
players = x.get_players()
players.to_sql("players", con=engine, if_exists="replace")

# get a list of all xfl teams
teams = x.get_teams()
teams.to_sql("teams", con=engine, if_exists="replace")

# get a table of league wide stats for the seaso
player_stats = x.get_stats_combined("season")
player_stats.to_sql("player_stats", con=engine, if_exists="replace")

# print a list of games
games = x.get_games()
games.to_sql("games", con=engine, if_exists="replace")

# turn out the lights.
# the party's over.

import pandas as pd

players = pd.read_csv('processed_data/player_list.csv')
stats = pd.read_csv('processed_data/player_stats.csv')

output = pd.merge(players,stats,
                  on='OfficialId',
                  how='left').to_csv('processed_data/combined_stats.csv')


import pandas as pd
import numpy as np

df = pd.read_csv('match_data.csv')
df = df[(df['Pitch_x'].between(-52.5, 52.5)) & (df['Pitch_y'].between(-34, 34))]

df['Speed_filtered']= df.groupby('participation_id')['Speed (m/s)'].transform(
    lambda x: x.rolling(window=5, min_periods=1).mean()
)
#diffence in time is 0.1
dt = 0.1
#then to get the average speed between rows for each id
df['avg_speed'] = df.groupby('participation_id')['Speed_filtered'].transform(
    lambda x: (x + x.shift(1)) / 2
)
#then distance is speed * time
df['distance'] = df['avg_speed'] * dt

#the distance in speed zone 5
#19.5kmh/h = 5.41666666667 m/s
#25.1km/h = 6.97222222222 m/s
df['distance_zone_5'] = np.where(df['Speed_filtered'].between(5.41666666667, 6.97222222222), df['distance'], 0)

#then group by partcipation id
leaderboard = df.groupby('participation_id').agg(
    total_distance=('distance', 'sum'),
    total_distance_zone_5=('distance_zone_5', 'sum'),
    top_speed=('Speed_filtered', 'max'),
).reset_index()

leaderboard['rank_total_distance'] = leaderboard['total_distance'].rank(ascending=False)
leaderboard['rank_total_distance_zone_5'] = leaderboard['total_distance_zone_5'].rank(ascending=False)
leaderboard['rank_top_speed'] = leaderboard['top_speed'].rank(ascending=False)

#now will seperate these into 3 leaderboards 
print("leaderboard total distance")
print(leaderboard.sort_values(by='rank_total_distance').reset_index(drop=True))
print("\n")
print("leaderboard total distance zone 5")
print(leaderboard.sort_values(by='rank_total_distance_zone_5').reset_index(drop=True))
print("\n")
print("leaderboard top speed")
print(leaderboard.sort_values(by='rank_top_speed').reset_index(drop=True))
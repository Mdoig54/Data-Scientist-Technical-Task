import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df = pd.read_csv('match_data.csv')
df = df[(df['Pitch_x'].between(-52.5, 52.5)) & (df['Pitch_y'].between(-34, 34))]

#assuming to plot all points from csv to see what that looks like

#then to plot points for the ball, group by the ball id
ball_id = "ball"
df_ball = df[df['participation_id'] == ball_id]
df_player = df[df['participation_id'] != ball_id]

plt.figure(figsize=(10, 7))
plt.scatter(
    df_ball['Pitch_x'], df_ball['Pitch_y'], c='blue', alpha=0.7, label='Ball', s=1)

plt.scatter(
    df_player['Pitch_x'], df_player['Pitch_y'], c='red', alpha=0.05, label='Player', s=2)

#format 
plt.title("All points from match data, player vs ball")
plt.xlabel("Pitch x (m)")
plt.ylabel("Pitch y (m)")
plt.xlim(-52.5, 52.5)
plt.ylim(-34, 34)
plt.legend()
plt.show()

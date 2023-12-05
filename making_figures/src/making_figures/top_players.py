"""
Generate a bar chart to visualize the top fantasy performers in the NFL based on total fantasy points for Weeks 1-4.

Parameters:
-----------
None

Returns:
--------
None

Libraries Used:
---------------
- pandas: Data manipulation and analysis library.
- matplotlib.pyplot: Plotting library for creating visualizations.
- IPython.display.IFrame: Utility for embedding external content.
- numpy: Numerical computing library.
- seaborn: Statistical data visualization based on matplotlib.
- networkx: Library for the creation, manipulation, and study of the structure, dynamics, and functions of complex networks.
- plotly.graph_objects: Library for creating interactive plots.
- plotly.express: High-level interface for creating various visualizations.

Dependencies:
--------------
Ensure the required libraries are installed using appropriate package managers (e.g., pip).

Example Usage:
---------------
1. Load necessary libraries and specify the path to the CSV file containing weekly fantasy football data.
2. Read the CSV file into a pandas DataFrame.
3. Group the data by player name and calculate the total fantasy points for each player.
4. Sort the players based on total fantasy points in descending order.
5. Select the top 15 performers.
6. Create a bar chart with player names on the x-axis, total fantasy points on the y-axis, and player positions as data labels.
7. Save the resulting chart as an image file ('top_performers.png') and display it.

Note:
-----
Adjust the 'file_path' variable to the correct path of the CSV file on your system.
"""

# Import necessary libraries
from IPython.display import IFrame
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import kde
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import seaborn as sns
import networkx as nx

# Specify the full path to the file
file_path = r'C:\Users\admin\Desktop\MEMT680\HW4\making_figures\src\making_figures\Weeklydata.csv'

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(file_path)

# Group the data by player name and calculate the total fantasy points for each player
total_points = df.groupby('PLAYER NAME')['TOTAL'].sum().reset_index()

# Sort the players based on total fantasy points in descending order
total_points = total_points.sort_values(by='TOTAL', ascending=False)

# Select the top 15 performers
top_performers = total_points.head(15)

# Create a bar chart
plt.figure(figsize=(12, 12))
bars = plt.bar(range(len(top_performers['PLAYER NAME'])), top_performers['TOTAL'])

# Add player names and positions as data labels
for i, bar in enumerate(bars):
    player_name = top_performers['PLAYER NAME'].iloc[i]
    player_position = df[df['PLAYER NAME'] == player_name]['PLAYER POSITION'].iloc[0]
    text_label = f"{player_name}, {player_position}"
    
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
             text_label,
             ha='center', va='bottom', rotation=45)

# Customize the plot
plt.xlabel('Players')
plt.ylabel('Fantasy Points')
plt.title('Top Fantasy Performers NFL Weeks 1-4')
plt.ylim(0, 110)
plt.tight_layout()

# Save the resulting chart as an image file ('top_performers.png') and display it
plt.savefig('top_performers.png')
plt.show()

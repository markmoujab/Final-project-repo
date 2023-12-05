# Libraries
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

# Read the CSV file
df = pd.read_csv(file_path)

def plot_home_away_scatter():
    """
    Generate a scatter plot comparing total and projected points for home and away games.

    Parameters:
    - No direct parameters; uses global DataFrame `df`.

    Returns:
    - None.

    Outputs:
    - Displays a scatter plot.
    - Saves the plot as 'homeaway.png'.
    """
    # Filter data for home and away games
    home_games = df[df['Location'] == 'Home']
    away_games = df[df['Location'] == 'Away']

    # Scatter plot for home games
    plt.scatter(home_games['PROJ'], home_games['TOTAL'], label='Home Games', marker='x')

    # Scatter plot for away games
    plt.scatter(away_games['PROJ'], away_games['TOTAL'], label='Away Games', marker='x')

    # Customize the plot
    plt.title('Total vs Projected Points for Home and Away Games')
    plt.xlabel('Projected Points')
    plt.ylabel('Total Points')
    plt.legend()
    plt.grid(True)
    plt.xlim(0, 65)
    plt.ylim(0, 65)
    
    # Add a diagonal line for reference
    plt.plot([0, 65], [0, 65], color='gray', linestyle='--', label='x=y')
    
    plt.tight_layout()

    # Save the plot as an image
    plt.savefig('homeaway.png')

    # Show the plot
    plt.show()

# Call the function to generate and display the scatter plot
plot_home_away_scatter()

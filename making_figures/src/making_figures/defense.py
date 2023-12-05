import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd

# Specify the full path to the file
file_path = r'C:\Users\admin\Desktop\MEMT680\HW4\making_figures\src\making_figures\FantasyFootballWeekly.csv'

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(file_path, low_memory=False)
df = df.infer_objects()

# Replace "--" with NaN and drop rows with NaN
df.replace("--", pd.NA, inplace=True)
df.dropna(inplace=True)

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    # Dropdown for selecting player position
    dcc.Dropdown(
        id='position-dropdown',
        options=[
            {'label': position, 'value': position}
            for position in df['PLAYER POSITION'].unique()
        ],
        value=df['PLAYER POSITION'].unique()[0],  # Set default value
        style={'width': '50%'}
    ),
    
    # Bar plot to display the ten teams with the least total points against them
    dcc.Graph(id='bar-plot')
])

# Define callback to update bar plot based on dropdown selection
@app.callback(
    Output('bar-plot', 'figure'),
    [Input('position-dropdown', 'value')]
)
def update_bar_plot(selected_position):
    # Filter DataFrame based on selected position
    filtered_df = df[df['PLAYER POSITION'] == selected_position]
    
    # Find the ten teams with the least total points against them
    top_teams = filtered_df.groupby('PLAYER TEAM')['TOTAL'].sum().sort_values().head(10)
    
    # Create bar plot
    figure = {
        'data': [
            {'x': top_teams.index, 'y': top_teams.values, 'type': 'bar', 'name': 'Total Points'}
        ],
        'layout': {
            'title': f'Top 10 Teams with Least Total Points Against {selected_position}',
            'xaxis': {'title': 'Team'},
            'yaxis': {'title': 'Total Points'}
        }
    }
    
    return figure

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

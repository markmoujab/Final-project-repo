import dash
from dash import dcc, html
import plotly.express as px
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
    html.H1("Fantasy Football Player Comparison"),
    
    # Dropdown for selecting player position
    html.Label("Select Player Position:"),
    dcc.Dropdown(
        id='position-dropdown',
        options=[
            {'label': position, 'value': position} for position in df['PLAYER POSITION'].unique() if position is not None and pd.notna(position)
        ],
        value='QB',  # default value
        style={'width': '50%'}
    ),
    
    # Dropdown for selecting Player 1 Team
    html.Label("Select Player 1 Team:"),
    dcc.Dropdown(
        id='team1-dropdown',
        options=[
            {'label': team, 'value': team} for team in df['PLAYER TEAM'].unique() if team is not None and pd.notna(team)
        ],
        value='Phi',  # default value
        style={'width': '50%'}
    ),
    
    # Dropdown for selecting Player 2 Team
    html.Label("Select Player 2 Team:"),
    dcc.Dropdown(
        id='team2-dropdown',
        options=[
            {'label': team, 'value': team} for team in df['PLAYER TEAM'].unique() if team is not None and pd.notna(team)
        ],
        value='Dal',  # default value
        style={'width': '50%'}
    ),
    
    # Dropdown for selecting Player 1 Name
    html.Label("Select Player 1 Name:"),
    dcc.Dropdown(
        id='player1-dropdown',
        style={'width': '50%'}
    ),
    
    # Dropdown for selecting Player 2 Name
    html.Label("Select Player 2 Name:"),
    dcc.Dropdown(
        id='player2-dropdown',
        style={'width': '50%'}
    ),
    
    # Bar plot based on player stats
    dcc.Graph(id='player-comparison-plot'),
])

# Define callback to update Player 1 Name dropdown based on selected team and position
@app.callback(
    dash.dependencies.Output('player1-dropdown', 'options'),
    [dash.dependencies.Input('team1-dropdown', 'value'),
     dash.dependencies.Input('position-dropdown', 'value')]
)
def update_player1_dropdown(selected_team1, selected_position):
    if selected_team1 is not None:
        player1_options = [
            {'label': player, 'value': player} for player in
            sorted(df[(df['PLAYER TEAM'] == selected_team1) & (df['PLAYER POSITION'] == selected_position)]['PLAYER NAME'].unique())
        ]
    else:
        player1_options = []
    
    return player1_options

# Define callback to update Player 2 Name dropdown based on selected team and position
@app.callback(
    dash.dependencies.Output('player2-dropdown', 'options'),
    [dash.dependencies.Input('team2-dropdown', 'value'),
     dash.dependencies.Input('position-dropdown', 'value')]
)
def update_player2_dropdown(selected_team2, selected_position):
    if selected_team2 is not None:
        player2_options = [
            {'label': player, 'value': player} for player in
            sorted(df[(df['PLAYER TEAM'] == selected_team2) & (df['PLAYER POSITION'] == selected_position)]['PLAYER NAME'].unique())
        ]
    else:
        player2_options = []
    
    return player2_options

# Define callback to update the bar plot based on user input
@app.callback(
    dash.dependencies.Output('player-comparison-plot', 'figure'),
    [dash.dependencies.Input('position-dropdown', 'value'),
     dash.dependencies.Input('player1-dropdown', 'value'),
     dash.dependencies.Input('player2-dropdown', 'value')]
)
def update_player_comparison_plot(selected_position, selected_player1, selected_player2):
    # Bar plot based on player stats for the selected position
    if selected_position == 'QB':
        stats_labels = ['RUSHING TD', 'PASSING TD']
    elif selected_position in ['RB', 'WR', 'TE']:
        stats_labels = ['RECEIVING TAR', 'MISC TD', 'RECEIVING TD', 'RUSHING TD']
    else:
        return px.bar(), "Invalid player position selected."

    filtered_df_player1 = df[(df['PLAYER NAME'] == selected_player1) & (df['PLAYER POSITION'] == selected_position)]
    filtered_df_player2 = df[(df['PLAYER NAME'] == selected_player2) & (df['PLAYER POSITION'] == selected_position)]

    # Combine data for both players
    combined_df = pd.concat([filtered_df_player1, filtered_df_player2], ignore_index=True)


    fig = px.bar(
        combined_df.melt(id_vars='PLAYER NAME', value_vars=stats_labels),
        x='variable',
        y='value',
        color='PLAYER NAME',
        title=f'{selected_player1} vs {selected_player2} ({selected_position}) Comparison',
        labels={'variable': 'Stat', 'value': 'Value'},
        barmode='group',
        height=400
    )


    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

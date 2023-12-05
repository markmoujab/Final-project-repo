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
    html.H1("Player Projected vs Actual Points"),
    
    # Dropdown for selecting teams
    dcc.Dropdown(
        id='team-dropdown',
        options=[
            {'label': team, 'value': team} for team in df['PLAYER TEAM'].unique() if team is not None and pd.notna(team)
        ],
        value='Phi',  # default value
        style={'width': '50%'}
    ),
    
    # Dropdown for selecting player positions
    dcc.Dropdown(
        id='position-dropdown',
        options=[
            {'label': position, 'value': position} for position in df['PLAYER POSITION'].unique() 
            if position is not None and pd.notna(position)
        ],
        value='QB',  # default value
        style={'width': '50%'}
    ),
    
    # Scatter plot based on user-selected team and position
    dcc.Graph(id='points-plot'),
])

# Define callback to update the plot based on user input
@app.callback(
    dash.dependencies.Output('points-plot', 'figure'),
    [dash.dependencies.Input('team-dropdown', 'value'),
     dash.dependencies.Input('position-dropdown', 'value')]
)
def update_plot(selected_team, selected_position):
    filtered_df = df[(df['PLAYER TEAM'] == selected_team) & (df['PLAYER POSITION'] == selected_position)]

    # Sort the DataFrame by 'PROJ' and 'TOTAL'
    filtered_df = filtered_df.sort_values(by=['PROJ', 'TOTAL'])

    fig = px.scatter(
        filtered_df, x='PROJ', y='TOTAL', color='PLAYER NAME',
        title=f'Projected vs Actual Points for Players in {selected_team} - {selected_position}',
        labels={'PROJ': 'Projected Points', 'TOTAL': 'Actual Points'},
        hover_data=['PLAYER NAME', 'PLAYER POSITION', 'Opponent']
    )
    
        # Set xlim and ylim
    fig.update_layout(
        xaxis=dict(range=[0, 55]),
        yaxis=dict(range=[0, 55])
    )

    # Add x=y line
    fig.add_shape(
        type='line',
        x0=0,
        y0=0,
        x1=55,
        y1=55,
        line=dict(color='black', width=2)
    )
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

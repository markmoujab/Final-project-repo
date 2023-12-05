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
    html.H1("Fantasy Football Analysis"),
    
    # Dropdown for selecting teams
    html.Label("Select Team:"),
    dcc.Dropdown(
        id='team-dropdown',
        options=[
            {'label': team, 'value': team} for team in df['PLAYER TEAM'].unique() if team is not None and pd.notna(team)
        ],
        value='Phi',  # default value
        style={'width': '50%'}
    ),
    
    # Dropdown for listing QBs from selected team
    html.Label("Select QB:"),
    dcc.Dropdown(
        id='qb-dropdown',
        style={'width': '50%'}
    ),
    
    # Scatter plot based on rushing and passing yards
    dcc.Graph(id='yards-plot'),
])

# Define callback to update the QB dropdown based on selected team
@app.callback(
    dash.dependencies.Output('qb-dropdown', 'options'),
    [dash.dependencies.Input('team-dropdown', 'value')]
)
def update_qb_dropdown(selected_team):
    if selected_team is not None:
        qb_options = [
            {'label': player, 'value': player} for player in
            sorted(df[(df['PLAYER TEAM'] == selected_team) & (df['PLAYER POSITION'] == 'QB')]['PLAYER NAME'].unique())
        ]
    else:
        qb_options = []
    
    return qb_options

# Define callback to update the scatter plot based on user input
@app.callback(
    dash.dependencies.Output('yards-plot', 'figure'),
    [dash.dependencies.Input('team-dropdown', 'value'),
     dash.dependencies.Input('qb-dropdown', 'value')]
)
def update_plot(selected_team, selected_qb):
    # Scatter plot based on rushing and passing yards for the selected QB
    filtered_df = df[(df['PLAYER TEAM'] == selected_team) & (df['PLAYER POSITION'] == 'QB') & (df['PLAYER NAME'] == selected_qb)]

    fig = px.scatter(
        filtered_df, x='RUSHING YDS', y='PASSING YDS', color = 'Location',
        title=f'Rushing Yards vs Passing Yards for {selected_qb} (QB) in {selected_team}',
        labels={'RUSHING YDS': 'Rushing Yards', 'PASSING YDS': 'Passing Yards'},
        hover_data=['PLAYER NAME', 'PLAYER POSITION', 'Opponent']
    )

    # Set xlim and ylim
    fig.update_layout(
        xaxis=dict(range=[0, max(filtered_df['RUSHING YDS'].max(), 100)]),  # Adjust the upper limit for better visibility
        yaxis=dict(range=[0, max(filtered_df['PASSING YDS'].max(), 100)])
    )

    # Add x=y line
    fig.add_shape(
        type='line',
        x0=0,
        y0=0,
        x1=max(filtered_df['RUSHING YDS'].max(), 100),
        y1=max(filtered_df['PASSING YDS'].max(), 100),
        line=dict(color='black', width=2)
    )

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

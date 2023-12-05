# Import necessary libraries
import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd


# Specify the full path to the file
file_path = r'C:\Users\admin\Desktop\MEMT680\HW4\making_figures\src\making_figures\Weeklydata.csv'

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(file_path)

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1("Projected vs Actual Points for Players Against a Team, if you're looking for a kicker play Jake Eliott"),
    
    # Dropdown for selecting teams
    dcc.Dropdown(
        id='team-dropdown',
        options=[
            {'label': team, 'value': team} for team in df['Opponent'].unique() if team is not None and pd.notna(team)
        ],
        value='Phi',  # default value
        style={'width': '50%'}
    ),

    
    # Scatter plot based on user-selected team
    dcc.Graph(id='points-plot'),

])

# Define callback to update the plot based on user input
@app.callback(
    dash.dependencies.Output('points-plot', 'figure'),
    [dash.dependencies.Input('team-dropdown', 'value')]
)
def update_plot(selected_team):
    filtered_df = df[df['Opponent'] == selected_team]
    fig = px.scatter(
        filtered_df, x='PROJ', y='TOTAL', color='PLAYER POSITION',
        title=f'Projected vs Actual Points for Players in {selected_team}',
        labels={'PROJ': 'Projected Points', 'TOTAL': 'Actual Points'},
        hover_data=['PLAYER NAME', 'PLAYER POSITION', 'PLAYER TEAM']
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

print(df['Opponent'].unique())

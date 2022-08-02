from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import pandas as pd
from train_model import linreg_model

forecasts, date_list = linreg_model(building_nr=5)


app = Dash(__name__)

app.layout = html.Div([
    html.H4('Interactive color selection with simple Dash example'),
    html.P("Select color:"),
    dcc.Dropdown(
        id="dropdown1",
        options=['Gold', 'MediumTurquoise', 'LightGreen'],
        value='Gold',
        clearable=False,
    ),
    dcc.Dropdown(
        id="dropdown2",
        options=['small', 'medium', 'large'],
        value='small',
        clearable=False,
    ),
    dcc.Graph(id="graph"),
])


@app.callback(
    Output("graph", "figure"), 
    Input("dropdown1", "value"),
    Input("dropdown2", "value"),
    )
def display_color(color, size):
    if size == 'small':
        data = [0.1, 0.2, 0.6]
    elif size == 'medium':
        data = [1, 2, 3]
    else:
        data = [10, 20, 20]
    fig = go.Figure(
        data=go.Bar(y=data, # replace with your own data source
                    marker_color=color))
    return fig


app.run_server(debug=True, port=8113)
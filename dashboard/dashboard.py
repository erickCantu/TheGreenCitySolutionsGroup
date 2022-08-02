from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta, date
today = date.today()
from train_model import linreg_model

forecasts, date_list = linreg_model(building_nr=5)

# forecasts_df = pd.DataFrame(forecasts)


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
    dcc.DatePickerSingle(
            id='my-date-picker-single',
            month_format='Y-M-D',
            #min_date_allowed=today - timedelta(years=12, days=3),
            #max_date_allowed=today + timedelta(days=730),
            initial_visible_month=datetime(2011, 5, 5),
            date=datetime(2011, 5, 5)),
    dcc.Graph(id="graph"),
])


@app.callback(
    Output("graph", "figure"), 
    Input("dropdown1", "value"),
    Input("dropdown2", "value"),
    Input("my-date-picker-single", "date"),
    )
def display_color(color, size, date):
    if size == 'small':
        data = [0.1, 0.2, 0.6]
    elif size == 'medium':
        data = [1, 2, 3]
    else:
        data = [10, 20, 20]
    start_date = pd.Timestamp(date)
    end_date = pd.Timestamp(date) + pd.Timedelta(hours=24)
    masked_forecasts = forecasts.loc[start_date:end_date]
    fig = px.line(masked_forecasts, x="datetime", y="linreg_poly")
    return fig


app.run_server(debug=True, port=8113)
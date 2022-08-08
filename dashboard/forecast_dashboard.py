from calendar import month
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np

dfs = {}
for i in range(1, 10):
    dfs[i] = (pd.read_csv(f"../data/preprocessed/Building_{i}.csv")
        .astype({"datetime": "datetime64"})
        .set_index("datetime")
    )
dfs['all'] = (pd.read_csv(f"../data/preprocessed/Agg_buildings.csv")
    .astype({"datetime": "datetime64"})
    .set_index("datetime")
)

forecasts = {}
forecasts["all"] = pd.read_pickle('../data/models/linreg_poly_building_all.pkl')
for i in range(1, 10):
    forecasts[i] = pd.read_pickle(f'../data/models/linreg_poly_building_{i}.pkl')

app = Dash(external_stylesheets=[dbc.themes.FLATLY])

with open("template.html", 'r') as template_html:
    template_string = template_html.readlines()
    app.index_string = "".join(template_string)
    
preset_dropdown = dcc.Dropdown(
    id="preset-dropdown",
    className="dropdown",
    options=[f"Preset {i}" for i in range(1, 9)],
    value='Choose preset',
    clearable=True,
    style={"min-width": "8em", "margin-left": "0em", "color": "gray"},
)

radioitems = html.Div(
    [
        html.H4("Building", className="pl-0"),
        dbc.RadioItems(
            options=[*[{"label": f"{i}", "value": i} for i in range(1, 10)],
                {"label": "All", "value": "all"},
            ],
            value=1,
            id="building-selection",
            className="btn-group-vertical",
            inputClassName="btn-check",
            labelClassName="btn btn-outline-primary",
            labelCheckedClassName="active",
            labelStyle={"width": "6em"},
        ),
    ],
    style={"margin": "auto"},
)

checklist = html.Div(
    [
        html.H3("Prediction models", style={"margin-top": "4.5em"}),
        dbc.Checklist(
            options=[
                {"label": "Linear regression", "value": "lin_reg", "disabled": False},
                {"label": "SARIMAX", "value": 1, "disabled": True},
                {"label": "Prophet", "value": 2, "disabled": True},
                {"label": "TBATS", "value": 3, "disabled": True},
                {"label": "Random Forest", "value": 4, "disabled": True},
                {"label": "XGBoost", "value": 5, "disabled": True},
                {"label": "Baseline", "value": "baseline"},
            ],
            value=["lin_reg"],
            id="model-selection",
        ),
    ]
)

switches = html.Div(
    [
        html.H4("View options"),
        dbc.Checklist(
            options=[
                {"label": "Display weather data", "value": "weather", "disabled": False},
                {"label": "Display actual data", "value": "actual"},
                {"label": "Show previous day", "value": "previousday", "disabled": False},
            ],
            value=[],
            id="config-toggles",
            switch=True,
            className="ml-3",
        ),
    ],
    style={"position": "absolute", "bottom": "1em"},
)

dropdown_time = dcc.Dropdown(
    id="time-selection",
    className="dropdown mx-2",
    options=[str(i).zfill(2) for i in range(24)],
    value='00',
    #style={'width': '30%', 'display': 'inline-block', 'verticalAlign': 'middle'},
    style={'min-width': '5em'},
    clearable=False,
)

datepick = dcc.DatePickerSingle(
    id="datepicker",
    display_format="MM-DD",
    #month_format="MMMM, \Y 4",
    month_format="MMMM, 2022",
    min_date_allowed="2011-01-01",
    max_date_allowed="2011-12-31",
    initial_visible_month="2011-08-01",
    date="2011-05-05",
    className="mr-4",
)

left_div = html.Div([
    #dropdown_buildings,
    radioitems,
], className="col-1",
    style={"padding-top": "1em", "background-color": "rgb(255,255,255)", "justify-content": "center"},
)
right_div = html.Div([
    checklist,
    switches
], className="col-2 bg-light",
style={"position": "relative"},
)

time_input_group = html.Div([
    html.H5("Select date and time:", style={"vertical-align": "bottom", "padding-top": "0.35em", "margin-right": "1em"}),
    datepick,
    #dcc.Input(type="text", className="form-control", value="12", style={"width": "3em"}),
    dropdown_time,
    #html.Span(":00", className="input-group-text"),
    html.H5(":00", style={"vertical-align": "bottom", "padding-top": "0.35em", "margin-left": "0em", "margin-right": "0.2em"}),
    html.H5("...or choose a preset: ", style={"vertical-align": "bottom", "padding-top": "0.35em", "margin-left": "2em", "margin-right": "0.2em"}),
    preset_dropdown,
    ], className="input-group mb-3")

middle_div = html.Div([
html.Div(
    [
        dcc.Graph(id="graph",),
        html.Div([
            html.Div([
            time_input_group,
            ], style={'display': 'inline-block', 'width': 'fit-content'})
        ],
        style={'border-radius': 0, "text-align": "center"},
        ),
    ],
)],
className="col-11",
style={"background-color": "rgb(255,255,255)"},
)

    
app.layout = html.Div(
    [
        html.Div([
            html.Div([
                html.H1("Energy usage forecast", className="p-0 pt-4 pb-2"),
                html.Div([
                    left_div, middle_div,
                ], className="row"),
            ], className="col-10 bg-white"),
            right_div
        ], className="row"),
    ],
className="container dash-bootstrap")

@app.callback(
        Output("graph", "figure"),
        Input("building-selection", "value"),
        Input("datepicker", "date"),
        Input("time-selection", "value"),
        Input("model-selection", "value"),
        Input("config-toggles", "value"),
    )
def display_graph(building_nr, selected_date, selected_time, models, config_toggles):

    forecast_df = forecasts[building_nr]
    df = dfs[building_nr]

    year_start = pd.Timestamp("2011-01-01")
    year_end = pd.Timestamp("2011-12-31 23:00")

    forecast_df["baseline"] = df.net_load_kW.shift(24*365).loc[year_start:year_end]

    start_date = pd.Timestamp(f"{selected_date} {selected_time}:00")
    day_before = start_date - pd.Timedelta(hours=24)
    end_date = start_date + pd.Timedelta(hours=24)
    masked_forecasts = forecast_df.loc[start_date+pd.Timedelta(hours=1):end_date]
    mf2 = forecast_df.loc[day_before:start_date]

    #fig = px.line(masked_forecasts, x="datetime", y="linreg_poly", template="simple_white")
    fig = px.line(x=masked_forecasts["datetime"], y=[np.nan for _ in masked_forecasts["datetime"]], template="simple_white")
    if "lin_reg" in models:
        fig.append_trace({'x':masked_forecasts["datetime"], 'y':masked_forecasts["linreg_poly"]}, 1, 1)

    if ("actual" in config_toggles) or ("previousday" in config_toggles):
        if ("actual" in config_toggles) and ("previousday" in config_toggles):
            df_actual = forecast_df.loc[day_before:end_date]
        elif ("actual" in config_toggles):
            df_actual = forecast_df.loc[start_date:end_date]
        elif ("previousday" in config_toggles):
            df_actual = forecast_df.loc[day_before:start_date]
        fig.append_trace({'x':df_actual["datetime"], 'y':df_actual["net_load_kW"]}, 1, 1)
    
    #TODO: if "previousday" not in config_toggles, deactivate "weather" switch?
    if ("weather" in config_toggles) and ("previousday" in config_toggles):
        fig.append_trace({'x':mf2["datetime"], 'y':mf2["outdoor_temp"]}, 1, 1)

    if "baseline" in models:
        fig.append_trace({'x':masked_forecasts["datetime"], 'y':masked_forecasts["baseline"]}, 1, 1)
    
    fig.add_vline(x=start_date, line_width=3, line_dash="dash", line_color="green")
    fig.update_layout(showlegend=False,
                      xaxis_title=None,
                      yaxis_title=None,
    )
    
    fig.update_yaxes(
        ticksuffix=" kW",
        showgrid=True,
        griddash="dot",
        linewidth=0,
        linecolor="white",
    )
    return fig

app.run_server(debug=True, port=8100)

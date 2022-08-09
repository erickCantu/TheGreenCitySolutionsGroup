from calendar import month
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import sys
sys.path.append("../notebooks/")
from green_city.utils import datetime2index, index2datetime

#dfs = {}
#for i in range(1, 10):
#    dfs[i] = (pd.read_csv(f"../data/preprocessed/Building_{i}.csv")
#        .astype({"datetime": "datetime64"})
#        .set_index("datetime")
#    )
#dfs['all'] = (pd.read_csv(f"../data/preprocessed/Agg_buildings.csv")
#    .astype({"datetime": "datetime64"})
#    .set_index("datetime")
#)
#
#forecasts = {}
#for model in ["linreg_poly", "random_forest", "xgboost", "xgboost_reduced_features"]:
#    forecasts[model] = {}
#    for i in [*list(range(1, 10)), "all"]:
#        forecasts[model][i] = pd.read_pickle(f'../data/models/{model}_building_{i}.pkl')

pred_indices = [32135, 33311, 26478, 33357, 30387, 30794, 31800, 28783]
pred_times = [index2datetime(pi) for pi in pred_indices]
pred_time_hours = [(d.strftime("%Y-%m-%d"), d.strftime("%H")) for d in pred_times]

all_forecasts = pd.read_pickle("../data/models/all_models.pkl")

set_date = "2011-08-09"
set_time = "18"

app = Dash(external_stylesheets=[dbc.themes.FLATLY])

with open("template.html", 'r') as template_html:
    template_string = template_html.readlines()
    app.index_string = "".join(template_string)
    
preset_dropdown = dcc.Dropdown(
    id="preset-dropdown",
    className="dropdown",
    options=[f"Preset {i}" for i in range(1, 9)],
    value='Choose preset',
    clearable=False,
    style={"min-width": "8em", "margin-left": "0em", "color": "gray"},
)

radioitems = html.Div(
    [
        html.H4("Building", className="pl-0 pt-4"),
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
                #{"label": "SARIMAX", "value": "sarimax", "disabled": True},
                #{"label": "Prophet", "value": "prophet", "disabled": True},
                #{"label": "TBATS", "value": "tbats", "disabled": True},
                {"label": "XGBoost", "value": "xgboost"},
                {"label": "XGB (reduced features)", "value": "xgboost_reduced_features"},
                {"label": "Random Forest", "value": "random_forest"},
                {"label": "Linear regression", "value": "linreg_poly", "disabled": False},
                {"label": "Baseline", "value": "baseline"},
            ],
            value=[],
            id="model-selection",
        ),
    ]
)

switches = html.Div(
    [
        html.H4("View options"),
        dbc.Checklist(
            options=[
                #{"label": "Display weather data", "value": "weather", "disabled": False},
                {"label": "Display actual data", "value": "actual"},
                {"label": "Show previous day", "value": "previousday", "disabled": False},
            ],
            value=["actual"],
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
    value=set_time,
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
    initial_visible_month=set_date,
    date=set_date,
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
], className="col-2",
style={"position": "relative", "background-color": "rgb(230, 245, 252)"},
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
            html.Div([],
            className="col-1 my-3 companylogo",
            #style={'background-image': "assets/green-energy.png"},
            ),
            html.Div([
                html.H1("Forecasting building energy demand")
                ],
                className="col-11",
                style={'background-color': 'rgb(149, 184, 116)',
                       'color': 'white', "padding": "20px"}
            ),
        ], className="row"),
        html.Div([
            html.Div([
                #html.H1("Energy usage forecast", className="p-0 pt-4 pb-2"),
                html.Div([
                    left_div, middle_div,
                ], className="row"),
            ], className="col-10 bg-white"),
            right_div
        ], className="row"),
    ],
className="container dash-bootstrap mt-0")

@app.callback(
        Output("datepicker", "date"),
        Output("time-selection", "value"),
        Input("preset-dropdown", "value"),
    )
def change_date_and_time(preset):
    if preset == "Choose preset":
        return (set_date, set_time)
    else:
        i = int(preset[-1])
    return pred_time_hours[i-1]

@app.callback(
        Output("graph", "figure"),
        Input("building-selection", "value"),
        Input("datepicker", "date"),
        Input("time-selection", "value"),
        Input("model-selection", "value"),
        Input("config-toggles", "value"),
    )
def display_graph(building_nr, selected_date, selected_time, models, config_toggles):
    set_date = selected_date
    set_time = selected_time
    
    building_forecasts = all_forecasts[building_nr]
    
    year_start = building_forecasts.index[0]
    year_end = building_forecasts.index[-1]
    assert year_start == pd.Timestamp("2011-01-01")
    assert year_end == pd.Timestamp("2011-12-31 23:00")

    start_date = pd.Timestamp(f"{selected_date} {selected_time}:00")
    #current_date = start_date - pd.Timedelta(hours=1)
    day_before = start_date - pd.Timedelta(hours=24)
    end_date = start_date + pd.Timedelta(hours=24)
    masked_forecasts = building_forecasts.loc[start_date+pd.Timedelta(hours=1):end_date]
    mf2 = building_forecasts.loc[day_before:start_date]

    #fig = go.Figure()
    fig = px.line(x=masked_forecasts.index, y=[np.nan for _ in masked_forecasts.index], template="simple_white",)
    #              specs=[])
    #fig = px.line(x=masked_forecasts.index, y=[np.nan for _ in masked_forecasts.index], template="simple_white",)
    #              specs=[])
    #fig.add_trace(go.Scatter(
    #    x=masked_forecasts.index,
    #    y=[np.nan for _ in masked_forecasts.index],
    #    name="yaxis1 data",
    #))
    #fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    #fig.update_layout(
    #    yaxis=dict(
    #        title="yaxis title",
    #        titlefont=dict(
    #            color="#1f77b4"
    #        ),
    #        tickfont=dict(
    #            color="#1f77b4"
    #        )
    #    ),
    #    yaxis2=dict(
    #        title="yaxis2 title",
    #        titlefont=dict(
    #            color="#ff7f0e"
    #        ),
    #        tickfont=dict(
    #            color="#ff7f0e"
    #        ),
    #        anchor="free",
    #        overlaying="y",
    #        side="left",
    #        position=0.15
    #    ),
    #)

    actual_usage = building_forecasts["actual_usage"]
    current_actual_usage = actual_usage[start_date]
    if "previousday" in config_toggles:
        #plotting actual usage in time before
        df_actual = actual_usage.loc[day_before:start_date]
        fig.append_trace(
            {'type': 'scatter',
             'mode': 'lines',
             'x': df_actual.index,
             'y': df_actual,
             'name': 'Actual usage',
             'line': {
                'color': 'black',
             }},
             row=1, col=1,
        )

    if "actual" in config_toggles:
        df_actual = actual_usage.loc[start_date:end_date]
        fig.append_trace(
            {'type': 'scatter',
             'mode': 'lines',
             'x': df_actual.index,
             'y': df_actual,
             'name': 'Actual usage',
             'line': {
                'color': 'black',
                'dash': 'dash',
             }},
             row=1, col=1,
        )

    {"label": "XGBoost", "value": "xgboost"},
    {"label": "XGB (reduced features)", "value": "xgboost_reduced_features"},
    {"label": "Random Forest", "value": "random_forest"},
    {"label": "Linear regression", "value": "linreg_poly", "disabled": False},
    {"label": "Baseline", "value": "baseline"},
    model_names = {
        "xgboost": "XGBoost",
        "xgboost_reduced_features": "XGBoost (reduced features)",
        "random_forest": "Random forest",
        "linreg_poly": "Linear regression",
        "baseline": "Baseline",
    }
    model_colors = {
        "xgboost": "green",
        "xgboost_reduced_features": "blue",
        "random_forest": "red",
        "linreg_poly": "gray",
        "baseline": "orange",
    }
    for model in models:
        times = [start_date, *masked_forecasts.index]
        values = [current_actual_usage, *masked_forecasts[model]]
        #fig.append_trace({'x':masked_forecasts.index, 'y':masked_forecasts[model]}, 1, 1)
        fig.append_trace({'x':times, 'y':values, 'name': model_names[model], 'line': {'color': model_colors[model]}}, row=1, col=1)#, secondary_y=True)
    
    #if ("weather" in config_toggles) and ("previousday" in config_toggles):
    #    fig.append_trace({'x':mf2.index, 'y':mf2["outdoor_temp"], 'name': 'Outdoor temperature', 'yaxis': 'yaxis2'}, 1, 1)

    #if "baseline" in models:
    #    fig.append_trace({'x':masked_forecasts.index, 'y':masked_forecasts.baseline}, 1, 1)
    
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

    fig.update_xaxes(
        tickformat="%H:%M\n %b %d, 2022")

    return fig

app.run_server(debug=True, port=8100)

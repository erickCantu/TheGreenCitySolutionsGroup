import plotly.graph_objects as go

def plot_balance(timespan, adding, substracting, data):
    power_consumption = data.loc[timespan, adding].sum()
    power_generation = data.loc[timespan, substracting].sum()

    fig = go.Figure(go.Waterfall(
        name = "20", orientation = "v",
        measure = [*["relative"]*len(adding), "total", *["relative"]*len(substracting), "total"],
        x = [*adding, "Net consumption", *substracting, "grid power"],
        textposition = "outside",
        text = ["+", "+", "+", "=", "-", "="],
        y = [*power_consumption, 0, *[-i for i in power_generation], 0],
        connector = {"line":{"color":"rgb(63, 63, 63)"}},
    ))

    fig.update_layout(
            title = "Energy balance",
            showlegend = True
    )

    fig.show()
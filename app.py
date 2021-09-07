# from flask import Flask
# from dash import Dash
# from dash import dcc
# from  dash import  html

# app = Flask(__name__)
# dash_app = Dash(
#     __name__,
#     server=app,
#     url_base_pathname='/dash/'
# )

# dash_app.layout = html.Div(children=[
#     html.H1(children='Hello Dash'),

#     html.Div(children='''
#         This is Dash running on Azure App Service without a Docker container.
#     '''),

#     dcc.Graph(
#         id='example-graph',
#         figure={
#             'data': [
#                 {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
#                 {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
#             ],
#             'layout': {
#                 'title': 'Dash Data Visualization'
#             }
#         }
#     )
# ])

#########################################################################################################################
from flask import Flask
import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = Flask(__name__)
dash_app = dash.Dash(
    __name__,
    server=app,
    url_base_pathname='/dash/'
)


df = pd.read_csv(
    "https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Other/Dash_Introduction/intro_bees.csv"
)

df = df.groupby(["State", "ANSI", "Affected by", "Year", "state_code"])[
    ["Pct of Colonies Impacted"]
].mean()
df.reset_index(inplace=True)
print(df[:5])
print(df["Affected by"].unique())

# ------------------------------------------------------------------------------
# App layout
dash_app.layout = html.Div(
    [
        html.H1("Dash Web Application Demo 1", style={"text-align": "center"}),
        html.H4(children="Year"),
        dcc.Dropdown(
            id="slct_year",
            options=[
                {"label": "2015", "value": 2015},
                {"label": "2016", "value": 2016},
                {"label": "2017", "value": 2017},
                {"label": "2018", "value": 2018},
            ],
            multi=False,
            value=2015,
            style={"width": "40%"},
        ),
        html.Br(),
        html.H4(children="Reason"),
        dcc.Dropdown(
            id="affected_by",
            options=[
                {"label": "Disease", "value": "Disease"},
                {"label": "Other", "value": "Pesticides"},
                {"label": "Pests Excl Varroa", "value": "Pests_excl_Varroa"},
                {"label": "Varroa Mites", "value": "Varroa_mites"},
                {"label": "Unknown", "value": "Unknown"},
            ],
            multi=False,
            value="",
            style={"width": "40%"},
        ),
        html.Br(),
        html.Div(id="output_container", children=[]),
        html.Br(),
        dcc.Graph(id="my_bee_map", figure={}),
    ]
)


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@dash_app.callback(
    [
        Output(component_id="output_container", component_property="children"),
        Output(component_id="my_bee_map", component_property="figure"),
    ],
    [
        Input(component_id="slct_year", component_property="value"),
        Input(component_id="affected_by", component_property="value"),
    ],
)
def update_graph(option_slctd, affected_by):
    print(option_slctd)
    print(type(option_slctd))
    print(affected_by)

    container = "The year chosen by user was: {}".format(option_slctd)

    dff = df.copy()
    dff = dff[dff["Year"] == option_slctd]
    dff = dff[dff["Affected by"] == affected_by]

    # Plotly Express
    # fig = px.choropleth(
    #     data_frame=dff,
    #     locationmode="USA-states",
    #     locations="state_code",
    #     scope="usa",
    #     color="Pct of Colonies Impacted",
    #     hover_data=["State", "Pct of Colonies Impacted"],
    #     color_continuous_scale=px.colors.sequential.YlOrRd,
    #     labels={"Pct of Colonies Impacted": "% of Bee Colonies"},
    #     template="plotly_dark",
    # )

    # Plotly Graph Objects (GO)
    # https://plotly.com/python/choropleth-maps/
    fig = go.Figure(
        data=[
            go.Choropleth(
                locationmode="USA-states",
                locations=dff["state_code"],
                z=dff["Pct of Colonies Impacted"].astype(float),
                colorscale="Reds",
            )
        ]
    )

    fig.update_layout(
        title_text="Bees Affected by {:} in the USA".format(affected_by),
        title_xanchor="center",
        title_font=dict(size=24),
        title_x=0.5,
        geo=dict(scope="usa"),
    )

    return container, fig

@app.route("/dash")
def my_dash_app():
    return dash_app.index()




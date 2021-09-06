from flask import Flask
from dash import Dash
import dash_core_components as dcc
import dash_html_components as html

app = Flask(__name__)
dash_app = dash.Dash(
    __name__,
    server=app,
    url_base_pathname='/dash'
)

dash_app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        This is Dash running on Azure App Service without a Docker container.
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])

@app.route("/dash")
def my_dash_app():
    return dash_app.index()

@app.route("/")
def index():
    return "Welcome to flask "


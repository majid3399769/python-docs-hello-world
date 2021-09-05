from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Welcome to Azure web application"


@app.route("/main")
def hello():
    return "Main Page"

from flask import Flask,render_template
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.config["FLASK_ENV"] = os.getenv("FLASK_ENV")
app.config["FLASK_APP"] = os.getenv("FLASK_APP")

@app.route('/')

def index():
    return "<h1>Hello world!</h1>"
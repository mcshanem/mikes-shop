from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from dotenv import load_dotenv
import os

# Load variables from .env file
load_dotenv()

# Create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')

# Connect Bootstrap to Flask app
Bootstrap5(app)

@app.route('/')
def home():
    return "Mike's Shop"

if __name__ == '__main__':
    app.run(debug=True)

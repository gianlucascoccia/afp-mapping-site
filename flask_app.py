
from flask import Flask

app = Flask(__name__)

# Welcome route
@app.route('/')
def hello_world():
    return 'Hello from Flask!'

# Page not found route
# Pre-test questionaire
# Mappping test
# Post-test questionaire

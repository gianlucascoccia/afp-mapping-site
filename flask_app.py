import sys
import os.path
from flask import Flask, render_template

app = Flask(__name__)

# Set some variables according to whether we are on production or development
if app.config['DEBUG']:
    # We are in development
    # Sets activities list folder
    APPS_FOLDER = "apps"
    pass
else:
    # We are in production
    # Sets activities list folder
    APPS_FOLDER = ""
    pass


# Default route
@app.route('/')
def default():
    return 'Explanation!'


# Pre-test questionaire
@app.route('/before-test/<appname>')
def before_explanation(appname):
    if not activity_file_exists(appname):
        return render_template('app_not_found.html', appname=appname)
    return render_template('pre-test.html', appname=appname)


# Mappping test
@app.route('/test/<appname>')
def test(appname):
    if not activity_file_exists(appname):
        return render_template('app_not_found.html', appname=appname)
    return 'Testooo!'


# Post-test questionaire
@app.route('/after-test/<appname>')
def after_questionaire(appname):
    if not activity_file_exists(appname):
        return render_template('app_not_found.html', appname=appname)
    return 'Questionaire!'


# Utility function for safety url-check
# Checks whether the app exists in our db, otherwise redirect to error page
def activity_file_exists(appname: str) -> bool:
    print('{}/{}-activities.csv'.format(APPS_FOLDER, appname))
    return os.path.isfile('{}/{}-activities.csv'.format(APPS_FOLDER, appname))


# Page not found route
@app.errorhandler(404)
def page_not_found(e):
    return render_template('page_not_found.html'), 404

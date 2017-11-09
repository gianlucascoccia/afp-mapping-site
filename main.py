import os.path
import csv
import datetime
from flask import Flask, render_template, request

from contact_form import ContactForm
from mapping_form import MappingForm

app = Flask(__name__)

# Set some variables according to whether we are on production or development
if app.config['DEBUG']:
    # We are in development
    # Sets activities list folder
    APPS_FOLDER = "apps"
    OUT_FOLDER = "out"
    pass
else:
    # We are in production
    # Sets activities list folder
    APPS_FOLDER = "/home/Fragoel2/afp-mapping-site/apps"
    OUT_FOLDER = "/home/Fragoel2/afp-mapping-site/out"
    pass


# Default route
@app.route('/')
def default():
    return render_template('about.html')


# Pre-test questionaire
@app.route('/before-test/<appname>', methods=['GET', 'POST'])
def before_explanation(appname):
    # error handling: wrong url access
    if not activity_file_exists(appname):
        return handle_app_not_exists(appname)
    return render_template('before_test.html', appname=appname)


# Mappping test
@app.route('/test/<appname>', methods=['GET', 'POST'])
def test(appname):
    submitted_feature, submitted_description = "", ""
    timestamp = datetime.datetime.utcnow()
    # error handling: wrong url access
    if not activity_file_exists(appname):
        return handle_app_not_exists(appname)

    # load the list of activities for the app
    activities_file = open('{}/{}-activities.csv'.format(APPS_FOLDER, appname), "r")
    reader = csv.reader(activities_file, delimiter=";")
    activities = [(activity[0], activity[0]) for activity in reader]
    activities_file.close()

    form = MappingForm(request.form)
    form.activities.choices = activities
    if request.method == 'POST' and form.validate():
        # if a mapping was submitted, retrieve it's data and reset form
        submitted_feature = form.feature_name.data
        submitted_description = form.feature_description.data
        # activities
        form.feature_name.data, form.feature_description.data = "", ""

    # store data to file
    with open(os.path.join(OUT_FOLDER, '{}-mappings.csv'.format(appname)), 'a') as csv_file:
        writer = csv.writer(csv_file, delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([timestamp, submitted_feature, submitted_description])
        csv_file.flush()

    return render_template('test.html', appname=appname, form=form,
                           submitted_feature=submitted_feature, activities=activities)


# Post-test questionaire
@app.route('/after-test/<appname>', methods=['GET', 'POST'])
def after_questionaire(appname):
    # error handling: wrong url access
    if not activity_file_exists(appname):
        return handle_app_not_exists(appname)
    return 'Questionaire!'


# Page not found route
@app.errorhandler(404)
def page_not_found(e):
    form = ContactForm(request.form)
    if request.method == 'POST' and form.validate():
        return handle_error_submit(form)
    return render_template('page_not_found.html', form=form), 404


# Utility function for safety url-check
# Checks whether the app exists in our db, otherwise redirect to error page
def activity_file_exists(appname: str) -> bool:
    return os.path.isfile('{}/{}-activities.csv'.format(APPS_FOLDER, appname))


# Utility function to render the app does not exist page
def handle_app_not_exists(appname):
    form = ContactForm(request.form)
    if request.method == 'POST' and form.validate():
        return handle_error_submit(form)
    return render_template('app_not_found.html', appname=appname, form=form)


# Utility function to handle the error report page
def handle_error_submit(form):
    name, email, message = form.name.data, form.email.data, form.message.data
    with open(os.path.join(OUT_FOLDER, 'messages.csv'), 'a') as csv_file:
        writer = csv.writer(csv_file, delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([name, email, message])
        csv_file.flush()
    return render_template('message_sent.html', name=name)

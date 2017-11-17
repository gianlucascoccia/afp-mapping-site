import os.path
import csv
import time
from flask import Flask, render_template, request, url_for
from werkzeug.utils import redirect
from contact_form import ContactForm
from mapping_form import MappingForm

app = Flask(__name__)

# Set some variables according to whether we are on production or development
if app.config['DEBUG']:
    # We are in development
    # Sets activities list folder
    APPS_FOLDER = "apps"
    OUT_FOLDER = "out"
else:
    # We are in production
    # Sets activities list folder
    APPS_FOLDER = "/home/Fragoel2/afp-mapping-site/apps"
    OUT_FOLDER = "/home/Fragoel2/afp-mapping-site/out"


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

    # error handling: wrong url access
    if not activity_file_exists(appname):
        return handle_app_not_exists(appname)

    # load the list of activities for the app
    activities_file = open('{}/{}-activities.csv'.format(APPS_FOLDER, appname), "r")
    reader = csv.reader(activities_file, delimiter=";")
    activities = [(activity[0], activity[0]) for activity in reader]
    activities_file.close()

    # First access to page
    if request.method == 'GET':
        feature_count = 1
        feature_list = [feature_count]

    if request.method == 'POST':
        if len(request.form['features']) > 2:
            feature_list = list(map(int, request.form['features'][1:-1].split(',')))
            feature_count = max(feature_list)
        else:
            feature_count = 0
            feature_list = []

        # Handle case in which we need to add a field to form
        if request.form['submit'] == 'Add new row':
            feature_count += 1
            feature_list.append(feature_count)

        # Handle case in which we need to remove a field to form
        if request.form['submit'].startswith('Delete row '):
            removal_id = int(request.form['submit'][-1])
            feature_list.pop(removal_id - 1)
            MappingForm.delete_form_field_dinamically(removal_id)

    # build form dynamically
    MappingForm.build_mapping_form_dinamically(feature_list, activities)
    form = MappingForm(request.form)

    # Handle cases in which form was submitted
    if request.method == 'POST':
        if request.form['submit'] == 'Submit' and form.validate():
            # save the submit timestamp
            with open(os.path.join(OUT_FOLDER, '{}-timestamps.csv'.format(appname)), 'a') as csv_file:
                writer = csv.writer(csv_file, delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(['FormSubmit', time.time()])
                csv_file.flush()
            # store form data to file
            with open(os.path.join(OUT_FOLDER, '{}-mappings.csv'.format(appname)), 'a') as csv_file:
                for feature_num in feature_list:
                    writer = csv.writer(csv_file, delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow([
                                    form.data['feature_name_' + str(feature_num)],
                                    form.data['feature_description_' + str(feature_num)],
                                    form.data['feature_activity_' + str(feature_num)]
                                    ])
                csv_file.flush()
            return redirect(url_for('after_questionaire', appname=appname))

    return render_template('test.html', appname=appname, form=form, activities=activities,
                           features_list=feature_list)


# Post-test questionaire
@app.route('/after-test/<appname>', methods=['GET', 'POST'])
def after_questionaire(appname):
    # error handling: wrong url access
    if not activity_file_exists(appname):
        return handle_app_not_exists(appname)
    return render_template('after_test.html')


@app.route('/store-ts/<appname>')
def store_timestamp(appname):
    timestamp = request.args.get('timestamp', 0, int)
    clicked = request.args.get('clicked', 'Null', str)
    with open(os.path.join(OUT_FOLDER, '{}-timestamps.csv'.format(appname)), 'a') as csv_file:
        writer = csv.writer(csv_file, delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([clicked, timestamp])
        csv_file.flush()
    return '', 204


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
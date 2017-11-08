import os.path
import csv
from flask import Flask, render_template, request
from contact_form import ContactForm

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
    if not activity_file_exists(appname):
        return handle_app_not_exists(appname)
    return render_template('before_test.html', appname=appname)


# Mappping test
@app.route('/test/<appname>', methods=['GET', 'POST'])
def test(appname):
    if not activity_file_exists(appname):
        return handle_app_not_exists(appname)
    return 'Testooo!'


# Post-test questionaire
@app.route('/after-test/<appname>', methods=['GET', 'POST'])
def after_questionaire(appname):
    if not activity_file_exists(appname):
        return handle_app_not_exists(appname)
    return 'Questionaire!'


# Page not found route
@app.errorhandler(404)
def page_not_found(e):
    return render_template('page_not_found.html'), 404


# Utility function for safety url-check
# Checks whether the app exists in our db, otherwise redirect to error page
def activity_file_exists(appname: str) -> bool:
    print('{}/{}-activities.csv'.format(APPS_FOLDER, appname))
    return os.path.isfile('{}/{}-activities.csv'.format(APPS_FOLDER, appname))


# Utility function to render the app does not exist page
def handle_app_not_exists(appname):
    form = ContactForm(request.form)
    if request.method == 'POST' and form.validate():
        name,email,message = form.name.data, form.email.data, form.message.data
        with open(os.path.join(OUT_FOLDER,'messages.csv'), 'a') as csvfile:
            writer = csv.writer(csvfile, delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([name] + [email] + [message])
            csvfile.flush()
        return render_template('message_sent.html', name=name)
    return render_template('app_not_found.html', appname=appname, form=form)

from wtforms import Form, TextField, TextAreaField, SubmitField, validators
from multi_checkbox import MultiCheckboxField


class MappingForm(Form):
    feature_name = TextField("Feature name", [validators.DataRequired()])
    feature_description = TextAreaField("Brief feature description", [validators.DataRequired()])
    activities = MultiCheckboxField('App activities', choices=[])
    submit = SubmitField("Submit")


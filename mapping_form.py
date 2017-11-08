from wtforms import Form, TextField, TextAreaField, SubmitField, validators


class MappingForm(Form):
    feature_name = TextField("Feature name", [validators.DataRequired()])
    feature_description = TextAreaField("Brief feature description", [validators.DataRequired()])
    #activities =
    submit = SubmitField("Submit")


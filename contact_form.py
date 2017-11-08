from wtforms import Form, TextField, TextAreaField, SubmitField, validators


class ContactForm(Form):
    name = TextField("Name", [validators.DataRequired()])
    email = TextField("Email", [validators.DataRequired(), validators.Email()])
    message = TextAreaField("Message", [validators.DataRequired()])
    submit = SubmitField("Send")


from wtforms import Form, TextField, TextAreaField, SubmitField, validators, ValidationError
from multi_checkbox import MultiCheckboxField


class MappingForm(Form):
    feature_name = TextField("Feature name", [validators.DataRequired()])
    feature_description = TextAreaField("Brief feature description", [validators.DataRequired()])
    activities = MultiCheckboxField('App activities', choices=[])
    submit = SubmitField("Submit")

    def validate_activities(self, field):
        if len(field.data) == 0:
            raise ValidationError('Must select at least one activity')


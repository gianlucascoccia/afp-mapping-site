from wtforms import Form, TextField, TextAreaField, SubmitField, validators, ValidationError, StringField
from multi_checkbox import MultiCheckboxField


class MappingForm(Form):
    submit = SubmitField("Submit")

    # Utility function to add build form dinamically
    @staticmethod
    def build_mapping_form_dinamically(features_list, activities):
        if features_list:
            for index, feature in enumerate(features_list):
                setattr(MappingForm, "feature_name_" + str(feature),
                        StringField("Feature name", [validators.DataRequired()]))
                setattr(MappingForm, "feature_description_" + str(feature),
                        TextAreaField("Brief feature description"))
                setattr(MappingForm, "feature_activity_" + str(feature),
                        MultiCheckboxField('App activities', [
                            validators.DataRequired(message='Feature in row {} must be mapped with at least one activity!'
                                                    .format(index + 1))], choices=activities))

    @staticmethod
    def delete_form_field_dinamically(feature_id):
        try:
            print("FIELD TO REMOVE: " + str(feature_id))
            delattr(MappingForm, "feature_name_" + str(feature_id))
            delattr(MappingForm, "feature_description_" + str(feature_id))
            delattr(MappingForm, "feature_activity_" + str(feature_id))
        except AttributeError:
            print("DEL ERROR FOR " + str(feature_id))

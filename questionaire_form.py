from wtforms import Form, TextAreaField, SubmitField, validators


class QuestionaireForm(Form):
    question_one = TextAreaField("Question 1", [validators.DataRequired()],
                                 description="Lorem ipsum dolor sit amet, consectetur adipiscing "
                                             "elit. Nullam accumsan commodo nunc.")
    question_two = TextAreaField("Question 2", [validators.DataRequired()],
                                 description="Lorem ipsum dolor sit amet, consectetur adipiscing "
                                             "elit. Nullam accumsan commodo nunc.")
    question_three = TextAreaField("Question 3", [validators.DataRequired()],
                                   description="Lorem ipsum dolor sit amet, consectetur adipiscing "
                                               "elit. Nullam accumsan commodo nunc.")
    submit = SubmitField("Send")


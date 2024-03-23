from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, TextAreaField, SelectField, SubmitField, FieldList, FormField, BooleanField
from wtforms.validators import DataRequired

class OptionForm(FlaskForm):
    option_text = StringField('Option', validators=[DataRequired()])
    is_correct = BooleanField('Correct Option', default=False)

class QuizQuestionForm(FlaskForm):
    question_text = TextAreaField('Question', validators=[DataRequired()])
    options = FieldList(FormField(OptionForm), min_entries=4, max_entries=4)

class QuizForm(FlaskForm):
    questions = FieldList(FormField(QuizQuestionForm), min_entries=1)
    submit = SubmitField('Submit')

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, SelectField
from wtforms.validators import DataRequired, Length


class EditForm(FlaskForm):
    rating = StringField(label='Your Rating Out of 10 e.g. 7.5', validators=[DataRequired()])
    review = StringField(label='Your Review', validators=[DataRequired(), Length(min=10, max=250)])
    submit = SubmitField(label='Done')


class MovieForm(FlaskForm):
    title = StringField(label='Movie Title', validators=[DataRequired(), Length(min=4, max=250)])
    submit = SubmitField(label='Add Movie')


# def edit_form(ranking_choices):
#     class EditForm(FlaskForm):
#         rating = StringField(label='Your Rating Out of 10 e.g. 7.5', validators=[DataRequired()])
#         review = StringField(label='Your Review', validators=[DataRequired(), Length(min=10, max=250)])
#         ranking = StringField(label='Movie Ranking', validators=[DataRequired()])
#         ranking = SelectField(label='Select Ranking', choices=ranking_choices)
#         submit = SubmitField(label='Done')
#
#     return EditForm()
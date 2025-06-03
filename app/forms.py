from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class StudentSignupForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject you need help with', validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Sign Up')

class MentorSignupForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject you can teach', validators=[DataRequired(), Length(min=2, max=100)])
    availability = StringField('Your Availability (e.g., "Mon 9-12, Wed 2-5")', validators=[DataRequired(), Length(min=5, max=200)])
    submit = SubmitField('Sign Up as Mentor')

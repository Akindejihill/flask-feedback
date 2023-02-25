from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, TextAreaField, BooleanField
from wtforms.validators import InputRequired, Optional, Email, Length

class FeedbackForm(FlaskForm):
    """ Form for adding a post """
    title = StringField("Title", validators=[InputRequired(), Length(max=100)])
    content = TextAreaField("Body text", validators=[InputRequired()])

class UserForm(FlaskForm):
    """Form for adding a user"""
    username = StringField("Username", validators=[InputRequired(), Length(max=20)])
    first_name = StringField("First Name", validators=[InputRequired(), Length(max=30)])
    last_name = StringField("Last Name", validators=[InputRequired(), Length(max=30)])
    email = StringField("email", validators=[InputRequired(),Length(max=50)])

    password = PasswordField("Password", validators=[InputRequired(), Length(min=8)])
    confirm_password = PasswordField("Confirm password", validators=[InputRequired(), Length(min=8)])

class LoginForm(FlaskForm):
    """Form for adding a user"""
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password")
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length
from flask_pagedown.fields import PageDownField


class UserForm(FlaskForm):
    name = StringField('What is your name', validators=[DataRequired()])
    submit = SubmitField('submit')


class EditProfileForm(FlaskForm):
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1, 64)])
    body = PageDownField('Body', validators=[DataRequired()])
    submit = SubmitField('Submit')

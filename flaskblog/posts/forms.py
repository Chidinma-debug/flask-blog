from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


#Data required prevents field from beinge empty, Length restricts length
#Create a class. In bracket include what the class inherits from

class PostForm(FlaskForm):
    title= StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, IntegerField, TextAreaField, SelectField, PasswordField
from wtforms.validators import Required, Length, Optional, Email, EqualTo

class DatasetSubmit(Form):
    name = StringField('Enter the name of the dataset', validators=[Required()])
    category = SelectField('Select the category', choices = [('RR', 'RR'), ('EKG', 'EKG')])
    number_of_files = IntegerField('Enter the number of files', validators=[Required()])
    description = TextAreaField('Enter the description of the dataset', validators=[Optional(), Length(max=300)])
    keywords = StringField('Enter keywords separating them by comma ","', validators=[Optional()])
    submit = SubmitField('Submit')

class UserSubmit(Form):
    name = StringField("Enter the user's name (one word)", validators=[Required()])
    fullname = StringField("Enter the full name", validators=[Required()])
    email = StringField('Enter e-mail', validators=[Email(),Required()])
    password = PasswordField('Enter password', validators = [Required(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm password', validators = [Required()])
    submit = SubmitField('Submit')

class ContactOwner(Form):
    content = TextAreaField('Enter your message', validators=[Optional(), Length(max=300)])
    submit = SubmitField('Submit')

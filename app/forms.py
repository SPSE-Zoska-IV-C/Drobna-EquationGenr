from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo

class CreateEquationForm(FlaskForm):
    type = SelectField('Type', choices=[('logarithmic-substitute', 'logarithmic substitute'),
                                        ('logarithmic-mixed', 'logarithmic mixed methods'), 
                                        ('exponential-substitute', 'exponential substitute'),
                                        ('exponential-match', 'exponential match'),
                                        ('exponential-log', 'exponential log')])
    level = SelectField('Level', choices=[('simple', 'simple'), ('advanced', 'advanced')])
    number = IntegerField('Number', validators=[DataRequired()])
    submit = SubmitField('Create')

class CreateFunctionForm(FlaskForm):
    type = SelectField('Type', choices=[('logarithmic', 'logarithmic'), ('exponential', 'exponential')])
    number = IntegerField('Number', validators=[DataRequired()])
    submit = SubmitField('Create')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Password confirmation', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')



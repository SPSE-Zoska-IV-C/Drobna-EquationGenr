from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo

class CreateEquationForm(FlaskForm):
    type = SelectField('Type', choices=[('logarithmic - solved by substitution', 'logarithmic - solved by substitution'),
                                        ('logarithmic - solved by logarithm rules', 'logarithmic - solved by logarithm rules'),
                                        ('logarithmic - random methods of solving', 'logarithmic - random methods of solving'),
                                        ('exponential - solved by substitution', 'exponential - solved by substitution'),
                                        ('exponential - solved by converting it to same base', 'exponential - solved by converting it to same base'),
                                        ('exponential - solved by logarithms', 'exponential - solved by logarithms'),
                                        ('exponential - random methods of solving', 'exponential - random methods of solving'),
                                        ('random equations', 'random equations')])
    level = SelectField('Level', choices=[('simple', 'simple'), ('advanced', 'advanced')])
    number = IntegerField('Number', validators=[DataRequired()])
    submit = SubmitField('Create')

class CreateFunctionForm(FlaskForm):
    type = SelectField('Type', choices=[('logarithmic', 'logarithmic functions'), ('exponential', 'exponential functions'), ('random functions', 'random functions')])
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



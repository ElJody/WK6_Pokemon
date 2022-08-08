from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app import models


class FindPokemon(FlaskForm):
    pokemon_name = StringField("Enter Pokemon Name", validators=[DataRequired()])
    submit = SubmitField('Find It!!!')


class LoginForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
        validators=[DataRequired(), EqualTo('password', message='Passwords Must Match')])
    submit = SubmitField('Register')

    def validate_email(form, field):
        same_email_user = models.User.query.filter_by(email = field.data).first()
        if same_email_user:
            print('Email is Already in Use')
            return ValidationError('Email is Already in Use')


class EditProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
         validators=[DataRequired(), EqualTo('password', message='Passwords Must Match')])
    submit = SubmitField('Edit Profile')

class PokemonForm(FlaskForm):
    poke_name = StringField("Pokemon Name", validators=[DataRequired()])


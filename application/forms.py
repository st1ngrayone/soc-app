from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Email, EqualTo, Regexp


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired()])
    password = StringField(validators=[InputRequired()])
    submit = SubmitField('submit')


class RegisterForm(FlaskForm):
    username = StringField(validators=[
        InputRequired(), Regexp('^\\w+$', message="Логин должен содержать только буквы и цифры!")
    ])
    password = StringField(validators=[InputRequired()])
    password_2 = StringField(validators=[InputRequired(), EqualTo('password', message='Пароли должны совпадать')])
    email = StringField(validators=[InputRequired(), Email()])
    name = StringField(label='Ваше имя', validators=[InputRequired()])
    lastname = StringField(label='Ваша фамилия', validators=[InputRequired()])
    submit = SubmitField('submit')

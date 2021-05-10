from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField
from wtforms.validators import InputRequired, Email, EqualTo, Regexp, NumberRange

from application.entity.profile import Profile


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired()])
    password = StringField(validators=[InputRequired()])
    submit = SubmitField('submit')


class SearchForm(FlaskForm):
    name = StringField(validators=[InputRequired()])
    lastname = StringField(validators=[InputRequired()])
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
    city = StringField(label='Ваш город')
    birth_date = DateField(label='Дата рождения')
    gender = SelectField(label='Ваш пол', choices=[('m', 'Мужской'), ('f', 'Женский'), ('u', 'Не указан')])
    submit = SubmitField('submit')

    def populate_profile(self):
        return Profile(
            self.birth_date.data, self.email.data, self.gender.data,
            self.name.data, self.lastname.data, self.city.data
        )


class ProfileForm(FlaskForm):
    password = StringField(validators=[InputRequired()])
    email = StringField(validators=[InputRequired(), Email()])
    name = StringField(label='Ваше имя', validators=[InputRequired()])
    lastname = StringField(label='Ваша фамилия', validators=[InputRequired()])
    city = StringField(label='Ваш город')
    birth_date = DateField(label='Дата рождения')
    gender = SelectField(label='Ваш пол', choices=[('m', 'Мужской'), ('f', 'Женский'), ('u', 'Не указан')])
    submit = SubmitField('submit')

    def populate_profile(self):
        return Profile(
            self.birth_date.data, self.email.data, self.gender.data,
            self.name.data, self.lastname.data, self.city.data
        )

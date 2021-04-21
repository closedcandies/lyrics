from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    query = StringField('Введите запрос', validators=[DataRequired()])
    button = SubmitField('Найти')


class LoginForm(FlaskForm):
    login = StringField('Введите логин', validators=[DataRequired()])
    password = StringField('Введите пароль', validators=[DataRequired()])
    button = SubmitField('Войти')


class SignForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    login = StringField('Логин', validators=[DataRequired()])
    password = StringField('Придумайте пароль', validators=[DataRequired()])
    check_password = StringField('Повторите пароль', validators=[DataRequired()])
    button = SubmitField('Зарегестрироваться')


class EditForm(FlaskForm):
    name = StringField('Название песни', validators=[DataRequired()])
    text = StringField('Текст', validators=[DataRequired()])
    button = SubmitField('Готово')
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class JobForm(FlaskForm):
    description = StringField('Описание', validators=[DataRequired()])
    team_leader = StringField('team lead id')
    work_size = StringField('Время работы')
    collaborators = StringField('участники')
    start_date = StringField('Дата начала')
    end_date = StringField('Дата конца')
    is_finished = BooleanField('Работа закончена')
    submit = SubmitField('Добавить')


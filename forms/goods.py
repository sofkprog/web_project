from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired
from wtforms import FileField


class NewsForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    content = TextAreaField("Описание")
    is_private = BooleanField("Личное")
    submit = SubmitField('Применить')
    price = FloatField('Стоимость в рублях', validators=[DataRequired()])
    image = FileField('Фото')
    poisk = StringField(""
                        "")

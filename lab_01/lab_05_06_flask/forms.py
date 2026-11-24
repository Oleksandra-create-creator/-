from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length, ValidationError

class EventRegistrationForm(FlaskForm):
    name = StringField(
        'Повне ім\'я',
        validators=[DataRequired(message='Це поле є обов\'язковим'), Length(min=5, max=100, message='Ім\'я має містити від 5 до 100 символів')]
    )
    email = EmailField(
        'Електронна пошта',
        validators=[DataRequired(message='Це поле є обов\'язковим'), Email(message='Введіть коректну email адресу')]
    )
    ticket_type = SelectField(
        'Тип квитка',
        choices=[('standard', 'Стандартний'), ('vip', 'VIP'), ('student', 'Студентський')],
        validators=[DataRequired(message='Оберіть тип квитка')]
    )
    message = TextAreaField(
        'Повідомлення організаторам',
        validators=[Length(max=500, message='Повідомлення не може перевищувати 500 символів')]
    )
    submit = SubmitField('Зареєструватися')

    def validate_name(self, field):
        if len(field.data.split()) < 2:
            raise ValidationError('Будь ласка, введіть ім\'я та прізвище.')

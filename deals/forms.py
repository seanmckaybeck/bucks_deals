from flask_wtf import FlaskForm, RecaptchaField
from wtforms.fields import IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired


class ContactForm(FlaskForm):
    pass


class ItemForm(FlaskForm):
    item = IntegerField('Item number', validators=[DataRequired()])
    recaptcha = RecaptchaField()
    submit = SubmitField('Submit')


class PercentForm(FlaskForm):
    percentage = SelectField('Bucks Percentage',
                             choices=[(1, 1), (2, 2),
                                      (4, 4), (6, 6),
                                      (8, 8), (10, 10)], id='bucks-percent')
    cashback = SelectField('Credit Card Cashback Percentage',
                           choices=[(0.5, 0.5), (1, 1),
                                    (1.5, 1.5), (2, 2),
                                    (2.5, 2.5), (3, 3),
                                    (3.5, 3.5), (4, 4),
                                    (4.5, 4.5), (5, 5)], id='cash-percent', default=2)

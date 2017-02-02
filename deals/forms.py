from flask_wtf import FlaskForm
from wtforms.fields import IntegerField, SubmitField
from wtforms.validators import DataRequired


class ContactForm(FlaskForm):
    pass


class ItemForm(FlaskForm):
    item = IntegerField('Item number', validators=[DataRequired()])
    submit = SubmitField('Submit')


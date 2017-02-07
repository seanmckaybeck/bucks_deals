from flask_wtf import FlaskForm
from wtforms.fields import IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired


class ContactForm(FlaskForm):
    pass


class ItemForm(FlaskForm):
    item = IntegerField('Item number', validators=[DataRequired()])
    submit = SubmitField('Submit')


class PercentForm(FlaskForm):
    percentage = SelectField('Bucks percentage', choices=[('1', '1'), ('2', '2'),
                                                          ('4', '4'), ('6', '6'),
                                                          ('8', '8'), ('10', '10')], id='bucks-percent')


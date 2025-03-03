from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SubmitField, BooleanField, Form, IntegerField, SelectField, TextAreaField, HiddenField, RadioField, FileField, EmailField
from wtforms.validators import DataRequired

class AddCrypto(FlaskForm):
    symbol = StringField(label="Symbol", validators=[DataRequired()])
    amount = DecimalField(label="Amount", validators=[DataRequired()])
    submit = SubmitField(label='Submit')
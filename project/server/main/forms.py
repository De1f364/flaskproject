# project/server/main/forms.py


from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class AddressForm(FlaskForm):
    name = StringField("Address groupname", [DataRequired()])
    addresses = StringField("Addresses", [DataRequired()])


class AppForm(FlaskForm):
    name = StringField("Apps groupname", [DataRequired()])
    apps = StringField("Applications", [DataRequired()])

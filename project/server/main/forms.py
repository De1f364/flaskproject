# project/server/main/forms.py


from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo


from project.server import bcrypt, db
from project.server.models import Addrgroup, Appgroup


class AddressForm(FlaskForm):
    name_addrs = StringField("Address groupname")
    addresses = StringField("Addresses")


class AppForm(FlaskForm):
    name_apps = StringField("Apps groupname")
    apps = StringField("Applications")


class SelectAddrForm(FlaskForm):
    addr_groups = QuerySelectField(query_factory=lambda: Addrgroup.query.all(), get_label="name")

class SelectAppForm(FlaskForm):
    app_groups = QuerySelectField(query_factory=lambda: Appgroup.query.all(), get_label="name")
# project/server/main/forms.py


from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FieldList, FormField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo


from project.server import bcrypt, db
from project.server.models import Addrgroup, Appgroup


class AddressForm(FlaskForm):
    project_addr = SelectField("Project", choices=[("api-common", "API-Common"),
                                                   ("api-invest", "API-Invest"),
                                                   ("api-travel", "API-Travel"),
                                                   ("api-mvno", "API-MVNO")])
    name_addrs = StringField("Address groupname")
    addresses = StringField("Addresses")


class AppForm(FlaskForm):
    project_app = SelectField("Project", choices=[("api-common", "API-Common"),
                                                   ("api-invest", "API-Invest"),
                                                   ("api-travel", "API-Travel"),
                                                   ("api-mvno", "API-MVNO")])
    name_apps = StringField("Apps groupname")
    apps = StringField("Applications")


class SelectProjectForm(FlaskForm):
    project_select = SelectField("Project", choices=[("api-common", "API-Common"),
                                                   ("api-invest", "API-Invest"),
                                                   ("api-travel", "API-Travel"),
                                                   ("api-mvno", "API-MVNO")])


class AccessName(FlaskForm):
    name = StringField("Access name")


class SelectAddrForm(FlaskForm):
    addr_groups = QuerySelectField(query_factory=lambda: Addrgroup.query.all(), get_label="name")


class SelectAppForm(FlaskForm):
    app_groups = QuerySelectField(query_factory=lambda: Appgroup.query.all(), get_label="name")

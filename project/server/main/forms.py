# project/server/main/forms.py


from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FieldList, FormField, TextAreaField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo


from project.server import bcrypt, db
from project.server.models import Addrgroup, Appgroup, Projects


class CreateProject(FlaskForm):
    project_name = StringField("Project name")


class AddressForm(FlaskForm):
    project_select = QuerySelectField("Project",
                                      allow_blank=True,
                                      query_factory=lambda: Projects.query.all(),
                                      get_label="name")
    name_addrs = StringField("Address groupname")
    addresses = TextAreaField("Addresses")


class AppForm(FlaskForm):
    project_app = QuerySelectField("Project",
                                   query_factory=lambda: Projects.query.all(),
                                   get_label="name")
    name_apps = StringField("Apps groupname")
    apps = TextAreaField("Applications")


class SelectProjectForm(FlaskForm):
    project_select = QuerySelectField("Project",
                                      allow_blank=True,
                                      query_factory=lambda: Projects.query.all(),
                                      get_label="name")
    name = StringField("Access name")


class AccessName(FlaskForm):
    name = StringField("Access name")


class SelectAddrFormSRC(FlaskForm):
    src_groups = QuerySelectField("src groups",
                                  query_factory=lambda: Addrgroup.query.all(),
                                  get_label="name")


class SelectAddrFormDST(FlaskForm):
    dst_groups = QuerySelectField("dst groups",
                                  query_factory=lambda: Addrgroup.query.all(),
                                  get_label="name")


class SelectAppForm(FlaskForm):
    app_groups = QuerySelectField("apps",
                                  query_factory=lambda: Appgroup.query.all(),
                                  get_label="name")

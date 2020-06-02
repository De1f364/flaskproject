# project/server/main/forms.py


from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FieldList, FormField
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
    addresses = StringField("Addresses")


class AppForm(FlaskForm):
    project_app = QuerySelectField("Project",
                                   query_factory=lambda: Projects.query.all(),
                                   get_label="name")
    name_apps = StringField("Apps groupname")
    apps = StringField("Applications")


class SelectProjectForm(FlaskForm):
    # project_choices = [(projects.id, projects.project) for projects in Projects.query.all()]
    # project_select = SelectField("Project", choices=edit_user())
    project_select = QuerySelectField("Project",
                                      allow_blank=True,
                                      query_factory=lambda: Projects.query.all(),
                                      get_label="name")
    name = StringField("Access name")
    # def __init__(self):
    #     self.projects = [(projects.id, projects.project) for projects in Projects.query.all()]
    #
    # def edit_user(self):
    #     # projects = [(projects.id, projects.project) for projects in Projects.query.all()]
    #     return self.projects
    #
    # project_select = SelectField("Project", choices=edit_user())


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

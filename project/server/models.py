# project/server/models.py


import datetime

from flask import current_app

from project.server import db, bcrypt


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, email, password, admin=False):
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, current_app.config.get("BCRYPT_LOG_ROUNDS")
        ).decode("utf-8")
        self.registered_on = datetime.datetime.now()
        self.admin = admin

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return "<User {0}>".format(self.email)


class Addrgroup(db.Model):

    __tablename__ = "addrgroups"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    addresses = db.Column(db.String(255), nullable=False)
    project = db.Column(db.String(255), nullable=False)

    def __init__(self, name, addresses, project):
        self.name = name
        self.addresses = addresses
        self.project = project


class Appgroup(db.Model):

    __tablename__ = "appgroups"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    apps = db.Column(db.String(255), nullable=False)
    project = db.Column(db.String(255), nullable=False)

    def __init__(self, name, apps, project):
        self.name = name
        self.apps = apps
        self.project = project


class Accesses(db.Model):
    __tablename__ = "accesses"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    src = db.Column(db.String(255), nullable=False)
    dst = db.Column(db.String(255), nullable=False)
    app = db.Column(db.String(255), nullable=False)

    def __init__(self, name, src, dst, app):
        self.name = name
        self.src = src
        self.dst = dst
        self.app = app


class Projects(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project = db.Column(db.String(255), unique=True, nullable=False)

    def __init__(self, project):
        self.project = project

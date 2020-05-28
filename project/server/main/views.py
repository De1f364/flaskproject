# project/server/main/views.py


from flask import render_template, Blueprint, request, flash, redirect, url_for

from project.server import bcrypt, db
from project.server.models import Addrgroup, Appgroup, Accesses, Projects
from project.server.main.forms import AddressForm, AppForm, SelectAddrForm, SelectAppForm, SelectProjectForm, AccessName, CreateProject

import json

main_blueprint = Blueprint("main", __name__)


@main_blueprint.route("/")
def home():
    access_name = AccessName()
    # addr_form = AddressForm()
    # app_form = AppForm()
    select_project = SelectProjectForm()
    new_project = CreateProject()
    # select_addr_form = SelectAddrForm()
    # select_app_form = SelectAppForm()
    return render_template("main/home.html",
                           access_name=access_name,
                           # addr_form=addr_form,
                           # app_form=app_form,
                           new_project=new_project,
                           select_project=select_project)
                           # select_addr_form=select_addr_form,
                           # select_app_form=select_app_form)


@main_blueprint.route("/about/")
def about():
    addr_form = AddressForm()
    app_form = AppForm()
    select_project = SelectProjectForm()
    return render_template("main/about.html",
                           addr_form=addr_form,
                           app_form=app_form,
                           select_project=select_project)


@main_blueprint.route("/handle_data_addr", methods=["GET", "POST"])
def handle_data_addr():
    json_to_api = {}
    addr_form = AddressForm(request.form)
    if addr_form.validate_on_submit():
        print(addr_form.addresses())
        group_name = Addrgroup(project=addr_form.project_addr.data, name=addr_form.name_addrs.data, addresses=addr_form.addresses.data)
        db.session.add(group_name)
        db.session.commit()
        json_to_api["id"] = group_name.name
        json_to_api["address"] = group_name.addresses
        json_to_api["type"] = "ip"
        json.dumps(json_to_api)
        flash(json_to_api)
        flash("Address group added", "success")
        return redirect(url_for("main.home"))
    return redirect(url_for("main.about"))


@main_blueprint.route("/handle_data_app", methods=["GET", "POST"])
def handle_data_app():
    json_to_api = {}
    app_form = AppForm(request.form)
    if app_form.validate_on_submit():
        group_name = Appgroup(project=app_form.project_app.data, name=app_form.name_apps.data, apps=app_form.apps.data)
        db.session.add(group_name)
        db.session.commit()

        # json_to_api["id"] = group_name.name
        # json_to_api["address"] = group_name.addresses
        # json_to_api["type"] = "ip"
        # json.dumps(json_to_api)
        flash(json_to_api)
        flash("App group added", "success")
        return redirect(url_for("main.home"))
    return redirect(url_for("main.home"))


@main_blueprint.route("/handle_data_project", methods=["GET", "POST"])
def handle_data_project():
    new_project = CreateProject(request.form)
    if new_project.validate_on_submit():
        print(new_project.project_name.data)
        add_project = Projects(project=new_project.project_name.data)
        db.session.add(add_project)
        db.session.commit()

        flash("Project created", "success")
        return redirect(url_for("main.home"))
    return redirect(url_for("main.home"))


@main_blueprint.route("/handle_data_accesses", methods=["GET", "POST"])
def handle_data_accesses():
    json_to_api = {}
    name = AccessName(request.form)
    select_src_addr = SelectAddrForm(request.form)
    select_dst_addr = SelectAddrForm(request.form)
    app = SelectAppForm(request.form)
    if select_src_addr.validate_on_submit() and select_dst_addr.validate_on_submit():
        access = Accesses(name=name.name.data,
                          src=select_src_addr.src_groups.name,
                          dst=select_dst_addr.src_groups.name,
                          app=app.app_groups.name)
        db.session.add(access)
        db.session.commit()
        json_to_api["name"] = access.name
        json_to_api["src"] = access.src
        json_to_api["dst"] = access.dst
        json_to_api["app"] = access.app
        json.dumps(json_to_api)
        flash(json_to_api)
        flash("Access created", "success")
        return redirect(url_for("main.home"))
    return redirect(url_for("main.about"))


@main_blueprint.route("/get_accesses/", methods=["GET", "POST"])
def get_accesses():
    project = SelectProjectForm(request.form)
    # get_access_addr = SelectAddrForm(query_factory=lambda: Addrgroup.query.filter_by(project=project.project_select.data))
    get_access_addr_src = SelectAddrForm()
    get_access_addr_dst = SelectAddrForm()
    get_access_app = SelectAppForm()
    if project.validate_on_submit():
        flash(Addrgroup.query.filter_by(project=project.project_select.data), 'success')
        flash(type(project.project_select.data), 'success')
        print(get_access_addr_src.src_groups(query_factory=lambda: Addrgroup.query.filter_by(project=project.project_select.data)))
        return render_template("main/get_accesses.html",
                               get_access_addr_src=get_access_addr_src,
                               get_access_addr_dst=get_access_addr_dst,
                               get_access_app=get_access_app,
                               project=project.project_select,
                               name=project.name)

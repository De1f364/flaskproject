# project/server/main/views.py


from flask import render_template, Blueprint, request, flash, redirect, url_for

from project.server import bcrypt, db
from project.server.models import Addrgroup, Appgroup, Accesses
from project.server.main.forms import AddressForm, AppForm, SelectAddrForm, SelectAppForm, SelectProjectForm, AccessName

import json

main_blueprint = Blueprint("main", __name__)


@main_blueprint.route("/")
def home():
    access_name = AccessName()
    addr_form = AddressForm()
    app_form = AppForm()
    select_project = SelectProjectForm()
    select_addr_form = SelectAddrForm()
    select_app_form = SelectAppForm()
    return render_template("main/home.html",
                           access_name=access_name,
                           addr_form=addr_form,
                           app_form=app_form,
                           select_project=select_project,
                           select_addr_form=select_addr_form,
                           select_app_form=select_app_form)


@main_blueprint.route("/about/")
def about():
    flash(Addrgroup.query.with_entities(Addrgroup.name))
    return render_template("main/about.html")


@main_blueprint.route("/handle_data_addr", methods=["GET", "POST"])
def handle_data_addr():
    json_to_api = {}
    addr_form = AddressForm(request.form)
    if addr_form.validate_on_submit():
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
    return redirect(url_for("main.about"))


@main_blueprint.route("/handle_data_accesses", methods=["GET", "POST"])
def handle_data_accesses():
    json_to_api = {}
    name = AccessName(request.form)
    src_addr = SelectAddrForm(request.form)
    dst_addr = SelectAddrForm(request.form)
    app = SelectAppForm(request.form)
    if src_addr.validate_on_submit() and dst_addr.validate_on_submit():
        access = Accesses(name=name.name.data,
                         src=src_addr.addr_groups.name,
                         dst=dst_addr.addr_groups.name,
                         app=app.app_groups.name)
        db.session.add(access)
        db.session.commit()
        json_to_api["name"] = access.name
        json_to_api["src"] = access.src
        json_to_api["dst"] = access.dst
        json_to_api["app"] = access.app
        json.dumps(json_to_api)
        flash(json_to_api)
        flash("Address group added", "success")
        return redirect(url_for("main.home"))
    return redirect(url_for("main.about"))
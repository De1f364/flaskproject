# project/server/main/views.py


from flask import render_template, Blueprint, request, flash, redirect, url_for

from project.server import bcrypt, db
from project.server.models import Address, Application, Addrgroup, Appgroup, Accesses, Projects
from project.server.main.forms import CreateAddress, CreateApp, AddressForm, AppForm, SelectAddrFormSRC, SelectAddrFormDST, SelectAppForm, SelectProjectForm, AccessName, CreateProject

import json
import re

main_blueprint = Blueprint("main", __name__)


def search_db(dbase, data, count):
    choices = [(choice.id, choice.name) for choice in dbase.query.all()]
    for i in choices:
        if int(str(data)[count:-1]) == i[0]:
            choice_name = i[1].lower()
            return choice_name


def create_list(content):
    content = re.findall('[a-zа-яё0-9./_]+', content, flags=re.IGNORECASE)
    print('CONTENT:', content)
    return content


@main_blueprint.route("/")
def home():
    access_name = AccessName()
    select_project = SelectProjectForm()
    new_project = CreateProject()
    return render_template("main/home.html",
                           access_name=access_name,
                           new_project=new_project,
                           select_project=select_project)


@main_blueprint.route("/add_project/")
def add_project():
    new_project = CreateProject()
    return render_template("main/add_project.html",
                           new_project=new_project)


@main_blueprint.route("/create_address/")
def create_address():
    address = CreateAddress()
    return render_template("main/create_address.html",
                           address=address)


@main_blueprint.route("/create_app/")
def create_app():
    app = CreateApp()
    return render_template("main/create_app.html",
                           app=app)


@main_blueprint.route("/create_addr_group/")
def create_addr_group():
    addr_form = AddressForm()
    select_project = SelectProjectForm()
    return render_template("main/create_addr_group.html",
                           addr_form=addr_form,
                           select_project=select_project)


@main_blueprint.route("/create_app_group/")
def create_app_group():
    app_form = AppForm()
    select_project = SelectProjectForm()
    return render_template("main/create_app_group.html",
                           app_form=app_form,
                           select_project=select_project)


@main_blueprint.route("/handle_data_create_address", methods=["GET", "POST"])
def handle_data_create_address():
    json_to_api = {}
    address = CreateAddress(request.form)
    if address.validate_on_submit():
        print('YOOOOO', address.project.data)
        project_name = search_db(Projects, address.project.data, 10)
        # addr_list = create_list(addr_form.addresses.data)
        address_to_db = Address(project=project_name,
                                name=address.address_name.data,
                                addr_type=address.address_type.data,
                                address=address.address.data)
        db.session.add(address_to_db)
        db.session.commit()
        json_to_api["id"] = address.address_name.data
        json_to_api["address"] = address.address.data
        json_to_api["type"] = address.address_type.data
        json.dumps(json_to_api)
        flash(json_to_api)
        flash("Address added", "success")
        return redirect(url_for("main.create_address"))
    flash("Address add failed", "error")
    return redirect(url_for("main.create_address"))


@main_blueprint.route("/handle_data_create_app", methods=["GET", "POST"])
def handle_data_create_app():
    json_to_api = {}
    app = CreateApp(request.form)
    if app.validate_on_submit():
        print('YOOOOO', app.project.data)
        project_name = search_db(Projects, app.project.data, 10)
        # addr_list = create_list(addr_form.addresses.data)
        app_to_db = Application(project=project_name,
                                name=app.app_name.data,
                                protocol=app.app_protocol.data,
                                port=app.app_port.data)
        db.session.add(app_to_db)
        db.session.commit()
        json_to_api["id"] = app.app_name.data
        json_to_api["port"] = app.app_port.data
        json_to_api["protocol"] = app.app_protocol.data
        json.dumps(json_to_api)
        flash(json_to_api)
        flash("App added", "success")
        return redirect(url_for("main.create_app"))
    flash("App add failed", "error")
    return redirect(url_for("main.create_app"))


@main_blueprint.route("/handle_data_addr", methods=["GET", "POST"])
def handle_data_addr():
    json_to_api = {}
    addr_form = AddressForm(request.form)
    if addr_form.validate_on_submit():
        project_name = search_db(Projects, addr_form.project_select.data, 10)
        addr_list = create_list(addr_form.addresses.data)
        group_name = Addrgroup(project=project_name, name=addr_form.name_addrs.data, addresses=str(addr_list))
        db.session.add(group_name)
        db.session.commit()
        json_to_api["id"] = group_name.name
        json_to_api["addresses"] = addr_list
        json.dumps(json_to_api)
        flash(json_to_api)
        flash("Address group added", "success")
        return redirect(url_for("main.create_addr_group"))
    flash("Address group add failed", "error")
    return redirect(url_for("main.main.create_addr_group"))


@main_blueprint.route("/handle_data_app", methods=["GET", "POST"])
def handle_data_app():
    json_to_api = {}
    app_form = AppForm(request.form)
    if app_form.validate_on_submit():
        project_name = search_db(Projects, app_form.project_app.data, 10)
        app_list = create_list(app_form.apps.data)
        group_name = Appgroup(project=project_name, name=app_form.name_apps.data, apps=str(app_list))
        db.session.add(group_name)
        db.session.commit()

        json_to_api["id"] = group_name.name
        json_to_api["port"] = app_list
        json_to_api["protocol"] = "tcp"
        json.dumps(json_to_api)
        flash(json_to_api)
        flash("App group added", "success")
        return redirect(url_for("main.home"))
    return redirect(url_for("main.home"))


@main_blueprint.route("/handle_data_project", methods=["GET", "POST"])
def handle_data_project():
    new_project = CreateProject(request.form)
    if new_project.validate_on_submit():
        print(new_project.project_name.data)
        add_project = Projects(name=new_project.project_name.data)
        db.session.add(add_project)
        db.session.commit()

        flash("Project created", "success")
        return redirect(url_for("main.home"))
    return redirect(url_for("main.home"))


@main_blueprint.route("/handle_data_accesses", methods=["GET", "POST"])
def handle_data_accesses():
    json_to_api = {}
    project = SelectProjectForm(request.form)
    name = AccessName(request.form)
    select_src_addr = SelectAddrFormSRC(request.form)
    select_dst_addr = SelectAddrFormDST(request.form)
    app = SelectAppForm(request.form)
    if select_src_addr.validate_on_submit() and select_dst_addr.validate_on_submit():
        addrgroup_name_src = search_db(Addrgroup, select_src_addr.src_groups.data, 11)
        addrgroup_name_dst = search_db(Addrgroup, select_dst_addr.dst_groups.data, 11)
        appgroup_name = search_db(Appgroup, app.app_groups.data, 10)
        access = Accesses(name=name.name.data,
                          src=addrgroup_name_src,
                          dst=addrgroup_name_dst,
                          app=appgroup_name)
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
    get_access_addr_src = SelectAddrFormSRC()
    get_access_addr_dst = SelectAddrFormDST()
    get_access_app = SelectAppForm()
    # project_choices = [(projects.id, projects.name) for projects in Projects.query.all()]
    if project.validate_on_submit():
        # print('PROJECTS', project_choices)
        # print('ID:', int(str(project.project_select.data)[10:-1]))
        # for i in project_choices:
        #     if int(str(project.project_select.data)[10:-1]) == i[0]:
        #         project_name = i[1]
        #         get_access_addr_src.src_groups.query = Addrgroup.query.filter(Addrgroup.project == project_name.lower())
        #         get_access_addr_dst.dst_groups.query = Addrgroup.query.filter(Addrgroup.project == project_name.lower())
        #         get_access_app.app_groups.query = Appgroup.query.filter(Appgroup.project == project_name.lower())
        #         print('PROJECT NAME', project_name.lower())
        #         break
        project_name = search_db(Projects, project.project_select.data, 10)
        get_access_addr_src.src_groups.query = Addrgroup.query.filter(Addrgroup.project == project_name)
        get_access_addr_dst.dst_groups.query = Addrgroup.query.filter(Addrgroup.project == project_name)
        get_access_app.app_groups.query = Appgroup.query.filter(Appgroup.project == project_name)
        # flash(Addrgroup.query.filter_by(project=project.project_select.data), 'success')
        flash(type(project.project_select.data), 'success')
        return render_template("main/get_accesses.html",
                               get_access_addr_src=get_access_addr_src,
                               get_access_addr_dst=get_access_addr_dst,
                               get_access_app=get_access_app,
                               project=project.project_select,
                               name=project.name)
    return redirect(url_for("main.home"))

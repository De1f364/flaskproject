# project/server/main/views.py


from flask import render_template, Blueprint, request, flash, redirect, url_for

from project.server import bcrypt, db
from project.server.models import Addrgroup, Appgroup
from project.server.main.forms import AddressForm, AppForm, SelectAddrForm, SelectAppForm

main_blueprint = Blueprint("main", __name__)


@main_blueprint.route("/")
def home():
    addr_form = AddressForm()
    app_form = AppForm()
    select_addr_form = SelectAddrForm()
    select_app_form = SelectAppForm()
    return render_template("main/home.html",
                           addr_form=addr_form,
                           app_form=app_form,
                           select_addr_form=select_addr_form,
                           select_app_form=select_app_form)


@main_blueprint.route("/about/")
def about():
    flash(Addrgroup.query.with_entities(Addrgroup.name))
    return render_template("main/about.html")


@main_blueprint.route("/handle_data_addr", methods=["GET", "POST"])
def handle_data_addr():
    addr_form = AddressForm(request.form)
    if addr_form.validate_on_submit():
        group_name = Addrgroup(name=addr_form.name_addrs.data, addresses=addr_form.addresses.data)
        db.session.add(group_name)
        db.session.commit()


        flash("Address group added", "success")
        return redirect(url_for("main.home"))
    return redirect(url_for("main.about"))


@main_blueprint.route("/handle_data_app", methods=["GET", "POST"])
def handle_data_app():
    app_form = AppForm(request.form)
    if app_form.validate_on_submit():
        group_name = Appgroup(name=app_form.name_apps.data, apps=app_form.apps.data)
        db.session.add(group_name)
        db.session.commit()


        flash("App group added", "success")
        return redirect(url_for("main.home"))
    return redirect(url_for("main.about"))
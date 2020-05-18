# project/server/main/views.py


from flask import render_template, Blueprint, request, flash, redirect, url_for

from project.server import bcrypt, db
from project.server.models import Addrgroup, Appgroup
from project.server.main.forms import AddressForm, AppForm

main_blueprint = Blueprint("main", __name__)


@main_blueprint.route("/")
def home():
    return render_template("main/home.html")


@main_blueprint.route("/about/")
def about():
    return render_template("main/about.html")


@main_blueprint.route("/handle_data", methods=["POST"])
def handle_data():
    form = AddressForm(request.form)
    print(form)
    if form.validate_on_submit():
        group_name = Addrgroup(name=form.name.data, addresses=form.addresses.data)
        db.session.add(group_name)
        db.session.commit()


        flash("Address group added")
        return redirect(url_for("main.home"))
    # group_name = request.form['groupName']
    # address_list = request.form['addressList']
    return redirect(url_for("main.about"))


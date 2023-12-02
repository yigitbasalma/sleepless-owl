from flask import Blueprint, render_template, url_for, redirect
from flask_login import current_user

from w.apps.auth.forms import LoginForm, RegisterForm

index = Blueprint("index", __name__)


@index.route("/", methods=["GET"])
def welcome():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    return render_template(
        "index.html",
        form_login=LoginForm(),
        form_register=RegisterForm()
    )

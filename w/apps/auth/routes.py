from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required

from .forms import LoginForm, RegisterForm
from .controllers import login_customer_user, logout_customer_user, register_customer_user

auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.route("/", methods=["POST"])
def user_login():
    form_login = LoginForm()

    if form_login.validate_on_submit():
        return login_customer_user(form=form_login)

    _errors = []
    for fieldName, errorMessages in form_login.errors.items():
        for err in errorMessages:
            _errors.append(f"{form_login[fieldName].label.text}: {err}")

    return jsonify({
        "status": "error",
        "message": f"{_errors[0]}"
    })


@auth.route("/register", methods=["GET", "POST"])
def user_register():
    form_register = RegisterForm()

    if request.method in ("POST", ):
        if form_register.validate_on_submit():
            return register_customer_user(form=form_register)

        _errors = []
        for fieldName, errorMessages in form_register.errors.items():
            for err in errorMessages:
                _errors.append(f"{form_register[fieldName].label.text}: {err}")

        return jsonify({
            "status": "error",
            "message": f"{_errors[0]}"
        })

    return render_template(
        "auth/register.html",
        form_register=form_register
    )


@auth.route("/logout")
@login_required
def user_logout():
    return logout_customer_user()

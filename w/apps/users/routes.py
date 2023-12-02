from flask import Blueprint, render_template
from flask_login import login_required

from w import authorize
from w.apps.auth.models import Users

from .controllers import delete_user_func, toggle_user_role_func

users = Blueprint("users", __name__, url_prefix="/users")


@users.route("/", methods=["GET"])
@login_required
@authorize.has_role("admin")
def index():
    return render_template(
        "users/users.html",
        users=Users.all(conditions=[])
    )


@users.route("/<user_id>/delete", methods=["GET"])
@login_required
@authorize.has_role("admin")
def delete_user(user_id):
    return delete_user_func(user_id=user_id)


@users.route("/<user_id>/toggle-role", methods=["GET"])
@login_required
@authorize.has_role("admin")
def toggle_user_role(user_id):
    return toggle_user_role_func(user_id=user_id)
